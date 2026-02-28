import os
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ai_mafia_secret')

# Initialize SocketIO with CORS allowed for the frontend (Vite default is usually 5173)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return jsonify({"status": "AI Mafia backend is running!"})

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")

if __name__ == '__main__':
    # Run the SocketIO development server
    socketio.run(app, debug=True, port=5000)
