import { useState, useEffect } from 'react'
import { io } from 'socket.io-client'
import JoinScreen from './components/JoinScreen'
import LobbyScreen from './components/LobbyScreen'
import ChatScreen from './components/ChatScreen'
import VotingScreen from './components/VotingScreen'
import ResultScreen from './components/ResultScreen'
import SpectatorView from './components/SpectatorView'

const socket = io(import.meta.env.VITE_BACKEND_URL || '')

function App() {
  const [gameState, setGameState] = useState('LOBBY') // LOBBY, CHAT, VOTING, RESULT
  const [players, setPlayers] = useState([])
  const [joined, setJoined] = useState(false)
  const [playerName, setPlayerName] = useState('')
  const [joinError, setJoinError] = useState('')
  const [backendStatus, setBackendStatus] = useState('Checking backend...')
  const [lastResult, setLastResult] = useState(null)
  const [currentTurnSid, setCurrentTurnSid] = useState(null)
  const [currentTurnName, setCurrentTurnName] = useState('')
  const [timeLeft, setTimeLeft] = useState(20)
  const [isSpectator, setIsSpectator] = useState(false)
  const [spectators, setSpectators] = useState([])

  useEffect(() => {
    socket.on('connect', () => setBackendStatus('Connected'))
    socket.on('disconnect', () => setBackendStatus('Disconnected'))

    socket.on('game_update', (data) => {
      const prevState = gameState
      setGameState(data.state)
      setPlayers(data.players)
      if (data.spectators) setSpectators(data.spectators)
      // Reset local state when returning to LOBBY (restart)
      if (data.state === 'LOBBY') {
        setLastResult(null)
        setCurrentTurnSid(null)
        setCurrentTurnName('')
        setTimeLeft(20)
        // If this client was a spectator who opted in, they're now a player
        const isNowPlayer = data.players.some(p => p.sid === socket.id)
        if (isNowPlayer) {
          setIsSpectator(false)
        }
      }
    })

    socket.on('nickname_update', (nicknameMap) => {
      const myNickname = nicknameMap[socket.id]
      if (myNickname) {
        setPlayerName(myNickname)
      }
    })

    socket.on('game_result', (resultData) => {
      setLastResult(resultData)
    })

    socket.on('turn_update', (data) => {
      setCurrentTurnSid(data.current_turn_sid)
      setCurrentTurnName(data.current_turn_name)
      setTimeLeft(data.time_left)
    })

    socket.on('timer_update', (data) => {
      setTimeLeft(data.time_left)
      setCurrentTurnSid(data.current_turn_sid)
    })

    return () => {
      socket.off('connect')
      socket.off('disconnect')
      socket.off('game_update')
      socket.off('game_result')
      socket.off('turn_update')
      socket.off('timer_update')
      socket.off('nickname_update')
    }
  }, [])

  const handleJoin = () => {
    socket.emit('join_game', {}, (response) => {
      if (response && response.success) {
        setJoined(true)
        setPlayerName(response.nickname || '')
        setJoinError('')
        if (response.spectator) {
          setIsSpectator(true)
        }
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

  const handlePlayAgain = () => {
    socket.emit('restart_game', (response) => {
      if (response && !response.success) {
        alert(response.message)
      }
    })
  }

  const isChat = gameState === 'CHAT';
  const isSpectating = isSpectator || (joined && players.find(p => p.name === playerName)?.eliminated);
  const isHost = joined && players.find(p => p.sid === socket.id)?.is_host;
  const isGameOver = lastResult?.game_over === true;

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-950 text-slate-100 p-4 font-sans">
      {/* Background decoration */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-indigo-900/20 blur-[150px] rounded-full mix-blend-screen transition-all duration-1000"></div>
        <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-rose-900/10 blur-[150px] rounded-full mix-blend-screen transition-all duration-1000"></div>
        {gameState === 'VOTING' && <div className="absolute inset-0 bg-rose-950/20 backdrop-blur-[1px] transition-all duration-1000"></div>}
      </div>

      <div className="relative z-10 w-full max-w-lg mb-6 text-center">
        <div className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-[10px] font-black tracking-[0.2em] uppercase border ${backendStatus === 'Connected' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30 shadow-[0_0_15px_rgba(52,211,153,0.1)]' : 'bg-amber-500/10 text-amber-400 border-amber-500/30 animate-pulse'}`}>
          <div className={`w-2 h-2 rounded-full shadow-sm ${backendStatus === 'Connected' ? 'bg-emerald-400 shadow-emerald-400/50' : 'bg-amber-400'}`}></div>
          {backendStatus}
        </div>
      </div>

      {joined && playerName && (
        <div data-testid="nickname-banner" className="relative z-10 mb-3 px-4 py-2 bg-indigo-500/10 border border-indigo-500/30 rounded-full text-indigo-300 text-sm font-semibold tracking-wide">
          Your nickname is {playerName}
        </div>
      )}

      <div className={`relative z-10 w-full transition-all duration-500 ${isChat || isSpectating ? 'max-w-xl p-0 shadow-[0_0_40px_rgba(0,0,0,0.5)]' : 'max-w-md px-8 py-10 shadow-2xl'} bg-slate-900/80 backdrop-blur-2xl rounded-3xl border border-slate-700/50 overflow-hidden`}>
        {!joined ? (
          <JoinScreen onJoin={handleJoin} joinError={joinError} />
        ) : isSpectating && gameState !== 'LOBBY' ? (
          <SpectatorView socket={socket} spectatorCount={spectators.length} gameOver={isGameOver} />
        ) : gameState === 'LOBBY' ? (
          <LobbyScreen players={players} onStartGame={handleStartGame} playerName={playerName} />
        ) : gameState === 'CHAT' ? (
          <ChatScreen
            socket={socket}
            playerName={playerName}
            currentTurnName={currentTurnName}
            currentTurnSid={currentTurnSid}
            myTurn={socket.id === currentTurnSid}
            timeLeft={timeLeft}
          />
        ) : gameState === 'VOTING' ? (
          <VotingScreen socket={socket} players={players} playerName={playerName} />
        ) : gameState === 'RESULT' ? (
          <ResultScreen result={lastResult} isHost={isHost} onPlayAgain={handlePlayAgain} />
        ) : (
          <div className="text-center p-8">
            <h2 className="text-3xl font-bold text-slate-300 animate-pulse">
              Loading...
            </h2>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
