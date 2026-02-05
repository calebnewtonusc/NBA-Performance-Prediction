"""
Tests for GameDataCollector
"""

import pytest
import json
from pathlib import Path
from src.data_collection.game_data import GameDataCollector


@pytest.fixture
def sample_games():
    """Sample game data for testing"""
    return [
        {
            "id": 1,
            "date": "2023-10-24T00:00:00.000Z",
            "home_team": {"id": 14, "name": "Lakers"},
            "home_team_score": 105,
            "visitor_team": {"id": 2, "name": "Celtics"},
            "visitor_team_score": 98,
            "status": "Final"
        },
        {
            "id": 2,
            "date": "2023-10-25T00:00:00.000Z",
            "home_team": {"id": 5, "name": "Warriors"},
            "home_team_score": 110,
            "visitor_team": {"id": 14, "name": "Lakers"},
            "visitor_team_score": 115,
            "status": "Final"
        }
    ]


def test_game_collector_initialization():
    """Test GameDataCollector initialization"""
    collector = GameDataCollector()

    assert collector.client is not None
    assert collector.data_dir == Path("data/raw/games")


def test_enrich_game_data(sample_games):
    """Test game data enrichment"""
    collector = GameDataCollector()
    enriched = collector.enrich_game_data(sample_games)

    # Check first game
    assert enriched[0]["winner"] == "home"
    assert enriched[0]["winner_team_id"] == 14
    assert enriched[0]["loser_team_id"] == 2
    assert enriched[0]["score_differential"] == 7
    assert enriched[0]["total_points"] == 203

    # Check second game
    assert enriched[1]["winner"] == "away"
    assert enriched[1]["winner_team_id"] == 14
    assert enriched[1]["loser_team_id"] == 5


def test_enrich_game_data_with_tie():
    """Test game data enrichment with tie"""
    collector = GameDataCollector()
    tie_game = [{
        "id": 1,
        "date": "2023-10-24T00:00:00.000Z",
        "home_team": {"id": 1, "name": "Team A"},
        "home_team_score": 100,
        "visitor_team": {"id": 2, "name": "Team B"},
        "visitor_team_score": 100,
        "status": "Final"
    }]

    enriched = collector.enrich_game_data(tie_game)

    assert enriched[0]["winner"] == "tie"
    assert enriched[0]["winner_team_id"] is None
    assert enriched[0]["score_differential"] == 0


def test_save_and_load_games(tmp_path, sample_games):
    """Test saving and loading game data"""
    collector = GameDataCollector()
    test_file = tmp_path / "test_games.json"

    # Save
    collector.save_games_to_file(sample_games, test_file)
    assert test_file.exists()

    # Load
    loaded = collector.load_games_from_file(test_file)
    assert len(loaded) == len(sample_games)
    assert loaded[0]["id"] == sample_games[0]["id"]


def test_context_manager():
    """Test GameDataCollector as context manager"""
    with GameDataCollector() as collector:
        assert collector is not None
