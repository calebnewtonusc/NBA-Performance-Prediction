"""Tests for game feature engineering"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.data_processing.game_features import GameFeatureEngineer


class TestGameFeatureEngineer:
    """Test GameFeatureEngineer class"""

    @pytest.fixture
    def sample_games_df(self):
        """Create sample games DataFrame"""
        dates = [datetime(2023, 10, 1) + timedelta(days=i) for i in range(20)]

        data = {
            "game_id": range(1, 21),
            "date": dates,
            "home_team_id": [1, 2, 1, 2, 1] * 4,
            "away_team_id": [2, 1, 2, 1, 2] * 4,
            "home_score": np.random.randint(95, 125, 20),
            "away_score": np.random.randint(95, 125, 20),
        }

        df = pd.DataFrame(data)
        df["home_win"] = (df["home_score"] > df["away_score"]).astype(int)
        return df

    def test_engineer_initialization(self):
        """Test feature engineer can be initialized"""
        engineer = GameFeatureEngineer()
        assert engineer is not None

    def test_create_game_features(self, sample_games_df):
        """Test creating game features"""
        engineer = GameFeatureEngineer()
        features_df = engineer.create_game_features(sample_games_df)

        assert features_df is not None
        assert len(features_df) <= len(sample_games_df)
        assert "game_id" in features_df.columns
        assert "home_team_id" in features_df.columns

    def test_calculate_team_form(self, sample_games_df):
        """Test team form calculation"""
        engineer = GameFeatureEngineer()
        team_id = 1
        date = datetime(2023, 10, 10)

        form = engineer.calculate_team_form(sample_games_df, team_id, date, n_games=5)

        assert isinstance(form, dict)
        assert "win_pct" in form
        assert 0 <= form["win_pct"] <= 1

    def test_calculate_win_streak(self, sample_games_df):
        """Test win streak calculation"""
        engineer = GameFeatureEngineer()
        team_id = 1
        date = datetime(2023, 10, 15)

        streak = engineer.calculate_win_streak(sample_games_df, team_id, date)

        assert isinstance(streak, int)

    def test_is_back_to_back(self, sample_games_df):
        """Test back-to-back game detection"""
        engineer = GameFeatureEngineer()
        team_id = 1
        date = datetime(2023, 10, 2)

        is_b2b = engineer.is_back_to_back(sample_games_df, team_id, date)

        assert isinstance(is_b2b, bool)
