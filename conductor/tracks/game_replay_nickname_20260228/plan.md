# Plan: Game Replay & Auto-Nickname System

## Phase 1: Auto-Assigned Nicknames (Backend) ✅ `7f30f61`

- [x] Task: Write tests for nickname list and random assignment in GameManager
- [x] Task: Implement nickname pool and assign_nickname method — maintain a list of ~30+ common English nicknames, randomly assign a unique one on player join
- [x] Task: Write tests for unique nickname enforcement among players and spectators
- [x] Task: Implement unique nickname validation — ensure no duplicate nicknames across players and spectators dicts
- [x] Task: Write tests for updated add_player accepting no name parameter
- [x] Task: Update add_player to auto-assign nickname when no name is provided
- [x] Task: Write tests for updated add_spectator auto-assigning nickname
- [x] Task: Update add_spectator to auto-assign nickname when no name is provided
- [x] Task: Conductor - User Manual Verification 'Phase 1: Auto-Assigned Nicknames (Backend)' (Protocol in workflow.md)

## Phase 2: Auto-Assigned Nicknames (Frontend) ✅ `9b0a564`

- [x] Task: Write tests for simplified JoinScreen with no name input
- [x] Task: Refactor JoinScreen — remove name input field, show only a "Join Game" button that emits join_game with no name
- [x] Task: Write tests for nickname display banner across all game states
- [x] Task: Add persistent "Your nickname is XXX" banner above the game container in App.jsx, visible in all states
- [x] Task: Update App.jsx handleJoin to receive and store the assigned nickname from the backend response
- [x] Task: Conductor - User Manual Verification 'Phase 2: Auto-Assigned Nicknames (Frontend)' (Protocol in workflow.md)

## Phase 3: Game Restart (Backend) ✅ `6ccc8c5`

- [x] Task: Write tests for restart_game event handler — host-only validation
- [x] Task: Implement restart_game Socket.IO handler — validate requester is host, reject non-host requests
- [x] Task: Write tests for game state reset logic (clear chat, votes, results, turn order, round, remove AI)
- [x] Task: Implement reset_game method in GameManager — clear all game data, remove AI player, reset round to 0, reset eliminated status
- [x] Task: Write tests for nickname re-assignment on restart
- [x] Task: Implement nickname re-randomization — assign new unique nicknames to all players on restart
- [x] Task: Write tests for spectator opt-in tracking (spectator_opt_in event)
- [x] Task: Implement spectator_opt_in Socket.IO handler — track which spectators want to join the next game
- [x] Task: Write tests for opted-in spectators becoming players on restart and non-opted spectators remaining
- [x] Task: Implement spectator-to-player conversion on restart — move opted-in spectators to players dict, keep others as spectators
- [x] Task: Conductor - User Manual Verification 'Phase 3: Game Restart (Backend)' (Protocol in workflow.md)

## Phase 4: Game Restart (Frontend)

- [ ] Task: Write tests for host-only "Play Again" button on ResultScreen
- [ ] Task: Update ResultScreen — show "Play Again" button only to host, show "Waiting for the host to restart..." to others
- [ ] Task: Write tests for spectator opt-in UI on game over
- [ ] Task: Add spectator opt-in prompt to SpectatorView — show "Join" and "Stay Spectating" buttons when game_over is true, emit spectator_opt_in event
- [ ] Task: Write tests for frontend state reset on restart (clear messages, votes, results, turn data, spectator flag)
- [ ] Task: Implement frontend reset — listen for game_update with LOBBY state after restart, clear all local state, update displayed nickname
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Game Restart (Frontend)' (Protocol in workflow.md)
