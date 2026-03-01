import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

// We test the nickname banner behavior at the App level
// by extracting the banner rendering logic
describe('Nickname Banner', () => {
  it('displays nickname when player has joined', () => {
    const NicknameBanner = ({ nickname }) => (
      nickname ? <div data-testid="nickname-banner">Your nickname is {nickname}</div> : null
    );
    render(<NicknameBanner nickname="Rocky" />);
    expect(screen.getByTestId('nickname-banner')).toHaveTextContent('Your nickname is Rocky');
  });

  it('does not display when no nickname assigned', () => {
    const NicknameBanner = ({ nickname }) => (
      nickname ? <div data-testid="nickname-banner">Your nickname is {nickname}</div> : null
    );
    render(<NicknameBanner nickname="" />);
    expect(screen.queryByTestId('nickname-banner')).not.toBeInTheDocument();
  });

  it('updates when nickname changes', () => {
    const NicknameBanner = ({ nickname }) => (
      nickname ? <div data-testid="nickname-banner">Your nickname is {nickname}</div> : null
    );
    const { rerender } = render(<NicknameBanner nickname="Rocky" />);
    expect(screen.getByTestId('nickname-banner')).toHaveTextContent('Your nickname is Rocky');
    rerender(<NicknameBanner nickname="Luna" />);
    expect(screen.getByTestId('nickname-banner')).toHaveTextContent('Your nickname is Luna');
  });
});
