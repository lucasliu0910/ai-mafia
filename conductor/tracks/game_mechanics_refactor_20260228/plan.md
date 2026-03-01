# Plan: Refactor Game Mechanics to Match Product Specification

## Phase 1: Host System (Backend + Frontend)

- [x] Task: Write tests for host assignment logic in GameManager 958214d
- [x] Task: Implement host system in GameManager — first player to join becomes host, host transfers on disconnect 5467030
- [ ] Task: Write tests for host-only game start permission
- [ ] Task: Implement host-only start_game restriction in app.py
- [ ] Task: Write tests for host indicator in player list data
- [ ] Task: Update get_player_list to include is_host flag and emit host info to clients
- [ ] Task: Update LobbyScreen component to show host badge and restrict Start Game button to host only
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Host System' (Protocol in workflow.md)

## Phase 2: Turn-Based Chat System (Backend)

- [ ] Task: Write tests for turn order generation in GameManager
- [ ] Task: Implement turn order logic — generate randomized speaking order for each chat round among living players (including AI)
- [ ] Task: Write tests for turn timer and turn advancement
- [ ] Task: Implement turn management — 20-second timer per turn, advance to next player on message or timeout
- [ ] Task: Write tests for message restriction to active turn player
- [ ] Task: Implement send_message restriction — only the active turn player can send a message
- [ ] Task: Write tests for AI turn response generation within turn system
- [ ] Task: Implement AI turn participation — when it is the AI's turn, generate response with simulated typing delay (2-5s) within the 20-second window
- [ ] Task: Write tests for chat phase completion (all turns done → transition to VOTING)
- [ ] Task: Implement chat phase completion — after all living players have had a turn, transition game state to VOTING
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Turn-Based Chat System' (Protocol in workflow.md)

## Phase 3: Turn-Based Chat System (Frontend)

- [ ] Task: Write tests for ChatScreen turn indicator display
- [ ] Task: Refactor ChatScreen component — show active player indicator, 20-second countdown timer, and input field enabled only for the active player
- [ ] Task: Write tests for chat input disabled state for non-active players
- [ ] Task: Implement chat input restriction — disable text input and send button when it is not the player's turn
- [ ] Task: Write tests for turn transition animations and timer display
- [ ] Task: Add turn transition UI — animate turn changes, display "Your turn!" prompt, and pulsing timer countdown
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Turn-Based Chat System (Frontend)' (Protocol in workflow.md)

## Phase 4: Updated Win Conditions (Backend)

- [ ] Task: Write tests for human win condition (most-voted player is AI)
- [ ] Task: Implement human win condition — if the eliminated player is AI, set game_over and human_won
- [ ] Task: Write tests for AI win condition (3 players remaining including AI)
- [ ] Task: Implement AI win condition — after elimination, if only 3 players remain (including AI), AI wins
- [ ] Task: Write tests for tie vote handling
- [ ] Task: Implement tie vote resolution — random elimination among tied players
- [ ] Task: Remove max_rounds hard limit from GameManager
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Updated Win Conditions' (Protocol in workflow.md)

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
