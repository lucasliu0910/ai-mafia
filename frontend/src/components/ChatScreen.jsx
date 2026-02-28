import React, { useState, useEffect, useRef } from 'react';

export default function ChatScreen({ socket, playerName }) {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [timeLeft, setTimeLeft] = useState(60);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    useEffect(() => {
        const onMessage = (msg) => {
            setMessages((prev) => [...prev, msg]);
        };

        const onTimer = (data) => {
            setTimeLeft(data.time_left);
        };

        socket.on('receive_message', onMessage);
        socket.on('timer_update', onTimer);

        return () => {
            socket.off('receive_message', onMessage);
            socket.off('timer_update', onTimer);
        };
    }, [socket]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (input.trim()) {
            socket.emit('send_message', { text: input.trim() });
            setInput('');
        }
    };

    return (
        <div className="flex flex-col h-[500px] w-full mx-auto bg-slate-900 overflow-hidden">
            {/* Header */}
            <div className="flex items-center justify-between p-4 bg-slate-900 border-b border-slate-700 shadow-sm z-10">
                <h2 className="font-bold text-slate-200">
                    Chat <span className="text-slate-500 font-normal">as {playerName}</span>
                </h2>
                <div className={`px-4 py-1 rounded-full font-bold shadow-sm flex items-center gap-2 ${timeLeft <= 10 ? 'bg-rose-500/20 text-rose-400 animate-pulse border border-rose-500/50' : 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/50'}`}>
                    <span>⏳</span>
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
                        placeholder="Type message..."
                        maxLength={150}
                        className="flex-1 p-3 bg-slate-800 border border-slate-700 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                    />
                    <button
                        type="submit"
                        disabled={!input.trim()}
                        className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 active:scale-95 text-white font-bold rounded-xl transition-all shadow-lg hover:shadow-indigo-500/30 disabled:opacity-50 disabled:active:scale-100"
                    >
                        Send
                    </button>
                </form>
            </div>
        </div>
    );
}
