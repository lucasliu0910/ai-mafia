import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import ChatScreen from '../components/ChatScreen';

function createMockSocket() {
    const listeners = {};
    return {
        on: vi.fn((event, cb) => {
            if (!listeners[event]) listeners[event] = [];
            listeners[event].push(cb);
        }),
        off: vi.fn((event, cb) => {
            if (listeners[event]) {
                listeners[event] = listeners[event].filter(fn => fn !== cb);
            }
        }),
        emit: vi.fn(),
        _emit: (event, data) => {
            (listeners[event] || []).forEach(cb => cb(data));
        },
    };
}

describe('ChatScreen Turn Indicator', () => {
    let socket;

    beforeEach(() => {
        socket = createMockSocket();
    });

    it('shows active player name in turn indicator', () => {
        render(
            <ChatScreen
                socket={socket}
                playerName="Alice"
                currentTurnName="Bob"
                currentTurnSid="sid_2"
                myTurn={false}
                timeLeft={20}
            />
        );
        expect(screen.getByText(/Bob/)).toBeInTheDocument();
    });

    it('shows "Your turn!" when it is the player\'s turn', () => {
        render(
            <ChatScreen
                socket={socket}
                playerName="Alice"
                currentTurnName="Alice"
                currentTurnSid="sid_1"
                myTurn={true}
                timeLeft={20}
            />
        );
        expect(screen.getByText(/Your turn/i)).toBeInTheDocument();
    });

    it('shows countdown timer', () => {
        render(
            <ChatScreen
                socket={socket}
                playerName="Alice"
                currentTurnName="Bob"
                currentTurnSid="sid_2"
                myTurn={false}
                timeLeft={15}
            />
        );
        expect(screen.getByText(/15/)).toBeInTheDocument();
    });

    it('disables input when it is not the player\'s turn', () => {
        render(
            <ChatScreen
                socket={socket}
                playerName="Alice"
                currentTurnName="Bob"
                currentTurnSid="sid_2"
                myTurn={false}
                timeLeft={20}
            />
        );
        const input = screen.getByPlaceholderText(/waiting/i);
        expect(input).toBeDisabled();
    });

    it('enables input when it is the player\'s turn', () => {
        render(
            <ChatScreen
                socket={socket}
                playerName="Alice"
                currentTurnName="Alice"
                currentTurnSid="sid_1"
                myTurn={true}
                timeLeft={20}
            />
        );
        const input = screen.getByPlaceholderText(/type message/i);
        expect(input).not.toBeDisabled();
    });

    it('disables send button when it is not the player\'s turn', () => {
        render(
            <ChatScreen
                socket={socket}
                playerName="Alice"
                currentTurnName="Bob"
                currentTurnSid="sid_2"
                myTurn={false}
                timeLeft={20}
            />
        );
        const sendButton = screen.getByRole('button', { name: /send/i });
        expect(sendButton).toBeDisabled();
    });

    it('shows timer with warning style when time is low', () => {
        render(
            <ChatScreen
                socket={socket}
                playerName="Alice"
                currentTurnName="Bob"
                currentTurnSid="sid_2"
                myTurn={false}
                timeLeft={5}
            />
        );
        const timerEl = screen.getByTestId('turn-timer');
        expect(timerEl.className).toMatch(/rose/);
    });
});
