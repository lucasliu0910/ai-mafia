import React, { useState } from 'react';

export default function VotingScreen({ socket, players, playerName }) {
    const [selected, setSelected] = useState(null);
    const [voted, setVoted] = useState(false);

    const livingPlayers = players.filter(p => !p.eliminated);
    const amIEliminated = players.find(p => p.name === playerName)?.eliminated;

    const handleVote = () => {
        if (selected) {
            socket.emit('submit_vote', { target: selected }, (res) => {
                if (res?.success) {
                    setVoted(true);
                } else {
                    alert(res?.message || 'Error voting');
                }
            });
        }
    };

    if (voted) {
        return (
            <div className="flex flex-col items-center justify-center p-8 text-center min-h-[300px]">
                <h2 className="text-3xl font-extrabold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent mb-4 mt-6">
                    Vote Casted
                </h2>
                <div className="w-16 h-16 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin mx-auto mb-4"></div>
                <p className="text-slate-400 font-medium text-lg">Waiting for other players...</p>
            </div>
        );
    }

    if (amIEliminated) {
        return (
            <div className="flex flex-col items-center justify-center p-8 text-center min-h-[300px]">
                <h2 className="text-4xl font-black bg-gradient-to-br from-rose-500 to-orange-500 bg-clip-text text-transparent mb-4">
                    You are eliminated
                </h2>
                <p className="text-slate-400 font-medium text-lg">Watch the remaining players unfold...</p>
            </div>
        );
    }

    return (
        <div className="flex flex-col items-center w-full mx-auto bg-slate-900 overflow-hidden p-2">
            <h2 className="text-4xl font-extrabold bg-gradient-to-br from-rose-400 to-pink-500 bg-clip-text text-transparent mb-2 text-center drop-shadow-lg">
                Who is the AI?
            </h2>
            <p className="text-slate-400 mb-8 font-medium text-center">Cast your vote to eliminate a suspect.</p>

            <div className="flex flex-col gap-3 w-full mb-8 max-h-[300px] overflow-y-auto px-2">
                {livingPlayers.map((p, idx) => {
                    if (p.name === playerName) return null; // Prefer not to vote self
                    return (
                        <button
                            key={idx}
                            onClick={() => setSelected(p.name)}
                            className={`flex items-center gap-4 p-4 rounded-xl border-2 transition-all ${selected === p.name
                                    ? 'border-rose-500 bg-rose-500/10 text-rose-300 transform scale-[1.02] shadow-lg shadow-rose-500/20'
                                    : 'border-slate-700 bg-slate-800 text-slate-200 hover:border-slate-500 hover:bg-slate-750'
                                }`}
                        >
                            <div className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-xl transition-colors ${selected === p.name ? 'bg-rose-500 text-white' : 'bg-slate-700 text-slate-400'}`}>
                                {p.name.charAt(0).toUpperCase()}
                            </div>
                            <span className="font-bold text-xl tracking-wide">{p.name}</span>
                        </button>
                    )
                })}
            </div>

            <button
                onClick={handleVote}
                disabled={!selected}
                className="w-full py-5 rounded-2xl bg-rose-600 hover:bg-rose-500 disabled:opacity-50 disabled:bg-slate-700 disabled:text-slate-500 text-white font-black tracking-widest text-xl shadow-[0_0_20px_rgba(225,29,72,0.4)] disabled:shadow-none transition-all active:scale-95"
            >
                ELIMINATE
            </button>
        </div>
    );
}
