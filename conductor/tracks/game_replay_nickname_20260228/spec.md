# Spec: Game Replay & Auto-Nickname System

## Overview

Two related changes: (1) The game currently has no way to restart after it ends. This track adds a "Play Again" flow where the host can reset the game, returning everyone to the lobby. (2) Players no longer enter their own name — the system automatically assigns a random, common English nickname to each player on join, and re-assigns new nicknames on every restart.

## Functional Requirements

### FR-1: Auto-Assigned Nicknames
- Remove the name input field from the JoinScreen.
- When a player connects and joins, the backend automatically assigns a random, common English nickname (e.g., "Sunny", "Rocky", "Pepper", "Clover", "Blaze", etc.).
- The assigned nickname must be unique among all current players and spectators.
- Maintain a predefined list of ~30+ common, fun English nicknames in the backend.

### FR-2: Display Nickname on Screen
- Show "Your nickname is **XXX**" prominently at the top of the screen (above the game container), visible at all times across all game states (lobby, chat, voting, result, spectator).

### FR-3: Re-Assign Nicknames on Restart
- When the game restarts, **all** players (including the AI when it joins in the next game) receive new, freshly randomized nicknames.
- The previous nicknames are fully discarded.

### FR-4: Host-Only "Play Again" Button
- On the Result screen, when `game_over` is `true`, display a "Play Again" button **only to the current host**.
- Non-host players see a message like "Waiting for the host to restart..."

### FR-5: Spectator Opt-In Before Restart
- When the game ends (`game_over` is `true`), spectators see a prompt: "Join next game?" with **"Join"** and **"Stay Spectating"** buttons.
- Spectators who choose "Join" are flagged as ready to rejoin. When the host restarts, these spectators are moved into the `players` dict as regular players.
- Spectators who choose "Stay Spectating" (or make no choice) remain as spectators in the next game.
- The backend tracks each spectator's opt-in choice via a `spectator_opt_in` Socket.IO event.

### FR-6: Game Reset (Backend)
- When the host triggers a restart via a `restart_game` Socket.IO event, the backend must:
  - Transition game state back to `LOBBY`
  - Clear all game data: `chat_history`, `votes`, `last_round_result`, `turn_order`, `current_turn_index`
  - Reset `round` to `0`
  - Remove the AI player from the `players` dict
  - Reset all players' `eliminated` status to `False`
  - Move only **opted-in spectators** into the `players` dict as regular players
  - Keep remaining spectators in the `spectators` dict
  - Preserve the current host assignment (the host remains the host)
  - Re-assign new random nicknames to all players

### FR-7: Frontend State Reset
- All clients receive a `game_update` with state `LOBBY` and the updated player list (with new nicknames)
- Frontend must reset local state: messages, votes, results, turn data, spectator flag (if opted in)
- Frontend must update the displayed nickname to the newly assigned one

### FR-8: Simplified Join Flow
- The JoinScreen is replaced with a single "Join Game" button (no name input).
- On click, the client emits `join_game` with no name. The backend responds with the assigned nickname.

## Acceptance Criteria

- [ ] JoinScreen has no name input — only a "Join Game" button
- [ ] Backend assigns a unique random English nickname on join
- [ ] "Your nickname is XXX" is displayed at the top of the screen at all times
- [ ] Only the host sees the "Play Again" button on the Result screen
- [ ] Non-host players see "Waiting for the host to restart..."
- [ ] Spectators see "Join next game?" prompt with Join / Stay Spectating buttons when game is over
- [ ] Opted-in spectators become regular players in the lobby on restart
- [ ] Non-opted spectators remain as spectators
- [ ] All players receive new random nicknames on restart
- [ ] Host remains the host after restart
- [ ] Chat history, votes, and results are fully cleared
- [ ] AI player is removed and gets a new name when the next game starts

## Out of Scope

- Allowing players to choose or customize their nickname
- Changing the host on restart (host stays the same)
- Persisting any game history or stats between games
- Automatic restart timer
