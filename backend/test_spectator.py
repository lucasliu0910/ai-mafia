"""Tests for spectator mode in GameManager."""
import pytest
from game_manager import GameManager, GameState


@pytest.fixture
def gm_in_game():
    """Create a GameManager with 4 players + AI in CHAT state."""
    gm = GameManager()
    gm.add_player('sid_1', 'Alice')
    gm.add_player('sid_2', 'Bob')
    gm.add_player('sid_3', 'Charlie')
    gm.add_player('sid_4', 'Dave')
    gm.start_game('AI_Agent', requester_sid='sid_1')
    return gm


class TestEliminatedPlayerSpectator:
    """Tests for eliminated players becoming spectators."""

    def test_eliminated_player_marked_as_spectator(self, gm_in_game):
        """An eliminated player should be marked as a spectator."""
        gm_in_game.players['sid_2']['eliminated'] = True
        gm_in_game.players['sid_2']['spectator'] = True
        assert gm_in_game.players['sid_2'].get('spectator') is True

    def test_eliminated_player_excluded_from_turn_order(self, gm_in_game):
        """An eliminated player should not appear in turn order."""
        gm_in_game.players['sid_2']['eliminated'] = True
        gm_in_game._generate_turn_order()
        assert 'sid_2' not in gm_in_game.turn_order

    def test_eliminated_player_cannot_vote(self, gm_in_game):
        """An eliminated player should not be able to vote."""
        gm_in_game.players['sid_2']['eliminated'] = True
        gm_in_game.state = GameState.VOTING
        success, msg = gm_in_game.submit_vote('sid_2', 'Alice')
        assert success is False
        assert 'eliminated' in msg.lower()


class TestLateJoinerSpectator:
    """Tests for late joiners becoming spectators."""

    def test_late_joiner_rejected_during_game(self, gm_in_game):
        """A player joining after game start should be rejected by add_player."""
        success, msg = gm_in_game.add_player('sid_late', 'LateGuy')
        assert success is False

    def test_add_spectator_during_game(self, gm_in_game):
        """add_spectator should allow joining as spectator during active game."""
        success, msg = gm_in_game.add_spectator('sid_late', 'LateGuy')
        assert success is True

    def test_spectator_stored_in_spectators_dict(self, gm_in_game):
        """Spectators should be stored in a separate spectators dict."""
        gm_in_game.add_spectator('sid_late', 'LateGuy')
        assert 'sid_late' in gm_in_game.spectators
        assert gm_in_game.spectators['sid_late']['name'] == 'LateGuy'

    def test_spectator_not_in_players(self, gm_in_game):
        """Spectators should not be in the players dict."""
        gm_in_game.add_spectator('sid_late', 'LateGuy')
        assert 'sid_late' not in gm_in_game.players


class TestSpectatorRestrictions:
    """Tests for spectator message and vote restrictions."""

    def test_spectator_cannot_send_message(self, gm_in_game):
        """A spectator should not be allowed to send messages."""
        gm_in_game.add_spectator('sid_late', 'LateGuy')
        assert gm_in_game.can_send_message('sid_late') is False

    def test_spectator_cannot_vote(self, gm_in_game):
        """A spectator should not be able to vote."""
        gm_in_game.add_spectator('sid_late', 'LateGuy')
        gm_in_game.state = GameState.VOTING
        success, msg = gm_in_game.submit_vote('sid_late', 'Alice')
        assert success is False

    def test_spectator_not_in_turn_order(self, gm_in_game):
        """Spectators should never appear in the turn order."""
        gm_in_game.add_spectator('sid_late', 'LateGuy')
        gm_in_game._generate_turn_order()
        assert 'sid_late' not in gm_in_game.turn_order


class TestSpectatorInGameState:
    """Tests for spectator info in game state broadcast data."""

    def test_get_spectator_list(self, gm_in_game):
        """get_spectator_list should return spectator names."""
        gm_in_game.add_spectator('sid_late', 'LateGuy')
        spectator_list = gm_in_game.get_spectator_list()
        assert len(spectator_list) == 1
        assert spectator_list[0]['name'] == 'LateGuy'

    def test_spectator_count(self, gm_in_game):
        """Spectator count should be accurate."""
        gm_in_game.add_spectator('sid_late1', 'Late1')
        gm_in_game.add_spectator('sid_late2', 'Late2')
        assert len(gm_in_game.get_spectator_list()) == 2

    def test_remove_spectator_on_disconnect(self, gm_in_game):
        """Spectator should be removed on disconnect."""
        gm_in_game.add_spectator('sid_late', 'LateGuy')
        gm_in_game.remove_spectator('sid_late')
        assert 'sid_late' not in gm_in_game.spectators
