import { useState, useEffect } from 'react'
import { io } from 'socket.io-client'
import JoinScreen from './components/JoinScreen'
import LobbyScreen from './components/LobbyScreen'
import ChatScreen from './components/ChatScreen'

const socket = io('http://localhost:5000')

function App() {
  const [gameState, setGameState] = useState('LOBBY') // LOBBY, CHAT, VOTING, RESULT
  const [players, setPlayers] = useState([])
  const [joined, setJoined] = useState(false)
  const [playerName, setPlayerName] = useState('')
  const [joinError, setJoinError] = useState('')
  const [backendStatus, setBackendStatus] = useState('Checking backend...')

  useEffect(() => {
    socket.on('connect', () => setBackendStatus('Connected'))
    socket.on('disconnect', () => setBackendStatus('Disconnected'))

    socket.on('game_update', (data) => {
      setGameState(data.state)
      setPlayers(data.players)
    })

    return () => {
      socket.off('connect')
      socket.off('disconnect')
      socket.off('game_update')
    }
  }, [])

  const handleJoin = (name) => {
    socket.emit('join_game', { name }, (response) => {
      if (response && response.success) {
        setJoined(true)
        setPlayerName(name)
        setJoinError('')
      } else {
        setJoinError(response?.message || 'Failed to join')
      }
    })
  }

  const handleStartGame = () => {
    socket.emit('start_game', (response) => {
      if (response && !response.success) {
        alert(response.message)
      }
    })
  }

  // Choose layout based on state so ChatScreen can have more space
  const isChat = gameState === 'CHAT';

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-900 text-slate-100 p-4">
      {/* Background decoration */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-indigo-900/20 blur-[120px] rounded-full mix-blend-screen"></div>
        <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-pink-900/10 blur-[120px] rounded-full mix-blend-screen"></div>
      </div>

      <div className="relative z-10 w-full max-w-lg mb-4 text-center">
        <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold tracking-widest uppercase border ${backendStatus === 'Connected' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border-amber-500/20 animate-pulse'}`}>
          <div className={`w-2 h-2 rounded-full ${backendStatus === 'Connected' ? 'bg-emerald-400' : 'bg-amber-400'}`}></div>
          {backendStatus}
        </div>
      </div>

      <div className={`relative z-10 w-full transition-all duration-500 ${isChat ? 'max-w-xl p-0' : 'max-w-md px-8 py-10'} bg-slate-800/80 backdrop-blur-xl rounded-2xl shadow-2xl border border-slate-700/50 overflow-hidden`}>
        {!joined ? (
          <JoinScreen onJoin={handleJoin} joinError={joinError} />
        ) : gameState === 'LOBBY' ? (
          <LobbyScreen players={players} onStartGame={handleStartGame} />
        ) : gameState === 'CHAT' ? (
          <ChatScreen socket={socket} playerName={playerName} />
        ) : (
          <div className="text-center p-8">
            <h2 className="text-3xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent mb-4">
              Phase: {gameState}
            </h2>
            <p className="text-slate-400">Loading next phase...</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
