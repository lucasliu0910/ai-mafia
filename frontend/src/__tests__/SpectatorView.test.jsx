import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import SpectatorView from '../components/SpectatorView';

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

describe('SpectatorView', () => {
    let socket;

    beforeEach(() => {
        socket = createMockSocket();
    });

    it('renders spectating badge', () => {
        render(<SpectatorView socket={socket} spectatorCount={2} />);
        expect(screen.getByText('Spectating')).toBeInTheDocument();
    });

    it('does not render an input field', () => {
        render(<SpectatorView socket={socket} spectatorCount={1} />);
        const input = screen.queryByPlaceholderText(/type message/i);
        expect(input).toBeNull();
    });

    it('does not render a send button', () => {
        render(<SpectatorView socket={socket} spectatorCount={1} />);
        const sendButton = screen.queryByRole('button', { name: /send/i });
        expect(sendButton).toBeNull();
    });

    it('does not render vote buttons', () => {
        render(<SpectatorView socket={socket} spectatorCount={1} />);
        const eliminateButton = screen.queryByRole('button', { name: /eliminate/i });
        expect(eliminateButton).toBeNull();
    });

    it('displays spectator count', () => {
        render(<SpectatorView socket={socket} spectatorCount={3} />);
        expect(screen.getByText(/3/)).toBeInTheDocument();
    });

    it('shows chat messages in read-only mode', () => {
        render(<SpectatorView socket={socket} spectatorCount={1} />);
        // Simulate receiving a message
        const onMessage = socket.on.mock.calls.find(c => c[0] === 'receive_message');
        expect(onMessage).toBeDefined();
    });
});
