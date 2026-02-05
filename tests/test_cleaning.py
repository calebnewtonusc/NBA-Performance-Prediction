"""
Tests for DataCleaner
"""

import pytest
import pandas as pd
import numpy as np
from src.data_processing.cleaning import DataCleaner


@pytest.fixture
def sample_player_stats():
    """Sample player statistics data"""
    return pd.DataFrame({
        "player_id": [1, 2, 3, 4, 5, 6],
        "pts": [25, 30, -5, 15, 200, 20],  # Has negative and extreme values
        "ast": [5, 7, 3, None, 8, 6],
        "reb": [10, 8, 6, 4, 12, 9],
        "fgm": [10, 12, 5, 6, 15, 8],
        "fga": [20, 25, 18, 5, 30, 20],  # FGA < FGM for player 4
        "fg_pct": [0.5, 0.48, 0.3, 1.5, 0.5, 0.4]  # Invalid percentage for player 4
    })


@pytest.fixture
def sample_game_data():
    """Sample game data"""
    return pd.DataFrame({
        "id": [1, 2, 2, 3, 4],  # Duplicate ID
        "home_team_score": [105, 110, 110, -10, 200],  # Negative score
        "visitor_team_score": [98, 105, 105, 100, 180],
        "status": ["Final", "Final", "Final", "Final", "In Progress"]
    })


def test_cleaner_initialization():
    """Test DataCleaner initialization"""
    cleaner = DataCleaner()
    assert cleaner is not None


def test_handle_missing_values_mean(sample_player_stats):
    """Test missing value handling with mean strategy"""
    cleaner = DataCleaner()
    df = cleaner.handle_missing_values(sample_player_stats, strategy="mean")

    assert df["ast"].isna().sum() == 0


def test_handle_missing_values_zero(sample_player_stats):
    """Test missing value handling with zero strategy"""
    cleaner = DataCleaner()
    df = cleaner.handle_missing_values(sample_player_stats, strategy="zero")

    assert df["ast"].isna().sum() == 0
    assert df.loc[3, "ast"] == 0


def test_detect_outliers_iqr(sample_player_stats):
    """Test IQR outlier detection"""
    cleaner = DataCleaner()
    outliers, lower, upper = cleaner.detect_outliers_iqr(sample_player_stats, "pts")

    assert outliers.sum() >= 1  # Should detect at least the 200 point game


def test_remove_outliers(sample_player_stats):
    """Test outlier removal"""
    cleaner = DataCleaner()
    original_len = len(sample_player_stats)
    df = cleaner.remove_outliers(sample_player_stats, columns=["pts"])

    assert len(df) < original_len


def test_cap_outliers(sample_player_stats):
    """Test outlier capping"""
    cleaner = DataCleaner()
    df = cleaner.cap_outliers(sample_player_stats, columns=["pts"])

    # Should cap the 200 point value
    assert df["pts"].max() < 200


def test_validate_player_stats(sample_player_stats):
    """Test player stats validation"""
    cleaner = DataCleaner()
    report = cleaner.validate_player_stats(sample_player_stats)

    assert report["total_rows"] == len(sample_player_stats)
    assert len(report["issues"]) > 0  # Should find issues


def test_validate_game_data(sample_game_data):
    """Test game data validation"""
    cleaner = DataCleaner()
    report = cleaner.validate_game_data(sample_game_data)

    assert report["total_rows"] == len(sample_game_data)
    assert len(report["issues"]) > 0  # Should find duplicate and negative score


def test_clean_player_stats(sample_player_stats):
    """Test player stats cleaning"""
    cleaner = DataCleaner()
    df = cleaner.clean_player_stats(sample_player_stats)

    # Should remove negative points
    assert (df["pts"] >= 0).all()

    # Should fix FGM > FGA
    assert (df["fgm"] <= df["fga"]).all()


def test_clean_game_data(sample_game_data):
    """Test game data cleaning"""
    cleaner = DataCleaner()
    df = cleaner.clean_game_data(sample_game_data)

    # Should remove negative scores
    assert (df["home_team_score"] >= 0).all()

    # Should remove duplicates
    assert df["id"].duplicated().sum() == 0

    # Should only have finished games
    assert (df["status"] == "Final").all()


def test_generate_quality_report(sample_player_stats):
    """Test quality report generation"""
    cleaner = DataCleaner()
    report = cleaner.generate_quality_report(sample_player_stats, "Test Dataset")

    assert report["name"] == "Test Dataset"
    assert report["rows"] == len(sample_player_stats)
    assert "missing_values" in report
