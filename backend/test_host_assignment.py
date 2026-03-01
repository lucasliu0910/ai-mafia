"""Tests for host assignment logic in GameManager."""
import pytest
from game_manager import GameManager, GameState


@pytest.fixture
def gm():
    """Create a fresh GameManager instance for each test."""
    return GameManager()


class TestHostAssignment:
    """Tests for first-player-becomes-host behavior."""

    def test_first_player_becomes_host(self, gm):
        """The first player to join should be assigned as host."""
        gm.add_player('sid_1', 'Alice')
        assert gm.players['sid_1'].get('is_host') is True

    def test_second_player_is_not_host(self, gm):
        """Subsequent players should not be host."""
        gm.add_player('sid_1', 'Alice')
        gm.add_player('sid_2', 'Bob')
        assert gm.players['sid_2'].get('is_host') is not True

    def test_only_one_host_exists(self, gm):
        """There should be exactly one host at any time."""
        gm.add_player('sid_1', 'Alice')
        gm.add_player('sid_2', 'Bob')
        gm.add_player('sid_3', 'Charlie')
        hosts = [p for p in gm.players.values() if p.get('is_host')]
        assert len(hosts) == 1

    def test_host_sid_tracked(self, gm):
        """GameManager should track the host's sid."""
        gm.add_player('sid_1', 'Alice')
        assert gm.host_sid == 'sid_1'

    def test_host_sid_is_none_initially(self, gm):
        """Before any players join, host_sid should be None."""
        assert gm.host_sid is None


class TestHostTransferOnDisconnect:
    """Tests for host transfer when the host disconnects."""

    def test_host_transfers_on_disconnect(self, gm):
        """When the host disconnects, the next player becomes host."""
        gm.add_player('sid_1', 'Alice')
        gm.add_player('sid_2', 'Bob')
        gm.remove_player('sid_1')
        assert gm.host_sid == 'sid_2'
        assert gm.players['sid_2'].get('is_host') is True

    def test_host_transfers_to_earliest_joiner(self, gm):
        """Host should transfer to the next player in join order."""
        gm.add_player('sid_1', 'Alice')
        gm.add_player('sid_2', 'Bob')
        gm.add_player('sid_3', 'Charlie')
        gm.remove_player('sid_1')
        assert gm.host_sid == 'sid_2'

    def test_host_sid_none_when_all_leave(self, gm):
        """If all players leave, host_sid should be None."""
        gm.add_player('sid_1', 'Alice')
        gm.remove_player('sid_1')
        assert gm.host_sid is None

    def test_non_host_disconnect_no_transfer(self, gm):
        """Removing a non-host player should not change the host."""
        gm.add_player('sid_1', 'Alice')
        gm.add_player('sid_2', 'Bob')
        gm.remove_player('sid_2')
        assert gm.host_sid == 'sid_1'
        assert gm.players['sid_1'].get('is_host') is True
