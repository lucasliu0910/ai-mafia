"""Tests for turn-based chat system in GameManager."""
import pytest
from game_manager import GameManager, GameState


@pytest.fixture
def gm_in_chat():
    """Create a GameManager with 3 players + AI in CHAT state."""
    gm = GameManager()
    gm.add_player('sid_1', 'Alice')
    gm.add_player('sid_2', 'Bob')
    gm.add_player('sid_3', 'Charlie')
    gm.start_game('AI_Agent', requester_sid='sid_1')
    return gm


class TestTurnOrderGeneration:
    """Tests for generating turn order among living players."""

    def test_turn_order_generated_on_game_start(self, gm_in_chat):
        """Turn order should be generated when the game starts."""
        assert hasattr(gm_in_chat, 'turn_order')
        assert gm_in_chat.turn_order is not None
        assert len(gm_in_chat.turn_order) > 0

    def test_turn_order_includes_all_living_players(self, gm_in_chat):
        """Turn order should include all living players including AI."""
        living_sids = [sid for sid, p in gm_in_chat.players.items()
                       if not p.get('eliminated', False)]
        assert set(gm_in_chat.turn_order) == set(living_sids)

    def test_turn_order_includes_ai(self, gm_in_chat):
        """Turn order should include the AI player."""
        assert gm_in_chat.ai_sid in gm_in_chat.turn_order

    def test_current_turn_index_starts_at_zero(self, gm_in_chat):
        """Current turn index should start at 0."""
        assert gm_in_chat.current_turn_index == 0

    def test_get_current_turn_sid(self, gm_in_chat):
        """get_current_turn_sid should return the first player in turn order."""
        current = gm_in_chat.get_current_turn_sid()
        assert current == gm_in_chat.turn_order[0]


class TestTurnAdvancement:
    """Tests for advancing turns."""

    def test_advance_turn_increments_index(self, gm_in_chat):
        """Advancing a turn should increment the current turn index."""
        gm_in_chat.advance_turn()
        assert gm_in_chat.current_turn_index == 1

    def test_advance_turn_returns_next_sid(self, gm_in_chat):
        """Advancing a turn should return the next player's sid."""
        next_sid = gm_in_chat.advance_turn()
        assert next_sid == gm_in_chat.turn_order[1]

    def test_advance_past_last_returns_none(self, gm_in_chat):
        """Advancing past the last player should return None (round complete)."""
        for _ in range(len(gm_in_chat.turn_order)):
            result = gm_in_chat.advance_turn()
        assert result is None

    def test_all_turns_complete_flag(self, gm_in_chat):
        """all_turns_complete should be True after all players have had a turn."""
        for _ in range(len(gm_in_chat.turn_order)):
            gm_in_chat.advance_turn()
        assert gm_in_chat.all_turns_complete() is True

    def test_all_turns_not_complete_initially(self, gm_in_chat):
        """all_turns_complete should be False at the start."""
        assert gm_in_chat.all_turns_complete() is False


class TestMessageRestriction:
    """Tests for restricting messages to the active turn player."""

    def test_active_player_can_send(self, gm_in_chat):
        """The active turn player should be allowed to send a message."""
        active_sid = gm_in_chat.get_current_turn_sid()
        assert gm_in_chat.can_send_message(active_sid) is True

    def test_non_active_player_cannot_send(self, gm_in_chat):
        """A non-active player should not be allowed to send a message."""
        active_sid = gm_in_chat.get_current_turn_sid()
        other_sids = [sid for sid in gm_in_chat.turn_order if sid != active_sid]
        if other_sids:
            assert gm_in_chat.can_send_message(other_sids[0]) is False

    def test_unknown_player_cannot_send(self, gm_in_chat):
        """An unknown sid should not be allowed to send a message."""
        assert gm_in_chat.can_send_message('unknown_sid') is False


class TestChatPhaseCompletion:
    """Tests for transitioning from CHAT to VOTING after all turns."""

    def test_transition_to_voting_after_all_turns(self, gm_in_chat):
        """Game state should transition to VOTING after all turns complete."""
        for _ in range(len(gm_in_chat.turn_order)):
            gm_in_chat.advance_turn()
        gm_in_chat.check_chat_phase_complete()
        assert gm_in_chat.state == GameState.VOTING

    def test_no_transition_during_turns(self, gm_in_chat):
        """Game state should remain CHAT while turns are in progress."""
        gm_in_chat.advance_turn()
        gm_in_chat.check_chat_phase_complete()
        assert gm_in_chat.state == GameState.CHAT
