"""
Tests for TeamDataCollector
"""

import pytest
from pathlib import Path
from src.data_collection.team_data import TeamDataCollector


@pytest.fixture
def sample_teams():
    """Sample team data for testing"""
    return [
        {
            "id": 14,
            "abbreviation": "LAL",
            "city": "Los Angeles",
            "conference": "West",
            "division": "Pacific",
            "full_name": "Los Angeles Lakers",
            "name": "Lakers"
        },
        {
            "id": 2,
            "abbreviation": "BOS",
            "city": "Boston",
            "conference": "East",
            "division": "Atlantic",
            "full_name": "Boston Celtics",
            "name": "Celtics"
        }
    ]


@pytest.fixture
def sample_games():
    """Sample game data for testing"""
    return [
        {
            "id": 1,
            "home_team": {"id": 14},
            "home_team_score": 105,
            "visitor_team": {"id": 2},
            "visitor_team_score": 98,
            "status": "Final"
        },
        {
            "id": 2,
            "home_team": {"id": 14},
            "home_team_score": 100,
            "visitor_team": {"id": 5},
            "visitor_team_score": 110,
            "status": "Final"
        },
        {
            "id": 3,
            "home_team": {"id": 3},
            "home_team_score": 95,
            "visitor_team": {"id": 14},
            "visitor_team_score": 102,
            "status": "Final"
        }
    ]


def test_team_collector_initialization():
    """Test TeamDataCollector initialization"""
    collector = TeamDataCollector()

    assert collector.client is not None
    assert collector.data_dir == Path("data/raw/teams")


def test_create_team_mapping(sample_teams):
    """Test team mapping creation"""
    collector = TeamDataCollector()
    mapping = collector.create_team_mapping(sample_teams)

    assert 14 in mapping
    assert mapping[14]["abbreviation"] == "LAL"
    assert mapping[14]["full_name"] == "Los Angeles Lakers"


def test_calculate_team_season_stats(sample_games):
    """Test team season statistics calculation"""
    collector = TeamDataCollector()
    stats = collector.calculate_team_season_stats(sample_games, team_id=14)

    assert stats["games_played"] == 3
    assert stats["wins"] == 2
    assert stats["losses"] == 1
    assert stats["home_wins"] == 1
    assert stats["away_wins"] == 1
    assert stats["win_percentage"] == pytest.approx(0.667, rel=0.01)


def test_calculate_standings(sample_teams):
    """Test standings calculation"""
    collector = TeamDataCollector()

    # Create mock team stats
    team_stats = {
        14: {
            "wins": 50,
            "losses": 32,
            "win_percentage": 0.610,
            "avg_points_scored": 110.5,
            "avg_points_allowed": 105.2,
            "team_info": {
                "full_name": "Los Angeles Lakers",
                "abbreviation": "LAL",
                "conference": "West",
                "division": "Pacific"
            }
        },
        2: {
            "wins": 55,
            "losses": 27,
            "win_percentage": 0.671,
            "avg_points_scored": 115.2,
            "avg_points_allowed": 108.1,
            "team_info": {
                "full_name": "Boston Celtics",
                "abbreviation": "BOS",
                "conference": "East",
                "division": "Atlantic"
            }
        }
    }

    standings = collector.calculate_standings(team_stats)

    assert len(standings) == 2
    assert standings[0]["team_id"] == 2  # Boston has more wins
    assert standings[0]["rank"] == 1
    assert standings[1]["rank"] == 2


def test_context_manager():
    """Test TeamDataCollector as context manager"""
    with TeamDataCollector() as collector:
        assert collector is not None
