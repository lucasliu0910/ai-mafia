import React, { useState } from 'react';

export default function JoinScreen({ onJoin, joinError }) {
    const [name, setName] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (name.trim()) {
            onJoin(name.trim());
        }
    };

    return (
        <div className="flex flex-col items-center w-full max-w-sm mx-auto">
            <h2 className="text-3xl font-bold bg-gradient-to-br from-indigo-400 to-purple-400 bg-clip-text text-transparent mb-6">
                Join the Game
            </h2>
            <form onSubmit={handleSubmit} className="w-full flex flex-col gap-4">
                <div>
                    <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Enter your name"
                        maxLength={15}
                        autoFocus
                        className="w-full p-4 bg-slate-900 border border-slate-700 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all font-medium tracking-wide"
                    />
                </div>
                {joinError && (
                    <p className="text-red-400 text-sm font-semibold">{joinError}</p>
                )}
                <button
                    type="submit"
                    disabled={!name.trim()}
                    className="w-full p-4 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl transition-all shadow-lg shadow-indigo-500/30 disabled:opacity-50 disabled:shadow-none"
                >
                    Join Lobby
                </button>
            </form>
        </div>
    );
}
