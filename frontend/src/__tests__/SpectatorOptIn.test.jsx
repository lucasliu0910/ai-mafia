import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import SpectatorView from '../components/SpectatorView';

const mockSocket = {
  on: vi.fn(),
  off: vi.fn(),
  emit: vi.fn(),
};

describe('SpectatorView - Opt-in UI', () => {
  it('shows opt-in buttons when game is over', () => {
    render(<SpectatorView socket={mockSocket} spectatorCount={2} gameOver={true} />);
    expect(screen.getByRole('button', { name: /^join$/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /stay spectating/i })).toBeInTheDocument();
  });

  it('does not show opt-in buttons when game is not over', () => {
    render(<SpectatorView socket={mockSocket} spectatorCount={2} gameOver={false} />);
    expect(screen.queryByRole('button', { name: /^join$/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /stay spectating/i })).not.toBeInTheDocument();
  });

  it('emits spectator_opt_in with true when Join is clicked', () => {
    mockSocket.emit.mockClear();
    render(<SpectatorView socket={mockSocket} spectatorCount={2} gameOver={true} />);
    fireEvent.click(screen.getByRole('button', { name: /^join$/i }));
    expect(mockSocket.emit).toHaveBeenCalledWith('spectator_opt_in', { opt_in: true }, expect.any(Function));
  });

  it('emits spectator_opt_in with false when Stay Spectating is clicked', () => {
    mockSocket.emit.mockClear();
    render(<SpectatorView socket={mockSocket} spectatorCount={2} gameOver={true} />);
    fireEvent.click(screen.getByRole('button', { name: /stay spectating/i }));
    expect(mockSocket.emit).toHaveBeenCalledWith('spectator_opt_in', { opt_in: false }, expect.any(Function));
  });

  it('shows confirmation after opting in', () => {
    render(<SpectatorView socket={mockSocket} spectatorCount={2} gameOver={true} />);
    fireEvent.click(screen.getByRole('button', { name: /^join$/i }));
    expect(screen.getByText(/joining next game/i)).toBeInTheDocument();
  });
});
