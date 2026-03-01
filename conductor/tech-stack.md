# Technology Stack: AI Mafia

## Architecture

Monorepo with two top-level directories: `frontend/` (React SPA) and `backend/` (Flask API server). Communication between client and server is handled via WebSocket (Socket.IO) for real-time game events, with standard HTTP endpoints for health checks.

## Frontend

| Component | Technology | Version |
|---|---|---|
| Language | JavaScript (ES Modules, JSX) | -- |
| Framework | React | ^19.2.0 |
| Build Tool | Vite | ^7.3.1 |
| CSS Framework | Tailwind CSS | ^4.2.1 |
| Real-time Client | Socket.IO Client | ^4.8.3 |
| Linting | ESLint | ^9.39.1 |
| Package Manager | npm | -- |

### Frontend Directory Structure
```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # React components (JoinScreen, LobbyScreen, ChatScreen, VotingScreen, ResultScreen)
│   ├── assets/          # Images and icons
│   ├── App.jsx          # Root component with game state routing
│   ├── App.css          # App-level styles
│   ├── index.css        # Global styles / Tailwind imports
│   └── main.jsx         # Entry point
├── index.html           # HTML template
├── vite.config.js       # Vite configuration
├── eslint.config.js     # ESLint configuration
└── package.json         # Dependencies and scripts
```

### Frontend Commands
- `npm run dev` -- Start development server with HMR
- `npm run build` -- Production build
- `npm run lint` -- Run ESLint
- `npm run preview` -- Preview production build

## Backend

| Component | Technology | Version |
|---|---|---|
| Language | Python | 3.x |
| Framework | Flask | >=3.0.0 |
| Real-time Server | Flask-SocketIO | >=5.3.0 |
| Async Runtime | Eventlet | >=0.35.0 |
| CORS | Flask-CORS | >=4.0.0 |
| AI Integration | OpenAI API (GPT-3.5-turbo) | >=1.12.0 |
| Environment Config | python-dotenv | >=1.0.0 |
| Package Manager | pip | -- |

### Backend Directory Structure
```
backend/
├── app.py               # Flask application, SocketIO event handlers, game orchestration
├── game_manager.py      # Game state machine (LOBBY, CHAT, VOTING, RESULT), player management, voting logic
├── ai_agent.py          # AI player agent using OpenAI API for human-like chat responses
└── requirements.txt     # Python dependencies
```

### Backend Commands
- `pip install -r requirements.txt` -- Install dependencies
- `python app.py` -- Start development server on port 5000

## Communication Protocol

- **WebSocket (Socket.IO):** Primary communication channel for all real-time game events
  - Client events: `join_game`, `start_game`, `send_message`, `submit_vote`
  - Server events: `game_update`, `receive_message`, `timer_update`, `game_result`
- **HTTP:** Health check endpoint (`GET /`)

## Environment Variables

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Flask session secret (default: `ai_mafia_secret`) |
| `OPENAI_API_KEY` | OpenAI API key for AI agent chat generation |
