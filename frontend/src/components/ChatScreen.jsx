import React, { useState, useEffect, useRef } from 'react';

export default function ChatScreen({ socket, playerName, currentTurnName, currentTurnSid, myTurn, timeLeft }) {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
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

    const handleSubmit = (e) => {
        e.preventDefault();
        if (input.trim() && myTurn) {
            socket.emit('send_message', { text: input.trim() });
            setInput('');
        }
    };

    const isLowTime = timeLeft <= 10;

    return (
        <div className="flex flex-col h-[500px] w-full mx-auto bg-slate-900 overflow-hidden">
            {/* Header with Turn Indicator */}
            <div className="flex items-center justify-between p-4 bg-slate-900 border-b border-slate-700 shadow-sm z-10">
                <div className="flex flex-col">
                    <h2 className="font-bold text-slate-200">
                        Chat <span className="text-slate-500 font-normal">as {playerName}</span>
                    </h2>
                    <div className="text-sm mt-0.5">
                        {myTurn ? (
                            <span className="text-emerald-400 font-bold animate-pulse">Your turn!</span>
                        ) : (
                            <span className="text-slate-400">
                                Waiting for <span className="font-semibold text-indigo-400">{currentTurnName}</span>
                            </span>
                        )}
                    </div>
                </div>
                <div
                    data-testid="turn-timer"
                    className={`px-4 py-1 rounded-full font-bold shadow-sm flex items-center gap-2 ${isLowTime ? 'bg-rose-500/20 text-rose-400 animate-pulse border border-rose-500/50' : 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/50'}`}
                >
                    00:{timeLeft.toString().padStart(2, '0')}
                </div>
            </div>

            {/* Messages Area */}
            <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-3">
                {messages.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-full text-slate-500 italic text-sm">
                        Say something to start the conversation...
                    </div>
                ) : (
                    messages.map((msg, idx) => {
                        const isMe = msg.sender === playerName;
                        return (
                            <div key={idx} className={`flex w-full ${isMe ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[80%] px-4 py-2.5 shadow-sm ${isMe ? 'bg-indigo-600 rounded-2xl rounded-tr-none text-white' : 'bg-slate-700 rounded-2xl rounded-tl-none text-slate-100'}`}>
                                    {!isMe && <p className="text-xs font-bold text-slate-400 mb-0.5">{msg.sender}</p>}
                                    <p className="whitespace-pre-wrap break-words leading-snug">{msg.text}</p>
                                </div>
                            </div>
                        );
                    })
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-slate-900 border-t border-slate-700">
                <form onSubmit={handleSubmit} className="flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder={myTurn ? "Type message..." : `Waiting for ${currentTurnName}...`}
                        disabled={!myTurn}
                        maxLength={150}
                        className={`flex-1 p-3 bg-slate-800 border border-slate-700 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors ${!myTurn ? 'opacity-50 cursor-not-allowed' : ''}`}
                    />
                    <button
                        type="submit"
                        disabled={!myTurn || !input.trim()}
                        className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 active:scale-95 text-white font-bold rounded-xl transition-all shadow-lg hover:shadow-indigo-500/30 disabled:opacity-50 disabled:active:scale-100"
                    >
                        Send
                    </button>
                </form>
            </div>
        </div>
    );
}
