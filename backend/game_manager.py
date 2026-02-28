import random

class GameState:
    LOBBY = 'LOBBY'
    CHAT = 'CHAT'
    VOTING = 'VOTING'
    RESULT = 'RESULT'

class GameManager:
    def __init__(self):
        self.state = GameState.LOBBY
        self.players = {}  # sid -> {'name': str, 'is_ai': bool}
        self.round = 0
        self.max_rounds = 3
        self.chat_history = [] 
        self.ai_sid = "ai_player_0" # dummy sid for the AI
        
    def add_player(self, sid, name):
        if self.state != GameState.LOBBY:
            return False, "Game already started."
        if any(p['name'] == name for p in self.players.values()):
            return False, "Name already taken."
        self.players[sid] = {'name': name, 'is_ai': False}
        return True, "Player joined."

    def remove_player(self, sid):
        if sid in self.players:
            del self.players[sid]

    def get_player_list(self):
        return [{'sid': sid, 'name': p['name']} for sid, p in self.players.items()]

    def start_game(self, ai_name):
        if self.state != GameState.LOBBY:
            return False, "Game is not in LOBBY state."
        if len(self.players) < 1:
            return False, "Not enough players."
            
        # Handle duplicate name for AI
        while any(p['name'] == ai_name for p in self.players.values()):
            ai_name += str(random.randint(1,9))
            
        self.players[self.ai_sid] = {'name': ai_name, 'is_ai': True}
        
        self.state = GameState.CHAT
        self.round = 1
        self.chat_history = []
        return True, "Game started."

game_manager = GameManager()
