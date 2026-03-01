import React, { useState, useEffect, useRef } from 'react';

export default function SpectatorView({ socket, spectatorCount, gameOver }) {
    const [messages, setMessages] = useState([]);
    const [optInChoice, setOptInChoice] = useState(null);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    useEffect(() => {
        const onMessage = (msg) => {
            setMessages((prev) => [...prev, msg]);
        };

        socket.on('receive_message', onMessage);

        return () => {
            socket.off('receive_message', onMessage);
        };
    }, [socket]);

    const handleOptIn = (wantsToJoin) => {
        socket.emit('spectator_opt_in', { opt_in: wantsToJoin }, () => {});
        setOptInChoice(wantsToJoin);
    };

    return (
        <div className="flex flex-col h-[500px] w-full mx-auto bg-slate-900 overflow-hidden">
            {/* Header */}
            <div className="flex items-center justify-between p-4 bg-slate-900 border-b border-slate-700 shadow-sm z-10">
                <div className="flex items-center gap-3">
                    <span className="px-3 py-1 rounded-full text-xs font-black tracking-wider uppercase bg-slate-700/50 text-slate-400 border border-slate-600/50">
                        Spectating
                    </span>
                </div>
                <div className="flex items-center gap-2 text-slate-500 text-sm">
                    <span className="font-semibold">{spectatorCount}</span>
                    <span>watching</span>
                </div>
            </div>

            {/* Messages Area (read-only) */}
            <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-3">
                {messages.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-full text-slate-500 italic text-sm">
                        Watching the game unfold...
                    </div>
                ) : (
                    messages.map((msg, idx) => (
                        <div key={idx} className="flex w-full justify-start">
                            <div className="max-w-[80%] px-4 py-2.5 shadow-sm bg-slate-700 rounded-2xl rounded-tl-none text-slate-100">
                                <p className="text-xs font-bold text-slate-400 mb-0.5">{msg.sender}</p>
                                <p className="whitespace-pre-wrap break-words leading-snug">{msg.text}</p>
                            </div>
                        </div>
                    ))
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Footer */}
            <div className="p-4 bg-slate-900 border-t border-slate-700 text-center">
                {gameOver && optInChoice === null ? (
                    <div className="flex flex-col gap-3">
                        <p className="text-slate-300 text-sm font-semibold">Join the next game?</p>
                        <div className="flex gap-3 justify-center">
                            <button
                                onClick={() => handleOptIn(true)}
                                className="px-6 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl transition-all text-sm"
                            >
                                Join
                            </button>
                            <button
                                onClick={() => handleOptIn(false)}
                                className="px-6 py-2 bg-slate-700 hover:bg-slate-600 text-slate-300 font-bold rounded-xl transition-all text-sm"
                            >
                                Stay Spectating
                            </button>
                        </div>
                    </div>
                ) : gameOver && optInChoice !== null ? (
                    <p className="text-indigo-400 text-sm font-semibold">
                        {optInChoice ? 'Joining next game...' : 'Staying as spectator.'}
                    </p>
                ) : (
                    <p className="text-slate-500 text-sm italic">You are spectating. Chat and voting are disabled.</p>
                )}
            </div>
        </div>
    );
}
