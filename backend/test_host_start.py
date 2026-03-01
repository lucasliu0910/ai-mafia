"""Tests for host-only game start permission."""
import pytest
from game_manager import GameManager, GameState


@pytest.fixture
def gm():
    """Create a fresh GameManager instance for each test."""
    return GameManager()


class TestHostOnlyGameStart:
    """Tests for restricting game start to the host player."""

    def test_host_can_start_game(self, gm):
        """The host should be able to start the game."""
        gm.add_player('sid_1', 'Alice')
        gm.add_player('sid_2', 'Bob')
        gm.add_player('sid_3', 'Charlie')
        success, msg = gm.start_game('AI_Agent', requester_sid='sid_1')
        assert success is True

    def test_non_host_cannot_start_game(self, gm):
        """A non-host player should not be able to start the game."""
        gm.add_player('sid_1', 'Alice')
        gm.add_player('sid_2', 'Bob')
        gm.add_player('sid_3', 'Charlie')
        success, msg = gm.start_game('AI_Agent', requester_sid='sid_2')
        assert success is False
        assert 'host' in msg.lower()

    def test_non_host_start_does_not_change_state(self, gm):
        """Game state should remain LOBBY if a non-host tries to start."""
        gm.add_player('sid_1', 'Alice')
        gm.add_player('sid_2', 'Bob')
        gm.add_player('sid_3', 'Charlie')
        gm.start_game('AI_Agent', requester_sid='sid_2')
        assert gm.state == GameState.LOBBY

    def test_start_game_without_requester_sid_fails(self, gm):
        """Calling start_game without requester_sid should fail."""
        gm.add_player('sid_1', 'Alice')
        gm.add_player('sid_2', 'Bob')
        gm.add_player('sid_3', 'Charlie')
        success, msg = gm.start_game('AI_Agent')
        assert success is False

    def test_host_start_transitions_to_chat(self, gm):
        """When host starts the game, state should transition to CHAT."""
        gm.add_player('sid_1', 'Alice')
        gm.add_player('sid_2', 'Bob')
        gm.add_player('sid_3', 'Charlie')
        gm.start_game('AI_Agent', requester_sid='sid_1')
        assert gm.state == GameState.CHAT

    def test_start_requires_minimum_players(self, gm):
        """Game should not start with fewer than 3 human players."""
        gm.add_player('sid_1', 'Alice')
        gm.add_player('sid_2', 'Bob')
        success, msg = gm.start_game('AI_Agent', requester_sid='sid_1')
        assert success is False
        assert 'enough' in msg.lower() or 'players' in msg.lower()
