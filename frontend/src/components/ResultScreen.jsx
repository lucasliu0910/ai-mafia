import React, { useEffect, useState } from 'react';

export default function ResultScreen({ result }) {
    const [countdown, setCountdown] = useState(8);

    useEffect(() => {
        let timer;
        if (result && !result.game_over) {
            timer = setInterval(() => {
                setCountdown((c) => (c > 0 ? c - 1 : 0));
            }, 1000);
        }
        return () => clearInterval(timer);
    }, [result]);

    if (!result) {
        return (
            <div className="flex flex-col items-center justify-center p-8 text-center min-h-[300px]">
                <div className="w-16 h-16 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin mx-auto mb-4"></div>
                <p className="text-slate-400 font-medium text-lg">Calculating results...</p>
            </div>
        );
    }

    const { eliminated, ai_won, human_won, game_over } = result;

    return (
        <div className="flex flex-col items-center w-full mx-auto p-4 max-w-lg text-center">
            <h2 className="text-4xl font-black bg-gradient-to-br from-amber-400 to-orange-500 bg-clip-text text-transparent mb-8 drop-shadow-md uppercase tracking-wider">
                Round Result
            </h2>

            {eliminated ? (
                <div className="mb-6 p-6 bg-slate-900/80 border border-rose-900/50 rounded-[2rem] w-full shadow-inner relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-t from-rose-500/5 to-transparent z-0"></div>
                    <p className="text-rose-500 text-sm font-bold uppercase tracking-[0.2em] mb-3 relative z-10">
                        Eliminated Player
                    </p>
                    <p className="text-4xl font-black text-slate-100 relative z-10 tracking-wide">{eliminated}</p>
                </div>
            ) : (
                <div className="mb-6 p-6 bg-slate-900/80 border border-slate-700/50 rounded-[2rem] w-full">
                    <p className="text-xl font-bold text-slate-400">No decisive votes. Everyone survives.</p>
                </div>
            )}

            {game_over ? (
                <div className={`mt-2 p-8 w-full rounded-[2rem] border-2 shadow-2xl relative overflow-hidden ${human_won ? 'bg-emerald-950/40 border-emerald-500/40' : 'bg-rose-950/40 border-rose-500/40'}`}>
                    <div className={`absolute top-0 left-0 w-full h-1 ${human_won ? 'bg-emerald-500' : 'bg-rose-500'}`}></div>
                    <h3 className={`text-5xl font-black mb-4 drop-shadow-md tracking-tight ${human_won ? 'text-emerald-400' : 'text-rose-500'}`}>
                        {human_won ? 'HUMANS WIN' : 'AI WINS'}
                    </h3>
                    <p className="text-slate-300 font-medium text-lg leading-relaxed mb-8">
                        {human_won
                            ? `You successfully eliminated the AI! Great job.`
                            : `The AI survived and infiltrated your group.`}
                    </p>
                    <button
                        onClick={() => window.location.reload()}
                        className="px-10 py-4 bg-slate-800 hover:bg-slate-700 text-white font-black uppercase tracking-widest text-sm rounded-2xl transition-all shadow-[0_0_20px_rgba(0,0,0,0.5)] active:scale-95 border border-slate-600/50"
                    >
                        Play Again
                    </button>
                </div>
            ) : (
                <div className="mt-8 flex flex-col items-center">
                    <div className="w-12 h-1 bg-slate-700 rounded-full mb-8"></div>
                    <p className="text-2xl font-bold text-slate-300 mb-3">The game continues...</p>
                    <div className="flex items-baseline gap-2 text-slate-500">
                        <span className="text-sm font-bold uppercase tracking-wider">Next round in</span>
                        <span className="text-2xl font-black text-indigo-400 font-mono">{countdown}s</span>
                    </div>
                </div>
            )}
        </div>
    );
}
