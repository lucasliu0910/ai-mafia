import React from 'react';

export default function LobbyScreen({ players, onStartGame, playerName }) {
    const currentPlayer = players.find((p) => p.name === playerName);
    const isHost = currentPlayer?.is_host === true;

    return (
        <div className="flex flex-col items-center w-full max-w-md mx-auto">
            <h2 className="text-3xl font-bold bg-gradient-to-br from-indigo-400 to-purple-400 bg-clip-text text-transparent mb-6">
                Lobby
            </h2>

            <div className="w-full bg-slate-900 border border-slate-800 rounded-xl p-4 mb-6 min-h-[150px] shadow-inner">
                <h3 className="text-sm uppercase tracking-wider text-slate-500 font-bold mb-3 flex justify-between">
                    <span>Players</span>
                    <span>{players.length} / 6</span>
                </h3>
                <ul className="flex flex-col gap-2">
                    {players.length === 0 && (
                        <li className="text-slate-500 text-center py-4 italic text-sm">Waiting for players...</li>
                    )}
                    {players.map((p, i) => (
                        <li key={i} className="flex items-center gap-3 p-2 rounded-lg bg-slate-800/50 hover:bg-slate-800 transition-colors">
                            <div className="w-8 h-8 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold shadow-sm">
                                {p.name.charAt(0).toUpperCase()}
                            </div>
                            <span className="font-semibold text-slate-200">{p.name}</span>
                            {p.is_host && (
                                <span className="ml-auto text-[10px] font-black tracking-wider uppercase px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30">
                                    Host
                                </span>
                            )}
                        </li>
                    ))}
                </ul>
            </div>

            {isHost ? (
                <button
                    onClick={onStartGame}
                    disabled={players.length < 3}
                    className="w-full p-4 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl transition-all shadow-lg shadow-emerald-500/30 disabled:bg-slate-700 disabled:text-slate-500 disabled:shadow-none"
                >
                    {players.length < 3 ? `Need ${3 - players.length} more player${3 - players.length === 1 ? '' : 's'}` : 'Start Game'}
                </button>
            ) : (
                <div className="w-full p-4 text-center text-slate-400 text-sm italic">
                    Waiting for the host to start the game...
                </div>
            )}
        </div>
    );
}
