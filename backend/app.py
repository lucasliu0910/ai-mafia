import os
import random
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

ai_is_typing = False

def broadcast_game_state():
    """Helper to broadcast the current game state to all clients."""
    state_data = {
        'state': game_manager.state,
        'players': game_manager.get_player_list(),
        'round': game_manager.round
    }
    socketio.emit('game_update', state_data)

def ai_respond_task():
    global ai_is_typing
    if ai_is_typing or game_manager.state != GameState.CHAT:
        return
    ai_is_typing = True
    socketio.sleep(random.uniform(3, 6)) # simulate typing delay
    
    if game_manager.state != GameState.CHAT:
        ai_is_typing = False
        return
        
    from ai_agent import ai_agent
    reply = ai_agent.generate_chat_response(game_manager.chat_history)
    
    msg_obj = {'sender': ai_agent.ai_name, 'text': reply}
    game_manager.chat_history.append(msg_obj)
    socketio.emit('receive_message', msg_obj)
    ai_is_typing = False

def chat_timer_task():
    time_left = 60
    # First AI message
    socketio.start_background_task(ai_respond_task)
    
    while time_left > 0 and game_manager.state == GameState.CHAT:
        socketio.emit('timer_update', {'time_left': time_left})
        socketio.sleep(1)
        time_left -= 1
        
    if game_manager.state == GameState.CHAT and time_left <= 0:
        game_manager.state = GameState.VOTING
        broadcast_game_state()

@app.route('/')
def index():
    return jsonify({"status": "AI Mafia backend is running!"})

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")
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
    from ai_agent import ai_agent
    ai_agent.reset_identity() # random name for a new game
    success, msg = game_manager.start_game(ai_agent.ai_name)
    if success:
        broadcast_game_state()
        socketio.start_background_task(chat_timer_task)
    return {'success': success, 'message': msg}

@socketio.on('send_message')
def handle_message(data):
    text = data.get('text')
    if game_manager.state != GameState.CHAT or not text:
        return
        
    sender = game_manager.players.get(request.sid)
    if not sender:
        return
        
    msg_obj = {'sender': sender['name'], 'text': text}
    game_manager.chat_history.append(msg_obj)
    emit('receive_message', msg_obj, broadcast=True)
    
    from ai_agent import ai_agent
    mentioned = ai_agent.ai_name.lower() in text.lower()
    
    # AI responds if mentioned, or randomly (30% chance)
    if mentioned or random.random() < 0.3:
        socketio.start_background_task(ai_respond_task)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
