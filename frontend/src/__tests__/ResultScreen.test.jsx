import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import ResultScreen from '../components/ResultScreen';

describe('ResultScreen - Play Again button', () => {
  const gameOverResult = {
    eliminated: 'TestBot',
    ai_won: false,
    human_won: true,
    game_over: true,
    votes: { TestBot: 3 },
  };

  it('shows Play Again button to the host', () => {
    render(<ResultScreen result={gameOverResult} isHost={true} onPlayAgain={() => {}} />);
    expect(screen.getByRole('button', { name: /play again/i })).toBeInTheDocument();
  });

  it('does not show Play Again button to non-host', () => {
    render(<ResultScreen result={gameOverResult} isHost={false} onPlayAgain={() => {}} />);
    expect(screen.queryByRole('button', { name: /play again/i })).not.toBeInTheDocument();
  });

  it('shows waiting message to non-host', () => {
    render(<ResultScreen result={gameOverResult} isHost={false} onPlayAgain={() => {}} />);
    expect(screen.getByText(/waiting for the host to restart/i)).toBeInTheDocument();
  });

  it('calls onPlayAgain when host clicks Play Again', () => {
    const onPlayAgain = vi.fn();
    render(<ResultScreen result={gameOverResult} isHost={true} onPlayAgain={onPlayAgain} />);
    fireEvent.click(screen.getByRole('button', { name: /play again/i }));
    expect(onPlayAgain).toHaveBeenCalledTimes(1);
  });

  it('does not show Play Again or waiting when game is not over', () => {
    const midGameResult = {
      eliminated: 'Someone',
      ai_won: false,
      human_won: false,
      game_over: false,
      votes: { Someone: 2 },
    };
    render(<ResultScreen result={midGameResult} isHost={true} onPlayAgain={() => {}} />);
    expect(screen.queryByRole('button', { name: /play again/i })).not.toBeInTheDocument();
    expect(screen.queryByText(/waiting for the host to restart/i)).not.toBeInTheDocument();
  });
});
