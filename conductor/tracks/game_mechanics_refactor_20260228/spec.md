# Specification: Refactor Game Mechanics to Match Product Specification

## Overview

This track aligns the existing AI Mafia codebase with the product specification defined in `conductor/product.md`. The current implementation uses free-form chat, round-limit-based win conditions, and has no host or spectator system. This track refactors both the backend game logic and frontend components to implement turn-based chat, correct win conditions, host assignment, and spectator mode.

## Current State

### What Exists
- **Free-form chat:** All players can type at any time during a 60-second timer
- **Round-limit win condition:** AI wins after 3 rounds; humans win by voting out AI
- **No host system:** Any player can start the game
- **No spectator mode:** No support for eliminated players watching or late joiners
- **AI responds reactively:** AI replies when mentioned or randomly (30% chance)

### What Needs to Change
1. Chat phase → turn-based (system assigns speaking order, 20s per turn)
2. Win condition → AI wins when only 3 players remain (including AI)
3. Host system → first player to join becomes host
4. Spectator mode → eliminated players and late joiners can watch chat but not participate
5. AI participates in the turn-based system like any other player

## Functional Requirements

### FR-1: Turn-Based Chat System
- The system randomly or sequentially assigns a speaking order for each chat round
- Only the active player can send a message during their turn
- Each player has 20 seconds to type and send a response
- If the timer expires without a message, the turn passes to the next player
- The AI takes turns like any other player, generating a response within the time window
- All players (and spectators) can see messages in real-time as they are sent
- After all living players have had a turn, the chat phase ends and voting begins

### FR-2: Updated Win Conditions
- **Humans win:** The player with the most votes in a round is the AI → game ends immediately
- **AI wins:** Only 3 players remain (including the AI) → game ends immediately
- Remove the previous `max_rounds = 3` hard limit
- Handle tie votes (e.g., random elimination among tied players, or no elimination)

### FR-3: Host System
- The first player to join the lobby automatically becomes the host
- The host is visually indicated in the lobby UI
- Only the host can trigger the "Start Game" action
- The host also participates as a regular player in the game
- If the host disconnects during the lobby phase, the next player in join order becomes host

### FR-4: Spectator Mode
- **Eliminated players:** After being voted out, a player's UI transitions to spectator view — they can see the chat messages but cannot send messages or vote
- **Late joiners:** Players who connect after the game has started enter directly into spectator view
- Spectators see a read-only version of the chat and game state
- Spectators are visually distinguished from active players (e.g., a "Spectating" badge)
- Spectator count is visible to all players

### FR-5: AI Turn Participation
- The AI is included in the turn order like any other player
- When it is the AI's turn, the backend generates a response via OpenAI and sends it within the 20-second window
- The AI's turn should include a brief simulated "typing" delay (2-5 seconds) to appear human

## Non-Functional Requirements

- **NFR-1:** Turn transitions must feel responsive (< 500ms latency for turn change events)
- **NFR-2:** The spectator view must not leak information about which player is the AI
- **NFR-3:** All new backend logic must have >80% test coverage
- **NFR-4:** All new frontend components must be responsive (mobile-first)
- **NFR-5:** WebSocket events must be well-documented for future extensibility

## Out of Scope

- Room/lobby codes (multiple game rooms)
- User accounts or authentication
- Persistent game history or leaderboards
- Chat moderation or content filtering
- Changing the AI model (stays on GPT-3.5-turbo)
