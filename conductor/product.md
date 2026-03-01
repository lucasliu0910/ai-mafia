# Product Guide: AI Mafia

## Overview

AI Mafia is a real-time, browser-based social deduction game where human players chat alongside a hidden AI agent. The twist on the classic Mafia/Werewolf formula is that instead of a human secretly playing the "mafia" role, an AI tries to pass as a human in live conversation -- creating a Turing-test-like experience. Players must identify and vote out the AI before it survives all rounds.

## Target Users

Casual gamers who enjoy quick, browser-based party games with friends, similar to Jackbox, Among Us, or online Mafia/Werewolf variants. No downloads or accounts required -- just open a browser and play.

## Core Value Proposition

The AI is the hidden player. Unlike traditional social deduction games where a human pretends to be part of the group, AI Mafia pits real people against an AI that must convincingly mimic human conversation. Every round is a live Turing test -- can the group spot the machine?

## Key Features

### Auto-Assigned Nicknames
Players do not enter their own name. When a player joins the game, the system automatically assigns a random, common English nickname (e.g., "Sunny", "Rocky", "Pepper", "Clover"). Each nickname is unique within the current session. The player's assigned nickname is displayed prominently at the top of the screen at all times ("Your nickname is XXX"). Nicknames are re-randomized for all players (including the AI) whenever a new game starts.

### Turn-Based Chat with AI Deception
The chat phase is structured and turn-based. The system selects which player speaks next, and that player has 20 seconds to type a response before the turn passes. The AI takes its turns just like any other player, attempting to blend in naturally. This turn-based structure ensures every player participates and prevents dominant personalities from controlling the conversation.

### Democratic Voting & Elimination
After each chat round, all players -- including the AI -- vote on who they believe is the AI. The player with the most votes is eliminated. The AI also participates in voting, adding another layer of deception as it tries to deflect suspicion onto human players.

### Multiple Rounds with Escalating Tension
The game plays over multiple rounds. Each round, the most-voted player is eliminated, narrowing the field and raising the stakes.

### Win Conditions
- **Humans win:** If the player with the most votes in a round is the AI, the AI is eliminated and humans win immediately.
- **AI wins:** If only 3 players remain (including the AI), the AI wins. The AI has successfully blended in long enough to survive.

### Host System
The first player to join the game automatically becomes the host. The host has the ability to start the game and restart the game after it ends. The host also participates as a regular player in the game itself.

### Game Replay
When a game ends (human or AI wins), only the host can press "Play Again" to restart. Non-host players see "Waiting for the host to restart..." on the Result screen. On restart, the game resets to a clean lobby state: all game data is cleared, all players receive new random nicknames, and the host remains the host. The AI player is removed and will receive a new name when the next game starts.

### Spectator Mode
- **Eliminated players** become spectators after being voted out. They can continue watching the chat room content but cannot participate in subsequent conversations or votes.
- **Late joiners** who arrive after the game has already started also become spectators. They can see the chat room dialogue in real-time but cannot participate in the game.
- **Spectator opt-in on restart:** When a game ends, spectators are presented with a choice to "Join" the next game or "Stay Spectating". Spectators who opt in become regular players in the lobby when the host restarts. Spectators who decline (or make no choice) remain as spectators in the next game.

## Platform

Web-only application, fully responsive across desktop and mobile browsers. No app installation required -- players join via a shared link or room code in any modern browser.

## Game Session Size

3-6 human players per game session, plus the hidden AI agent. This small group size keeps rounds tight, ensures meaningful social deduction, and allows every player's messages to be scrutinized.

## Game Flow

1. **Join** -- Players press "Join Game" (no name input). The system assigns a random nickname and displays it at the top of the screen.
2. **Lobby** -- Players wait in the lobby (first player becomes host). The host starts the game when ready.
3. **Chat Phase** -- Turn-based conversation where the system assigns speaking order. Each player (including AI) has 20 seconds per turn.
4. **Voting Phase** -- All living players (including AI) vote on who they think is the AI.
5. **Result Phase** -- The most-voted player is eliminated. If the AI is caught, humans win. If a human is eliminated, they become a spectator.
6. **Next Round or Game Over** -- If only 3 players remain (including AI), the AI wins. Otherwise, the game loops back to the chat phase for the next round.
7. **Game Over** -- The host can press "Play Again" to restart. Spectators choose whether to join the next game. All players receive new nicknames on restart.
8. **Spectators** -- Eliminated players and late joiners watch the game unfold in real-time.
