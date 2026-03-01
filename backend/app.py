import os
import random
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from flask_cors import CORS

from game_manager import game_manager, GameState

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ai_mafia_secret')

# Enable CORS for HTTP routes
CORS(app)

# Initialize SocketIO with aggressive CORS to allow 127.0.0.1 and localhost
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')


def broadcast_game_state():
    """Helper to broadcast the current game state to all clients."""
    state_data = {
        'state': game_manager.state,
        'players': game_manager.get_player_list(),
        'round': game_manager.round,
        'current_turn': game_manager.get_current_turn_sid(),
        'spectators': game_manager.get_spectator_list(),
    }
    socketio.emit('game_update', state_data)


def broadcast_turn_update():
    """Broadcast the current turn info to all clients."""
    current_sid = game_manager.get_current_turn_sid()
    current_player = game_manager.players.get(current_sid, {})
    socketio.emit('turn_update', {
        'current_turn_sid': current_sid,
        'current_turn_name': current_player.get('name', ''),
        'time_left': 20,
    })


def ai_turn_task():
    """Handle AI's turn: simulate typing delay, then send a response."""
    if game_manager.state != GameState.CHAT:
        return
    current_sid = game_manager.get_current_turn_sid()
    if current_sid != game_manager.ai_sid:
        return

    socketio.sleep(random.uniform(2, 5))  # simulate typing delay

    if game_manager.state != GameState.CHAT:
        return

    from ai_agent import ai_agent
    reply = ai_agent.generate_chat_response(game_manager.chat_history)

    msg_obj = {'sender': ai_agent.ai_name, 'text': reply}
    game_manager.chat_history.append(msg_obj)
    socketio.emit('receive_message', msg_obj)

    # Advance turn after AI sends message
    game_manager.advance_turn()
    if game_manager.all_turns_complete():
        game_manager.check_chat_phase_complete()
        broadcast_game_state()
    else:
        broadcast_turn_update()
        # If next turn is also AI (shouldn't happen), handle it
        if game_manager.get_current_turn_sid() == game_manager.ai_sid:
            socketio.start_background_task(ai_turn_task)


def turn_timer_task():
    """Run the 20-second timer for the current turn."""
    while game_manager.state == GameState.CHAT and not game_manager.all_turns_complete():
        current_sid = game_manager.get_current_turn_sid()
        if current_sid is None:
            break

        # If it's the AI's turn, let the AI task handle it
        if current_sid == game_manager.ai_sid:
            socketio.start_background_task(ai_turn_task)
            # Wait for AI to finish its turn
            while (game_manager.state == GameState.CHAT and
                   game_manager.get_current_turn_sid() == game_manager.ai_sid):
                socketio.sleep(0.5)
            continue

        # Human player's turn: 20-second countdown
        time_left = 20
        turn_sid_at_start = game_manager.get_current_turn_sid()
        while time_left > 0 and game_manager.state == GameState.CHAT:
            # Check if turn was already advanced (player sent a message)
            if game_manager.get_current_turn_sid() != turn_sid_at_start:
                break
            socketio.emit('timer_update', {'time_left': time_left, 'current_turn_sid': turn_sid_at_start})
            socketio.sleep(1)
            time_left -= 1

        # If the player didn't send a message, timeout and advance
        if (game_manager.state == GameState.CHAT and
                game_manager.get_current_turn_sid() == turn_sid_at_start):
            game_manager.advance_turn()
            if game_manager.all_turns_complete():
                game_manager.check_chat_phase_complete()
                broadcast_game_state()
            else:
                broadcast_turn_update()

    # If we exited the loop because all turns are complete
    if game_manager.state == GameState.CHAT and game_manager.all_turns_complete():
        game_manager.check_chat_phase_complete()
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
        'round': game_manager.round,
        'current_turn': game_manager.get_current_turn_sid(),
        'spectators': game_manager.get_spectator_list(),
    })


@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")
    game_manager.remove_spectator(request.sid)
    game_manager.remove_player(request.sid)
    broadcast_game_state()


@socketio.on('join_game')
def handle_join(data=None):
    # If game is in progress, join as spectator
    if game_manager.state != GameState.LOBBY:
        success, msg = game_manager.add_spectator(request.sid)
        if success:
            nickname = game_manager.spectators[request.sid]['name']
            broadcast_game_state()
            return {'success': success, 'message': msg, 'spectator': True, 'nickname': nickname}
        return {'success': success, 'message': msg, 'spectator': True}

    success, msg = game_manager.add_player(request.sid)
    if success:
        nickname = game_manager.players[request.sid]['name']
        broadcast_game_state()
        return {'success': success, 'message': msg, 'nickname': nickname}
    return {'success': success, 'message': msg}


@socketio.on('start_game')
def handle_start():
    from ai_agent import ai_agent
    ai_agent.reset_identity()  # random name for a new game
    success, msg = game_manager.start_game(ai_agent.ai_name, requester_sid=request.sid)
    if success:
        broadcast_game_state()
        broadcast_turn_update()
        socketio.start_background_task(turn_timer_task)
    return {'success': success, 'message': msg}


@socketio.on('send_message')
def handle_message(data):
    text = data.get('text')
    if game_manager.state != GameState.CHAT or not text:
        return

    # Only the active turn player can send a message
    if not game_manager.can_send_message(request.sid):
        return

    sender = game_manager.players.get(request.sid)
    if not sender:
        return

    msg_obj = {'sender': sender['name'], 'text': text}
    game_manager.chat_history.append(msg_obj)
    emit('receive_message', msg_obj, broadcast=True)

    # Advance turn after message is sent
    game_manager.advance_turn()
    if game_manager.all_turns_complete():
        game_manager.check_chat_phase_complete()
        broadcast_game_state()
    else:
        broadcast_turn_update()


@socketio.on('submit_vote')
def handle_vote(data):
    target_name = data.get('target')
    if not target_name:
        return {'success': False, 'message': 'Target required.'}

    success, msg = game_manager.submit_vote(request.sid, target_name)
    if success:
        if msg == "All_Voted":
            broadcast_game_state()
            emit('game_result', game_manager.last_round_result, broadcast=True)

            # Start timer for next round if game not over
            if not game_manager.last_round_result.get('game_over'):
                socketio.start_background_task(next_round_task)
    return {'success': success, 'message': msg}


@socketio.on('restart_game')
def handle_restart():
    success, msg = game_manager.reset_game(requester_sid=request.sid)
    if success:
        # Build nickname map so each client can update their displayed name
        nickname_map = {sid: p['name'] for sid, p in game_manager.players.items()}
        nickname_map.update({sid: s['name'] for sid, s in game_manager.spectators.items()})
        broadcast_game_state()
        socketio.emit('nickname_update', nickname_map)
    return {'success': success, 'message': msg}


@socketio.on('spectator_opt_in')
def handle_spectator_opt_in(data):
    opt_in = data.get('opt_in', False)
    game_manager.spectator_opt_in(request.sid, opt_in)
    return {'success': True}


def next_round_task():
    socketio.sleep(8)  # 8 seconds to view results
    if game_manager.state == GameState.RESULT:
        game_manager.state = GameState.CHAT
        game_manager.round += 1
        game_manager.chat_history = []
        game_manager.votes = {}
        game_manager._generate_turn_order()
        broadcast_game_state()
        broadcast_turn_update()
        socketio.start_background_task(turn_timer_task)


if __name__ == '__main__':
    socketio.run(
        app,
        host=os.getenv('FLASK_HOST', '127.0.0.1'),
        port=int(os.getenv('FLASK_PORT', '5000')),
        debug=os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    )
