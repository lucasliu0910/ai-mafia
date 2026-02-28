import { useState, useEffect } from 'react'
import { io } from 'socket.io-client'

// Use localhost:5000 as defined in app.py
const socket = io('http://localhost:5000')

function App() {
  const [backendStatus, setBackendStatus] = useState('Checking backend...')

  useEffect(() => {
    socket.on('connect', () => {
      console.log('socket connected')
      setBackendStatus('Connected to SocketIO!')
    })
    socket.on('disconnect', () => {
      console.log('socket disconnected')
      setBackendStatus('Disconnected from SocketIO.')
    })

    return () => {
      socket.off('connect')
      socket.off('disconnect')
    }
  }, [])

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 text-slate-100">
      <div className="px-8 py-10 bg-slate-800/80 backdrop-blur-md rounded-2xl shadow-2xl border border-slate-700/50 w-full max-w-md text-center">
        <h1 className="text-5xl font-extrabold bg-gradient-to-br from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent mb-6 drop-shadow-sm">
          AI Mafia
        </h1>
        <div className="bg-slate-900/50 p-4 rounded-xl shadow-inner border border-slate-800">
          <p className="text-slate-400 text-sm font-medium tracking-wide uppercase mb-1">
            System Status
          </p>
          <p className={`font-semibold ${backendStatus.includes('Connected') ? 'text-emerald-400' : 'text-amber-400 animate-pulse'}`}>
            {backendStatus}
          </p>
        </div>
      </div>
    </div>
  )
}

export default App
