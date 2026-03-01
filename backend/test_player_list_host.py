"""Tests for host indicator in player list data."""
import pytest
from game_manager import GameManager, GameState


@pytest.fixture
def gm():
    """Create a fresh GameManager instance for each test."""
    return GameManager()


class TestPlayerListHostIndicator:
    """Tests for is_host flag in get_player_list output."""

    def test_host_flag_in_player_list(self, gm):
        """Player list should include is_host flag."""
        gm.add_player('sid_1', 'Alice')
        player_list = gm.get_player_list()
        assert 'is_host' in player_list[0]

    def test_host_player_marked_true(self, gm):
        """The host player should have is_host=True in player list."""
        gm.add_player('sid_1', 'Alice')
        gm.add_player('sid_2', 'Bob')
        player_list = gm.get_player_list()
        host_entries = [p for p in player_list if p['is_host']]
        assert len(host_entries) == 1
        assert host_entries[0]['name'] == 'Alice'

    def test_non_host_player_marked_false(self, gm):
        """Non-host players should have is_host=False in player list."""
        gm.add_player('sid_1', 'Alice')
        gm.add_player('sid_2', 'Bob')
        player_list = gm.get_player_list()
        bob_entry = [p for p in player_list if p['name'] == 'Bob'][0]
        assert bob_entry['is_host'] is False

    def test_host_transfer_reflected_in_player_list(self, gm):
        """After host disconnect, the new host should be reflected in player list."""
        gm.add_player('sid_1', 'Alice')
        gm.add_player('sid_2', 'Bob')
        gm.remove_player('sid_1')
        player_list = gm.get_player_list()
        assert player_list[0]['is_host'] is True
        assert player_list[0]['name'] == 'Bob'
