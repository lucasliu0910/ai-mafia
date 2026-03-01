# Plan: Refactor Game Mechanics to Match Product Specification

## Phase 1: Host System (Backend + Frontend) [checkpoint: 880fddd]

- [x] Task: Write tests for host assignment logic in GameManager 958214d
- [x] Task: Implement host system in GameManager — first player to join becomes host, host transfers on disconnect 5467030
- [x] Task: Write tests for host-only game start permission 2271a9d
- [x] Task: Implement host-only start_game restriction in app.py 89f2653
- [x] Task: Write tests for host indicator in player list data 695f254
- [x] Task: Update get_player_list to include is_host flag and emit host info to clients 95e073e
- [x] Task: Update LobbyScreen component to show host badge and restrict Start Game button to host only 6416a5d
- [x] Task: Conductor - User Manual Verification 'Phase 1: Host System' (Protocol in workflow.md) 880fddd

## Phase 2: Turn-Based Chat System (Backend)

- [x] Task: Write tests for turn order generation in GameManager fd44053
- [x] Task: Implement turn order logic — generate randomized speaking order for each chat round among living players (including AI) fd44053
- [x] Task: Write tests for turn timer and turn advancement fd44053
- [x] Task: Implement turn management — 20-second timer per turn, advance to next player on message or timeout fd44053
- [x] Task: Write tests for message restriction to active turn player fd44053
- [x] Task: Implement send_message restriction — only the active turn player can send a message fd44053
- [x] Task: Write tests for AI turn response generation within turn system fd44053
- [x] Task: Implement AI turn participation — when it is the AI's turn, generate response with simulated typing delay (2-5s) within the 20-second window fd44053
- [x] Task: Write tests for chat phase completion (all turns done → transition to VOTING) fd44053
- [x] Task: Implement chat phase completion — after all living players have had a turn, transition game state to VOTING fd44053
- [x] Task: Conductor - User Manual Verification 'Phase 2: Turn-Based Chat System' (Protocol in workflow.md) df46491

## Phase 3: Turn-Based Chat System (Frontend) [checkpoint: 6a2f708]

- [x] Task: Write tests for ChatScreen turn indicator display 6a2f708
- [x] Task: Refactor ChatScreen component — show active player indicator, 20-second countdown timer, and input field enabled only for the active player 6a2f708
- [x] Task: Write tests for chat input disabled state for non-active players 6a2f708
- [x] Task: Implement chat input restriction — disable text input and send button when it is not the player's turn 6a2f708
- [x] Task: Write tests for turn transition animations and timer display 6a2f708
- [x] Task: Add turn transition UI — animate turn changes, display "Your turn!" prompt, and pulsing timer countdown 6a2f708
- [x] Task: Conductor - User Manual Verification 'Phase 3: Turn-Based Chat System (Frontend)' (Protocol in workflow.md) 6a2f708

## Phase 4: Updated Win Conditions (Backend) [checkpoint: pending]

- [x] Task: Write tests for human win condition (most-voted player is AI)
- [x] Task: Implement human win condition — if the eliminated player is AI, set game_over and human_won
- [x] Task: Write tests for AI win condition (3 players remaining including AI)
- [x] Task: Implement AI win condition — after elimination, if only 3 players remain (including AI), AI wins
- [x] Task: Write tests for tie vote handling
- [x] Task: Implement tie vote resolution — random elimination among tied players
- [x] Task: Remove max_rounds hard limit from GameManager
- [x] Task: Conductor - User Manual Verification 'Phase 4: Updated Win Conditions' (Protocol in workflow.md)

## Phase 5: Spectator Mode (Backend)

- [ ] Task: Write tests for eliminated player spectator transition
- [ ] Task: Implement spectator state for eliminated players — mark as spectator, exclude from turn order and voting
- [ ] Task: Write tests for late joiner spectator assignment
- [ ] Task: Implement late joiner spectator mode — players connecting after game start are assigned spectator role
- [ ] Task: Write tests for spectator message and vote restriction
- [ ] Task: Implement spectator restrictions — spectators cannot send messages or submit votes, but receive all chat and game state events
- [ ] Task: Write tests for spectator count in game state broadcast
- [ ] Task: Update broadcast_game_state to include spectator list and count
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Spectator Mode (Backend)' (Protocol in workflow.md)

## Phase 6: Spectator Mode (Frontend)

- [ ] Task: Write tests for spectator view component rendering
- [ ] Task: Create SpectatorView component — read-only chat display with "Spectating" badge, no input field or vote buttons
- [ ] Task: Write tests for App.jsx spectator routing logic
- [ ] Task: Update App.jsx to route eliminated players and late joiners to SpectatorView
- [ ] Task: Write tests for spectator count display in game UI
- [ ] Task: Add spectator count indicator visible to all players and spectators
- [ ] Task: Conductor - User Manual Verification 'Phase 6: Spectator Mode (Frontend)' (Protocol in workflow.md)
