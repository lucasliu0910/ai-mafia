#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# AI Mafia — AWS EC2 Deployment Script
#
# Usage:
#   First time:   ./deploy/deploy.sh
#   Re-deploy:    ./deploy/deploy.sh --update <server-ip>
# ============================================================

REGION="${AWS_REGION:-us-east-1}"
INSTANCE_TYPE="t3.micro"
KEY_NAME="ai-mafia-key"
KEY_FILE="deploy/${KEY_NAME}.pem"
SG_NAME="ai-mafia-sg"
INSTANCE_NAME="ai-mafia-server"
REMOTE_USER="ec2-user"
REMOTE_DIR="/home/${REMOTE_USER}/ai-mafia"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

SSH_OPTS="-o StrictHostKeyChecking=no -o ConnectTimeout=10"

# ============================================================
# Helper functions
# ============================================================

log()  { echo "==> $*"; }
err()  { echo "ERROR: $*" >&2; exit 1; }

wait_for_ssh() {
    local ip="$1" max_attempts=30 attempt=0
    log "Waiting for SSH on ${ip}..."
    while ! ssh ${SSH_OPTS} -i "${KEY_FILE}" "${REMOTE_USER}@${ip}" "echo ok" &>/dev/null; do
        attempt=$((attempt + 1))
        if [ "${attempt}" -ge "${max_attempts}" ]; then
            err "SSH not available after ${max_attempts} attempts"
        fi
        sleep 10
    done
    log "SSH is ready."
}

sync_and_deploy() {
    local ip="$1"

    log "Syncing project files to ${ip}..."
    rsync -avz --delete \
        --exclude '.git' \
        --exclude 'node_modules' \
        --exclude 'venv' \
        --exclude '__pycache__' \
        --exclude '.coverage' \
        --exclude '.pytest_cache' \
        --exclude '.env' \
        --exclude '.DS_Store' \
        --exclude '.agent' \
        --exclude '.claude' \
        --exclude '*.pyc' \
        -e "ssh ${SSH_OPTS} -i ${KEY_FILE}" \
        "${PROJECT_DIR}/" "${REMOTE_USER}@${ip}:${REMOTE_DIR}/"

    # Ensure .env exists on server
    ssh ${SSH_OPTS} -i "${KEY_FILE}" "${REMOTE_USER}@${ip}" bash <<'CHECK_ENV'
if [ ! -f /home/ec2-user/ai-mafia/.env ]; then
    echo ".env not found — creating it now."
    exit 1
fi
CHECK_ENV

    if [ $? -ne 0 ]; then
        log "Setting up .env on server..."
        echo ""
        read -rp "Enter your OPENAI_API_KEY (or press Enter to skip): " OPENAI_KEY
        SECRET=$(openssl rand -hex 32)

        ssh ${SSH_OPTS} -i "${KEY_FILE}" "${REMOTE_USER}@${ip}" bash <<ENVSETUP
cat > ${REMOTE_DIR}/.env <<EOF
OPENAI_API_KEY=${OPENAI_KEY}
SECRET_KEY=${SECRET}
EOF
chmod 600 ${REMOTE_DIR}/.env
echo ".env created."
ENVSETUP
    fi

    log "Building and starting containers..."
    ssh ${SSH_OPTS} -i "${KEY_FILE}" "${REMOTE_USER}@${ip}" bash <<'DEPLOY'
cd /home/ec2-user/ai-mafia
docker compose build
docker compose up -d
docker image prune -f
echo ""
echo "Container status:"
docker compose ps
DEPLOY

    echo ""
    echo "========================================"
    echo "  Deployed successfully!"
    echo "  Live at: http://${ip}"
    echo ""
    echo "  DNS setup:"
    echo "  Add an A record on your domain provider:"
    echo "    your-domain.com  →  ${ip}"
    echo "========================================"
}

# ============================================================
# --update mode: re-deploy to existing server
# ============================================================

if [ "${1:-}" = "--update" ]; then
    SERVER_IP="${2:?Usage: ./deploy/deploy.sh --update <server-ip>}"
    [ -f "${KEY_FILE}" ] || err "Key file not found: ${KEY_FILE}"
    sync_and_deploy "${SERVER_IP}"
    exit 0
fi

# ============================================================
# First-time provisioning
# ============================================================

command -v aws &>/dev/null || err "AWS CLI is not installed. Install it first: https://aws.amazon.com/cli/"

log "Provisioning EC2 instance in ${REGION}..."

# --- Detect latest Amazon Linux 2023 AMI ---
log "Finding latest Amazon Linux 2023 AMI..."
AMI_ID=$(aws ec2 describe-images \
    --owners amazon \
    --filters "Name=name,Values=al2023-ami-2023*-x86_64" \
              "Name=state,Values=available" \
    --query 'sort_by(Images, &CreationDate)[-1].ImageId' \
    --output text \
    --region "${REGION}")
log "Using AMI: ${AMI_ID}"

# --- Create key pair (skip if exists) ---
if [ -f "${KEY_FILE}" ]; then
    log "Key pair already exists: ${KEY_FILE}"
else
    log "Creating key pair: ${KEY_NAME}"
    aws ec2 create-key-pair \
        --key-name "${KEY_NAME}" \
        --query 'KeyMaterial' \
        --output text \
        --region "${REGION}" > "${KEY_FILE}"
    chmod 400 "${KEY_FILE}"
fi

# --- Create security group (skip if exists) ---
SG_ID=$(aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=${SG_NAME}" \
    --query 'SecurityGroups[0].GroupId' \
    --output text \
    --region "${REGION}" 2>/dev/null || echo "None")

if [ "${SG_ID}" = "None" ] || [ -z "${SG_ID}" ]; then
    log "Creating security group: ${SG_NAME}"
    SG_ID=$(aws ec2 create-security-group \
        --group-name "${SG_NAME}" \
        --description "AI Mafia game server" \
        --region "${REGION}" \
        --query 'GroupId' \
        --output text)

    aws ec2 authorize-security-group-ingress \
        --group-id "${SG_ID}" --protocol tcp --port 22 --cidr 0.0.0.0/0 --region "${REGION}"
    aws ec2 authorize-security-group-ingress \
        --group-id "${SG_ID}" --protocol tcp --port 80 --cidr 0.0.0.0/0 --region "${REGION}"
    aws ec2 authorize-security-group-ingress \
        --group-id "${SG_ID}" --protocol tcp --port 443 --cidr 0.0.0.0/0 --region "${REGION}"
else
    log "Security group already exists: ${SG_ID}"
fi

# --- Check for existing instance ---
EXISTING_IP=$(aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=${INSTANCE_NAME}" \
              "Name=instance-state-name,Values=running" \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text \
    --region "${REGION}" 2>/dev/null || echo "None")

if [ "${EXISTING_IP}" != "None" ] && [ -n "${EXISTING_IP}" ]; then
    log "Existing instance found at ${EXISTING_IP}. Re-deploying..."
    sync_and_deploy "${EXISTING_IP}"
    exit 0
fi

# --- User data: install Docker on first boot ---
USER_DATA=$(cat <<'USERDATA'
#!/bin/bash
dnf update -y
dnf install -y docker git
systemctl enable docker
systemctl start docker
usermod -aG docker ec2-user

# Install Docker Compose plugin
mkdir -p /usr/local/lib/docker/cli-plugins
ARCH=$(uname -m)
curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-${ARCH}" \
    -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# Signal setup complete
touch /home/ec2-user/.docker-ready
USERDATA
)

# --- Launch instance ---
log "Launching EC2 instance (${INSTANCE_TYPE})..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id "${AMI_ID}" \
    --instance-type "${INSTANCE_TYPE}" \
    --key-name "${KEY_NAME}" \
    --security-group-ids "${SG_ID}" \
    --user-data "${USER_DATA}" \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=${INSTANCE_NAME}}]" \
    --region "${REGION}" \
    --query 'Instances[0].InstanceId' \
    --output text)

log "Instance launched: ${INSTANCE_ID}"
log "Waiting for instance to be running..."

aws ec2 wait instance-running --instance-ids "${INSTANCE_ID}" --region "${REGION}"

PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids "${INSTANCE_ID}" \
    --region "${REGION}" \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

log "Instance running at ${PUBLIC_IP}"

# --- Wait for SSH + Docker to be ready ---
wait_for_ssh "${PUBLIC_IP}"

log "Waiting for Docker installation to complete..."
for i in $(seq 1 30); do
    if ssh ${SSH_OPTS} -i "${KEY_FILE}" "${REMOTE_USER}@${PUBLIC_IP}" "test -f /home/ec2-user/.docker-ready" 2>/dev/null; then
        break
    fi
    sleep 10
done

# Ensure docker group is effective (requires new login session)
ssh ${SSH_OPTS} -i "${KEY_FILE}" "${REMOTE_USER}@${PUBLIC_IP}" "newgrp docker || true" 2>/dev/null || true

# --- Deploy ---
sync_and_deploy "${PUBLIC_IP}"

echo ""
echo "  SSH access:"
echo "  ssh -i ${KEY_FILE} ${REMOTE_USER}@${PUBLIC_IP}"
echo ""
