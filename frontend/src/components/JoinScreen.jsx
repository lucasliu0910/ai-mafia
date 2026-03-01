import React from 'react';

export default function JoinScreen({ onJoin, joinError }) {
    return (
        <div className="flex flex-col items-center w-full max-w-sm mx-auto">
            <h2 className="text-3xl font-bold bg-gradient-to-br from-indigo-400 to-purple-400 bg-clip-text text-transparent mb-6">
                Join the Game
            </h2>
            <div className="w-full flex flex-col gap-4">
                {joinError && (
                    <p className="text-red-400 text-sm font-semibold">{joinError}</p>
                )}
                <button
                    type="button"
                    onClick={() => onJoin()}
                    className="w-full p-4 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl transition-all shadow-lg shadow-indigo-500/30"
                >
                    Join Game
                </button>
            </div>
        </div>
    );
}
