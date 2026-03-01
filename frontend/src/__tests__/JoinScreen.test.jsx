import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import JoinScreen from '../components/JoinScreen';

describe('JoinScreen', () => {
  it('renders a Join Game button', () => {
    render(<JoinScreen onJoin={() => {}} />);
    expect(screen.getByRole('button', { name: /join game/i })).toBeInTheDocument();
  });

  it('does not render a name input field', () => {
    render(<JoinScreen onJoin={() => {}} />);
    expect(screen.queryByPlaceholderText(/enter your name/i)).not.toBeInTheDocument();
    expect(screen.queryByRole('textbox')).not.toBeInTheDocument();
  });

  it('calls onJoin with no arguments when button is clicked', () => {
    const onJoin = vi.fn();
    render(<JoinScreen onJoin={onJoin} />);
    fireEvent.click(screen.getByRole('button', { name: /join game/i }));
    expect(onJoin).toHaveBeenCalledTimes(1);
    expect(onJoin).toHaveBeenCalledWith();
  });

  it('displays join error when provided', () => {
    render(<JoinScreen onJoin={() => {}} joinError="Server full" />);
    expect(screen.getByText('Server full')).toBeInTheDocument();
  });

  it('button is always enabled (no name validation needed)', () => {
    render(<JoinScreen onJoin={() => {}} />);
    expect(screen.getByRole('button', { name: /join game/i })).not.toBeDisabled();
  });
});
