import os
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv

from game_manager import game_manager, GameState

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ai_mafia_secret')

# Initialize SocketIO with CORS allowed for the frontend
socketio = SocketIO(app, cors_allowed_origins="*")

def broadcast_game_state():
    """Helper to broadcast the current game state to all clients."""
    state_data = {
        'state': game_manager.state,
        'players': game_manager.get_player_list(),
        'round': game_manager.round
    }
    socketio.emit('game_update', state_data)

@app.route('/')
def index():
    return jsonify({"status": "AI Mafia backend is running!"})

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")
    # Always send current state on connect
    emit('game_update', {
        'state': game_manager.state,
        'players': game_manager.get_player_list(),
        'round': game_manager.round
    })

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")
    game_manager.remove_player(request.sid)
    broadcast_game_state()

@socketio.on('join_game')
def handle_join(data):
    name = data.get('name')
    if not name:
        return {'success': False, 'message': 'Name required.'}
    
    success, msg = game_manager.add_player(request.sid, name)
    if success:
        broadcast_game_state()
    return {'success': success, 'message': msg}

@socketio.on('start_game')
def handle_start():
    success, msg = game_manager.start_game()
    if success:
        broadcast_game_state()
    return {'success': success, 'message': msg}

if __name__ == '__main__':
    # Run the SocketIO development server
    socketio.run(app, debug=True, port=5000)
