"""Tests for updated win conditions in GameManager."""
import pytest
import random
from game_manager import GameManager, GameState


@pytest.fixture
def gm_voting():
    """Create a GameManager with 4 human players + AI in VOTING state."""
    gm = GameManager()
    gm.add_player('sid_1', 'Alice')
    gm.add_player('sid_2', 'Bob')
    gm.add_player('sid_3', 'Charlie')
    gm.add_player('sid_4', 'Dave')
    gm.start_game('AI_Agent', requester_sid='sid_1')
    gm.state = GameState.VOTING
    return gm


class TestHumanWinCondition:
    """Tests for human win: most-voted player is AI."""

    def test_human_wins_when_ai_eliminated(self, gm_voting):
        """Humans win if the eliminated player is the AI."""
        ai_name = gm_voting.players[gm_voting.ai_sid]['name']
        gm_voting.votes = {
            'sid_1': ai_name,
            'sid_2': ai_name,
            'sid_3': ai_name,
            'sid_4': 'Alice',
            gm_voting.ai_sid: 'Alice',
        }
        gm_voting.resolve_votes()
        assert gm_voting.last_round_result['human_won'] is True
        assert gm_voting.last_round_result['game_over'] is True

    def test_ai_is_eliminated_when_most_voted(self, gm_voting):
        """The AI player should be marked eliminated when most-voted."""
        ai_name = gm_voting.players[gm_voting.ai_sid]['name']
        gm_voting.votes = {
            'sid_1': ai_name,
            'sid_2': ai_name,
            'sid_3': ai_name,
            'sid_4': 'Alice',
            gm_voting.ai_sid: 'Bob',
        }
        gm_voting.resolve_votes()
        assert gm_voting.players[gm_voting.ai_sid]['eliminated'] is True


class TestAIWinCondition:
    """Tests for AI win: 3 players remaining (including AI)."""

    def test_ai_wins_when_3_players_remain(self, gm_voting):
        """AI wins after elimination leaves only 3 players (including AI)."""
        # Start with 5 players (4 human + 1 AI)
        # Eliminate 1 human first to get to 4
        gm_voting.players['sid_4']['eliminated'] = True
        # Now 4 living: sid_1, sid_2, sid_3, ai_sid
        # Vote to eliminate sid_3 → 3 remaining (sid_1, sid_2, ai_sid)
        gm_voting.votes = {
            'sid_1': 'Charlie',
            'sid_2': 'Charlie',
            'sid_3': 'Alice',
            gm_voting.ai_sid: 'Charlie',
        }
        gm_voting.resolve_votes()
        assert gm_voting.last_round_result['ai_won'] is True
        assert gm_voting.last_round_result['game_over'] is True

    def test_ai_does_not_win_with_more_than_3(self, gm_voting):
        """AI does not win if more than 3 players remain after elimination."""
        # 5 players, eliminate 1 → 4 remain → no AI win
        gm_voting.votes = {
            'sid_1': 'Dave',
            'sid_2': 'Dave',
            'sid_3': 'Dave',
            'sid_4': 'Alice',
            gm_voting.ai_sid: 'Dave',
        }
        gm_voting.resolve_votes()
        assert gm_voting.last_round_result['ai_won'] is False
        assert gm_voting.last_round_result['game_over'] is False

    def test_ai_win_not_triggered_if_ai_eliminated(self, gm_voting):
        """AI cannot win if it is the one being eliminated."""
        # Eliminate 2 humans first to get to 3 living
        gm_voting.players['sid_3']['eliminated'] = True
        gm_voting.players['sid_4']['eliminated'] = True
        # Now 3 living: sid_1, sid_2, ai_sid
        # Vote to eliminate AI → human win, not AI win
        ai_name = gm_voting.players[gm_voting.ai_sid]['name']
        gm_voting.votes = {
            'sid_1': ai_name,
            'sid_2': ai_name,
            gm_voting.ai_sid: 'Alice',
        }
        gm_voting.resolve_votes()
        assert gm_voting.last_round_result['human_won'] is True
        assert gm_voting.last_round_result['ai_won'] is False


class TestTieVoteHandling:
    """Tests for tie vote resolution."""

    def test_tie_eliminates_one_of_tied_players(self, gm_voting):
        """A tie should randomly eliminate one of the tied players."""
        gm_voting.votes = {
            'sid_1': 'Bob',
            'sid_2': 'Alice',
            'sid_3': 'Bob',
            'sid_4': 'Alice',
            gm_voting.ai_sid: 'Charlie',
        }
        random.seed(42)
        gm_voting.resolve_votes()
        eliminated = gm_voting.last_round_result['eliminated']
        assert eliminated in ('Alice', 'Bob')

    def test_tie_only_among_top_voted(self, gm_voting):
        """Only the top-voted tied players should be candidates for elimination."""
        gm_voting.votes = {
            'sid_1': 'Bob',
            'sid_2': 'Alice',
            'sid_3': 'Bob',
            'sid_4': 'Alice',
            gm_voting.ai_sid: 'Charlie',
        }
        random.seed(42)
        gm_voting.resolve_votes()
        eliminated = gm_voting.last_round_result['eliminated']
        # Charlie only got 1 vote, should never be eliminated in a tie
        assert eliminated != 'Charlie'


class TestNoMaxRoundsLimit:
    """Tests for removing the max_rounds hard limit."""

    def test_no_game_over_from_round_count(self):
        """Game should not end just because round count reaches old max_rounds."""
        gm = GameManager()
        gm.add_player('sid_1', 'Alice')
        gm.add_player('sid_2', 'Bob')
        gm.add_player('sid_3', 'Charlie')
        gm.start_game('AI_Agent', requester_sid='sid_1')
        gm.state = GameState.VOTING
        gm.round = 10  # Well past old max_rounds=3
        gm.votes = {
            'sid_1': 'Charlie',
            'sid_2': 'Charlie',
            'sid_3': 'Alice',
            gm.ai_sid: 'Charlie',
        }
        gm.resolve_votes()
        # With 3 players remaining (sid_1, sid_2, AI), AI should win
        # due to 3-player rule, NOT max_rounds
        assert gm.last_round_result['ai_won'] is True

    def test_game_continues_past_old_limit(self):
        """Game should continue if enough players remain, regardless of round."""
        gm = GameManager()
        gm.add_player('sid_1', 'Alice')
        gm.add_player('sid_2', 'Bob')
        gm.add_player('sid_3', 'Charlie')
        gm.add_player('sid_4', 'Dave')
        gm.add_player('sid_5', 'Eve')
        gm.start_game('AI_Agent', requester_sid='sid_1')
        gm.state = GameState.VOTING
        gm.round = 100
        gm.votes = {
            'sid_1': 'Eve',
            'sid_2': 'Eve',
            'sid_3': 'Eve',
            'sid_4': 'Eve',
            'sid_5': 'Alice',
            gm.ai_sid: 'Eve',
        }
        gm.resolve_votes()
        # 5 remain after eliminating Eve → game continues
        assert gm.last_round_result['game_over'] is False
        assert gm.last_round_result['ai_won'] is False
