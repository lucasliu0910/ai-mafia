"""Tests for auto-assigned nickname system in GameManager."""
import pytest
from game_manager import GameManager, GameState, NICKNAME_POOL


class TestNicknamePool:
    """Tests for the nickname pool and assignment."""

    def test_nickname_pool_exists(self):
        """A predefined nickname pool should exist with 30+ names."""
        assert len(NICKNAME_POOL) >= 30

    def test_nickname_pool_has_unique_names(self):
        """All names in the pool should be unique."""
        assert len(NICKNAME_POOL) == len(set(NICKNAME_POOL))

    def test_assign_nickname_returns_string(self):
        """assign_nickname should return a string."""
        gm = GameManager()
        name = gm.assign_nickname()
        assert isinstance(name, str)
        assert len(name) > 0

    def test_assign_nickname_from_pool(self):
        """Assigned nickname should come from the pool."""
        gm = GameManager()
        name = gm.assign_nickname()
        assert name in NICKNAME_POOL

    def test_assign_nickname_unique_among_players(self):
        """Assigned nicknames should not duplicate existing player names."""
        gm = GameManager()
        gm.add_player('sid_1')
        name1 = gm.players['sid_1']['name']
        gm.add_player('sid_2')
        name2 = gm.players['sid_2']['name']
        assert name1 != name2

    def test_assign_nickname_unique_among_spectators(self):
        """Assigned nicknames should not duplicate existing spectator names."""
        gm = GameManager()
        gm.add_player('sid_1')
        gm.add_player('sid_2')
        gm.add_player('sid_3')
        gm.start_game('AI_Agent', requester_sid='sid_1')
        gm.add_spectator('sid_late')
        spectator_name = gm.spectators['sid_late']['name']
        player_names = [p['name'] for p in gm.players.values()]
        assert spectator_name not in player_names


class TestAddPlayerAutoNickname:
    """Tests for add_player with auto-assigned nickname."""

    def test_add_player_no_name_succeeds(self):
        """add_player with no name should succeed and auto-assign."""
        gm = GameManager()
        success, msg = gm.add_player('sid_1')
        assert success is True

    def test_add_player_no_name_assigns_nickname(self):
        """add_player with no name should assign a nickname from the pool."""
        gm = GameManager()
        gm.add_player('sid_1')
        assert gm.players['sid_1']['name'] in NICKNAME_POOL

    def test_add_player_response_includes_nickname(self):
        """add_player should return the assigned nickname in the message."""
        gm = GameManager()
        success, msg = gm.add_player('sid_1')
        assert success is True
        # The player should have a name assigned
        assert gm.players['sid_1']['name'] != ''

    def test_add_player_multiple_unique(self):
        """Multiple players should get different nicknames."""
        gm = GameManager()
        gm.add_player('sid_1')
        gm.add_player('sid_2')
        gm.add_player('sid_3')
        names = [p['name'] for p in gm.players.values()]
        assert len(names) == len(set(names))


class TestAddSpectatorAutoNickname:
    """Tests for add_spectator with auto-assigned nickname."""

    def test_add_spectator_no_name_succeeds(self):
        """add_spectator with no name should succeed and auto-assign."""
        gm = GameManager()
        gm.add_player('sid_1')
        gm.add_player('sid_2')
        gm.add_player('sid_3')
        gm.start_game('AI_Agent', requester_sid='sid_1')
        success, msg = gm.add_spectator('sid_late')
        assert success is True

    def test_add_spectator_no_name_assigns_nickname(self):
        """add_spectator with no name should assign a nickname from the pool."""
        gm = GameManager()
        gm.add_player('sid_1')
        gm.add_player('sid_2')
        gm.add_player('sid_3')
        gm.start_game('AI_Agent', requester_sid='sid_1')
        gm.add_spectator('sid_late')
        assert gm.spectators['sid_late']['name'] in NICKNAME_POOL

    def test_add_spectator_unique_across_players_and_spectators(self):
        """Spectator nickname should be unique across players and other spectators."""
        gm = GameManager()
        gm.add_player('sid_1')
        gm.add_player('sid_2')
        gm.add_player('sid_3')
        gm.start_game('AI_Agent', requester_sid='sid_1')
        gm.add_spectator('sid_late1')
        gm.add_spectator('sid_late2')
        all_names = [p['name'] for p in gm.players.values()] + \
                    [s['name'] for s in gm.spectators.values()]
        assert len(all_names) == len(set(all_names))
