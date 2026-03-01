"""Tests for game restart system in GameManager."""
import pytest
from game_manager import GameManager, GameState, NICKNAME_POOL


class TestRestartGameHostOnly:
    """Tests for restart_game — host-only validation."""

    def test_only_host_can_restart(self):
        """Only the host should be able to restart the game."""
        gm = GameManager()
        gm.add_player('sid_1')
        gm.add_player('sid_2')
        gm.add_player('sid_3')
        gm.start_game('AI_Agent', requester_sid='sid_1')
        # Force game over state
        gm.state = GameState.RESULT
        success, msg = gm.reset_game(requester_sid='sid_1')
        assert success is True

    def test_non_host_cannot_restart(self):
        """Non-host players should not be able to restart."""
        gm = GameManager()
        gm.add_player('sid_1')
        gm.add_player('sid_2')
        gm.add_player('sid_3')
        gm.start_game('AI_Agent', requester_sid='sid_1')
        gm.state = GameState.RESULT
        success, msg = gm.reset_game(requester_sid='sid_2')
        assert success is False
        assert 'host' in msg.lower()

    def test_restart_requires_result_state(self):
        """Restart should only work in RESULT state."""
        gm = GameManager()
        gm.add_player('sid_1')
        gm.add_player('sid_2')
        gm.add_player('sid_3')
        gm.start_game('AI_Agent', requester_sid='sid_1')
        # State is CHAT, not RESULT
        success, msg = gm.reset_game(requester_sid='sid_1')
        assert success is False


class TestResetGameState:
    """Tests for game state reset logic."""

    def _setup_finished_game(self):
        gm = GameManager()
        gm.add_player('sid_1')
        gm.add_player('sid_2')
        gm.add_player('sid_3')
        gm.start_game('AI_Agent', requester_sid='sid_1')
        gm.chat_history = [{'sender': 'Test', 'text': 'hello'}]
        gm.votes = {'sid_1': 'TestTarget'}
        gm.last_round_result = {'eliminated': 'TestTarget', 'game_over': True}
        gm.round = 3
        gm.state = GameState.RESULT
        return gm

    def test_state_resets_to_lobby(self):
        gm = self._setup_finished_game()
        gm.reset_game(requester_sid='sid_1')
        assert gm.state == GameState.LOBBY

    def test_chat_history_cleared(self):
        gm = self._setup_finished_game()
        gm.reset_game(requester_sid='sid_1')
        assert gm.chat_history == []

    def test_votes_cleared(self):
        gm = self._setup_finished_game()
        gm.reset_game(requester_sid='sid_1')
        assert gm.votes == {}

    def test_last_round_result_cleared(self):
        gm = self._setup_finished_game()
        gm.reset_game(requester_sid='sid_1')
        assert gm.last_round_result == {}

    def test_round_reset_to_zero(self):
        gm = self._setup_finished_game()
        gm.reset_game(requester_sid='sid_1')
        assert gm.round == 0

    def test_turn_order_cleared(self):
        gm = self._setup_finished_game()
        gm.reset_game(requester_sid='sid_1')
        assert gm.turn_order == []
        assert gm.current_turn_index == 0

    def test_ai_player_removed(self):
        gm = self._setup_finished_game()
        assert gm.ai_sid in gm.players
        gm.reset_game(requester_sid='sid_1')
        assert gm.ai_sid not in gm.players

    def test_eliminated_status_reset(self):
        gm = self._setup_finished_game()
        gm.players['sid_2']['eliminated'] = True
        gm.reset_game(requester_sid='sid_1')
        for p in gm.players.values():
            assert p['eliminated'] is False

    def test_host_preserved(self):
        gm = self._setup_finished_game()
        gm.reset_game(requester_sid='sid_1')
        assert gm.host_sid == 'sid_1'
        assert gm.players['sid_1']['is_host'] is True


class TestNicknameReRandomization:
    """Tests for nickname re-assignment on restart."""

    def test_players_get_new_nicknames(self):
        gm = GameManager()
        gm.add_player('sid_1')
        gm.add_player('sid_2')
        gm.add_player('sid_3')
        old_names = {sid: p['name'] for sid, p in gm.players.items()}
        gm.start_game('AI_Agent', requester_sid='sid_1')
        gm.state = GameState.RESULT
        gm.reset_game(requester_sid='sid_1')
        new_names = {sid: p['name'] for sid, p in gm.players.items()}
        # At least some names should change (statistically very unlikely all same)
        # But we can at least verify all names are valid and unique
        assert len(new_names) == len(set(new_names.values()))
        for name in new_names.values():
            assert name in NICKNAME_POOL

    def test_all_nicknames_are_unique_after_restart(self):
        gm = GameManager()
        gm.add_player('sid_1')
        gm.add_player('sid_2')
        gm.add_player('sid_3')
        gm.start_game('AI_Agent', requester_sid='sid_1')
        gm.state = GameState.RESULT
        gm.reset_game(requester_sid='sid_1')
        names = [p['name'] for p in gm.players.values()]
        assert len(names) == len(set(names))


class TestSpectatorOptIn:
    """Tests for spectator opt-in tracking."""

    def test_spectator_can_opt_in(self):
        gm = GameManager()
        gm.add_player('sid_1')
        gm.add_player('sid_2')
        gm.add_player('sid_3')
        gm.start_game('AI_Agent', requester_sid='sid_1')
        gm.add_spectator('sid_late')
        gm.spectator_opt_in('sid_late', True)
        assert gm.spectators['sid_late'].get('opt_in') is True

    def test_spectator_can_opt_out(self):
        gm = GameManager()
        gm.add_player('sid_1')
        gm.add_player('sid_2')
        gm.add_player('sid_3')
        gm.start_game('AI_Agent', requester_sid='sid_1')
        gm.add_spectator('sid_late')
        gm.spectator_opt_in('sid_late', False)
        assert gm.spectators['sid_late'].get('opt_in') is False

    def test_non_spectator_opt_in_ignored(self):
        gm = GameManager()
        gm.add_player('sid_1')
        # Non-spectator should not crash
        result = gm.spectator_opt_in('sid_1', True)
        assert result is False


class TestSpectatorToPlayerOnRestart:
    """Tests for opted-in spectators becoming players on restart."""

    def _setup_game_with_spectators(self):
        gm = GameManager()
        gm.add_player('sid_1')
        gm.add_player('sid_2')
        gm.add_player('sid_3')
        gm.start_game('AI_Agent', requester_sid='sid_1')
        gm.add_spectator('sid_opt_in')
        gm.add_spectator('sid_stay')
        gm.spectator_opt_in('sid_opt_in', True)
        gm.spectator_opt_in('sid_stay', False)
        gm.state = GameState.RESULT
        return gm

    def test_opted_in_spectator_becomes_player(self):
        gm = self._setup_game_with_spectators()
        gm.reset_game(requester_sid='sid_1')
        assert 'sid_opt_in' in gm.players
        assert 'sid_opt_in' not in gm.spectators

    def test_non_opted_spectator_stays_spectator(self):
        gm = self._setup_game_with_spectators()
        gm.reset_game(requester_sid='sid_1')
        assert 'sid_stay' in gm.spectators
        assert 'sid_stay' not in gm.players

    def test_opted_in_spectator_not_host(self):
        gm = self._setup_game_with_spectators()
        gm.reset_game(requester_sid='sid_1')
        assert gm.players['sid_opt_in']['is_host'] is False

    def test_opted_in_spectator_gets_nickname(self):
        gm = self._setup_game_with_spectators()
        gm.reset_game(requester_sid='sid_1')
        assert gm.players['sid_opt_in']['name'] in NICKNAME_POOL

    def test_all_names_unique_after_restart_with_spectators(self):
        gm = self._setup_game_with_spectators()
        gm.reset_game(requester_sid='sid_1')
        all_names = [p['name'] for p in gm.players.values()] + \
                    [s['name'] for s in gm.spectators.values()]
        assert len(all_names) == len(set(all_names))
