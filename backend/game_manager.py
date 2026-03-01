import random

NICKNAME_POOL = [
    'Sunny', 'Rocky', 'Pepper', 'Clover', 'Blaze', 'Maple', 'Storm',
    'Coral', 'Dash', 'Echo', 'Frost', 'Ginger', 'Hazel', 'Ivy', 'Jet',
    'Kiwi', 'Luna', 'Mango', 'Nova', 'Olive', 'Pebble', 'Quinn', 'Raven',
    'Sage', 'Tiger', 'Uma', 'Viper', 'Willow', 'Ziggy', 'Amber', 'Birch',
    'Cedar', 'Dusk', 'Ember', 'Flint', 'Grove',
]

class GameState:
    LOBBY = 'LOBBY'
    CHAT = 'CHAT'
    VOTING = 'VOTING'
    RESULT = 'RESULT'

class GameManager:
    def __init__(self):
        self.state = GameState.LOBBY
        self.players = {}  # sid -> {'name': str, 'is_ai': bool, 'eliminated': bool, 'is_host': bool}
        self.round = 0
        self.chat_history = []
        self.ai_sid = "ai_player_0"
        self.votes = {} # sid -> target_name
        self.last_round_result = {}
        self.host_sid = None
        self._join_order = []  # track join order for host transfer
        self.turn_order = []  # list of sids in speaking order
        self.current_turn_index = 0
        self.spectators = {}  # sid -> {'name': str}

    def _get_used_names(self):
        """Return set of all names currently in use by players and spectators."""
        names = {p['name'] for p in self.players.values()}
        names.update(s['name'] for s in self.spectators.values())
        return names

    def assign_nickname(self):
        """Assign a random unique nickname from the pool."""
        used = self._get_used_names()
        available = [n for n in NICKNAME_POOL if n not in used]
        if not available:
            # Fallback: generate a numbered name
            i = 1
            while f"Player{i}" in used:
                i += 1
            return f"Player{i}"
        return random.choice(available)

    def add_player(self, sid, name=None):
        if self.state != GameState.LOBBY:
            return False, "Game already started."
        if name is None:
            name = self.assign_nickname()
        if any(p['name'] == name for p in self.players.values()):
            return False, "Name already taken."
        is_host = self.host_sid is None
        self.players[sid] = {'name': name, 'is_ai': False, 'eliminated': False, 'is_host': is_host}
        self._join_order.append(sid)
        if is_host:
            self.host_sid = sid
        return True, "Player joined."

    def remove_player(self, sid):
        if sid in self.players:
            was_host = self.players[sid].get('is_host', False)
            del self.players[sid]
            if sid in self._join_order:
                self._join_order.remove(sid)
            if was_host:
                self._transfer_host()

    def _transfer_host(self):
        """Transfer host to the next player in join order."""
        self.host_sid = None
        for candidate_sid in self._join_order:
            if candidate_sid in self.players:
                self.host_sid = candidate_sid
                self.players[candidate_sid]['is_host'] = True
                break

    def get_player_list(self):
        return [{'sid': sid, 'name': p['name'], 'eliminated': p.get('eliminated', False), 'is_ai': p.get('is_ai', False), 'is_host': p.get('is_host', False)} for sid, p in self.players.items()]

    def get_living_players(self):
        return [p for p in self.players.values() if not p.get('eliminated', False)]

    def start_game(self, ai_name, requester_sid=None):
        if self.state != GameState.LOBBY:
            return False, "Game is not in LOBBY state."
        if requester_sid is None or requester_sid != self.host_sid:
            return False, "Only the host can start the game."
        if len(self.players) < 3:
            return False, "Not enough players. Need at least 3."
            
        while any(p['name'] == ai_name for p in self.players.values()):
            ai_name += str(random.randint(1,9))
            
        for p in self.players.values():
            p['eliminated'] = False
            
        self.players[self.ai_sid] = {'name': ai_name, 'is_ai': True, 'eliminated': False}
        
        self.state = GameState.CHAT
        self.round = 1
        self.chat_history = []
        self.votes = {}
        self.last_round_result = {}
        self._generate_turn_order()
        return True, "Game started."

    def _generate_turn_order(self):
        """Generate a randomized speaking order for the current round."""
        living_sids = [sid for sid, p in self.players.items()
                       if not p.get('eliminated', False)]
        random.shuffle(living_sids)
        self.turn_order = living_sids
        self.current_turn_index = 0

    def get_current_turn_sid(self):
        """Return the sid of the player whose turn it is."""
        if self.current_turn_index >= len(self.turn_order):
            return None
        return self.turn_order[self.current_turn_index]

    def advance_turn(self):
        """Advance to the next turn. Returns the next player's sid, or None if all turns are done."""
        self.current_turn_index += 1
        if self.current_turn_index >= len(self.turn_order):
            return None
        return self.turn_order[self.current_turn_index]

    def all_turns_complete(self):
        """Check if all players have had their turn."""
        return self.current_turn_index >= len(self.turn_order)

    def can_send_message(self, sid):
        """Check if the given sid is the active turn player."""
        if self.state != GameState.CHAT:
            return False
        return sid == self.get_current_turn_sid()

    def add_spectator(self, sid, name=None):
        """Add a spectator (late joiner or eliminated player watching)."""
        if name is None:
            name = self.assign_nickname()
        self.spectators[sid] = {'name': name}
        return True, "Joined as spectator."

    def remove_spectator(self, sid):
        """Remove a spectator on disconnect."""
        if sid in self.spectators:
            del self.spectators[sid]

    def get_spectator_list(self):
        """Return list of spectator info dicts."""
        return [{'sid': sid, 'name': s['name']} for sid, s in self.spectators.items()]

    def check_chat_phase_complete(self):
        """Transition to VOTING if all turns are complete."""
        if self.all_turns_complete():
            self.state = GameState.VOTING

    def submit_vote(self, sid, target_name):
        if self.state != GameState.VOTING:
            return False, "Not in voting phase."
        if sid not in self.players:
            return False, "You are not in the game."
        if self.players[sid].get('eliminated', False):
            return False, "You are eliminated and cannot vote."
            
        self.votes[sid] = target_name
        
        # Check if everyone living has voted
        living_sids = [k for k, v in self.players.items() if not v.get('eliminated', False)]
        
        # Auto-vote for AI if it hasn't
        if self.ai_sid in living_sids and self.ai_sid not in self.votes:
            # Make AI vote randomly for a human
            targets = [p['name'] for p in self.get_living_players() if not p['is_ai']]
            if targets:
                self.votes[self.ai_sid] = random.choice(targets)
            else:
                self.votes[self.ai_sid] = self.players[self.ai_sid]['name'] # Vote self if impossible

        # Re-check after possible AI vote
        if len(self.votes) >= len(living_sids):
            self.resolve_votes()
            return True, "All_Voted"
            
        return True, "Vote registered."
        
    def resolve_votes(self):
        vote_counts = {}
        for target in self.votes.values():
            vote_counts[target] = vote_counts.get(target, 0) + 1

        if not vote_counts:
            eliminated_name = None
        else:
            sorted_votes = sorted(vote_counts.items(), key=lambda x: x[1], reverse=True)
            max_votes = sorted_votes[0][1]
            tied = [name for name, count in sorted_votes if count == max_votes]
            eliminated_name = random.choice(tied)

        human_won = False
        game_over = False

        if eliminated_name:
            for sid, p in self.players.items():
                if p['name'] == eliminated_name:
                    p['eliminated'] = True
                    if p['is_ai']:
                        human_won = True
                        game_over = True
                    break

        self.last_round_result = {
            'votes': vote_counts,
            'eliminated': eliminated_name,
            'ai_won': False,
            'human_won': human_won,
            'game_over': game_over
        }

        if not game_over:
            living = self.get_living_players()
            ai_alive = any(p['is_ai'] for p in living)
            if ai_alive and len(living) <= 3:
                self.last_round_result['ai_won'] = True
                self.last_round_result['game_over'] = True
                self.last_round_result['human_won'] = False

        self.state = GameState.RESULT

    def spectator_opt_in(self, sid, opt_in):
        """Track a spectator's choice to join or stay spectating on restart."""
        if sid not in self.spectators:
            return False
        self.spectators[sid]['opt_in'] = opt_in
        return True

    def reset_game(self, requester_sid=None):
        """Reset the game back to LOBBY state. Only the host can do this."""
        if self.state != GameState.RESULT:
            return False, "Game is not in RESULT state."
        if requester_sid is None or requester_sid != self.host_sid:
            return False, "Only the host can restart the game."

        # Remove AI player
        if self.ai_sid in self.players:
            del self.players[self.ai_sid]
            if self.ai_sid in self._join_order:
                self._join_order.remove(self.ai_sid)

        # Move opted-in spectators to players
        opted_in_sids = [sid for sid, s in self.spectators.items() if s.get('opt_in')]
        for sid in opted_in_sids:
            del self.spectators[sid]
            self.players[sid] = {'name': '', 'is_ai': False, 'eliminated': False, 'is_host': False}
            if sid not in self._join_order:
                self._join_order.append(sid)

        # Clear opt_in flags on remaining spectators
        for s in self.spectators.values():
            s.pop('opt_in', None)

        # Re-assign nicknames to all players (clear names first to avoid conflicts)
        for p in self.players.values():
            p['name'] = ''
        # Also clear spectator names temporarily for uniqueness check
        old_spectator_names = {sid: s['name'] for sid, s in self.spectators.items()}
        for s in self.spectators.values():
            s['name'] = ''
        # Assign new names to players
        for sid in self.players:
            self.players[sid]['name'] = self.assign_nickname()
        # Re-assign spectator names
        for sid in self.spectators:
            self.spectators[sid]['name'] = self.assign_nickname()

        # Reset game data
        self.state = GameState.LOBBY
        self.round = 0
        self.chat_history = []
        self.votes = {}
        self.last_round_result = {}
        self.turn_order = []
        self.current_turn_index = 0

        # Reset eliminated status and preserve host
        for sid, p in self.players.items():
            p['eliminated'] = False
            p['is_host'] = (sid == self.host_sid)

        return True, "Game reset."


game_manager = GameManager()
