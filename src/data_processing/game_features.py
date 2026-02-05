"""
Game Feature Engineering Module

This module creates features for predicting game outcomes:
- Rolling averages (last N games)
- Head-to-head history
- Home/away splits
- Rest days
- Win/loss streaks
- Strength of schedule

Usage:
    from src.data_processing.game_features import GameFeatureEngineer

    engineer = GameFeatureEngineer()
    features_df = engineer.create_all_features(games_df)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class GameFeatureEngineer:
    """Feature engineering for game outcome prediction"""

    def __init__(self):
        """Initialize the feature engineer"""
        pass

    def prepare_game_dataframe(self, games: List[Dict]) -> pd.DataFrame:
        """
        Convert list of game dictionaries to DataFrame and prepare it

        Args:
            games: List of game dictionaries

        Returns:
            Prepared DataFrame
        """
        df = pd.DataFrame(games)

        # Parse date if it exists
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df = df.sort_values("date").reset_index(drop=True)

        # Extract team IDs
        if "home_team" in df.columns and isinstance(df["home_team"].iloc[0], dict):
            df["home_team_id"] = df["home_team"].apply(lambda x: x.get("id") if isinstance(x, dict) else x)
            df["visitor_team_id"] = df["visitor_team"].apply(lambda x: x.get("id") if isinstance(x, dict) else x)

        return df

    def calculate_rolling_averages(
        self,
        df: pd.DataFrame,
        team_id_col: str,
        value_cols: List[str],
        windows: List[int] = [5, 10, 20]
    ) -> pd.DataFrame:
        """
        Calculate rolling averages for team statistics

        Args:
            df: Game DataFrame (must be sorted by date)
            team_id_col: Column containing team IDs
            value_cols: Columns to calculate rolling averages for
            windows: Window sizes for rolling averages

        Returns:
            DataFrame with rolling average columns added
        """
        df = df.copy()

        for window in windows:
            for col in value_cols:
                if col not in df.columns:
                    continue

                # Calculate rolling average per team
                df[f"{col}_rolling_{window}"] = df.groupby(team_id_col)[col].transform(
                    lambda x: x.rolling(window=window, min_periods=1).mean()
                )

        return df

    def calculate_team_form(
        self,
        df: pd.DataFrame,
        team_id: int,
        date: pd.Timestamp,
        n_games: int = 10
    ) -> Dict[str, float]:
        """
        Calculate team form (recent performance) before a specific date

        Args:
            df: Game DataFrame
            team_id: Team ID
            date: Date to calculate form before
            n_games: Number of recent games to consider

        Returns:
            Dictionary with form metrics
        """
        # Get team's games before this date
        team_games = df[
            ((df["home_team_id"] == team_id) | (df["visitor_team_id"] == team_id)) &
            (df["date"] < date)
        ].tail(n_games)

        if team_games.empty:
            return {
                "games_played": 0,
                "win_pct": 0.0,
                "avg_points_scored": 0.0,
                "avg_points_allowed": 0.0,
                "avg_point_differential": 0.0
            }

        # Vectorized calculation
        is_home = team_games["home_team_id"] == team_id
        is_away = ~is_home

        team_scores = pd.Series(dtype=float)
        opp_scores = pd.Series(dtype=float)

        # Home games
        team_scores = pd.concat([
            team_games.loc[is_home, "home_team_score"],
            team_scores
        ])
        opp_scores = pd.concat([
            team_games.loc[is_home, "visitor_team_score"],
            opp_scores
        ])

        # Away games
        team_scores = pd.concat([
            team_scores,
            team_games.loc[is_away, "visitor_team_score"]
        ])
        opp_scores = pd.concat([
            opp_scores,
            team_games.loc[is_away, "home_team_score"]
        ])

        wins = (team_scores > opp_scores).sum()
        points_scored = team_scores.tolist()
        points_allowed = opp_scores.tolist()

        return {
            "games_played": len(team_games),
            "win_pct": wins / len(team_games),
            "avg_points_scored": np.mean(points_scored),
            "avg_points_allowed": np.mean(points_allowed),
            "avg_point_differential": np.mean(points_scored) - np.mean(points_allowed)
        }

    def calculate_head_to_head(
        self,
        df: pd.DataFrame,
        team1_id: int,
        team2_id: int,
        before_date: pd.Timestamp,
        n_games: int = 10
    ) -> Dict[str, Any]:
        """
        Calculate head-to-head statistics between two teams

        Args:
            df: Game DataFrame
            team1_id: First team ID
            team2_id: Second team ID
            before_date: Only consider games before this date
            n_games: Number of recent H2H games to consider

        Returns:
            Dictionary with head-to-head stats
        """
        # Get games between these two teams
        h2h_games = df[
            (
                ((df["home_team_id"] == team1_id) & (df["visitor_team_id"] == team2_id)) |
                ((df["home_team_id"] == team2_id) & (df["visitor_team_id"] == team1_id))
            ) &
            (df["date"] < before_date)
        ].tail(n_games)

        if h2h_games.empty:
            return {
                "h2h_games": 0,
                "team1_wins": 0,
                "team2_wins": 0,
                "team1_win_pct": 0.0
            }

        # Vectorized calculation
        team1_home = h2h_games["home_team_id"] == team1_id
        team1_away = ~team1_home
        home_won = h2h_games["home_team_score"] > h2h_games["visitor_team_score"]

        team1_wins = ((team1_home & home_won) | (team1_away & ~home_won)).sum()

        return {
            "h2h_games": len(h2h_games),
            "team1_wins": team1_wins,
            "team2_wins": len(h2h_games) - team1_wins,
            "team1_win_pct": team1_wins / len(h2h_games)
        }

    def calculate_rest_days(
        self,
        df: pd.DataFrame,
        team_id: int,
        game_date: pd.Timestamp
    ) -> int:
        """
        Calculate days of rest before a game

        Args:
            df: Game DataFrame
            team_id: Team ID
            game_date: Date of the game

        Returns:
            Number of rest days
        """
        # Get team's previous game
        prev_games = df[
            ((df["home_team_id"] == team_id) | (df["visitor_team_id"] == team_id)) &
            (df["date"] < game_date)
        ]

        if prev_games.empty:
            return 999  # No previous game

        last_game_date = prev_games["date"].max()
        rest_days = (game_date - last_game_date).days

        return rest_days

    def calculate_win_streak(
        self,
        df: pd.DataFrame,
        team_id: int,
        before_date: pd.Timestamp
    ) -> int:
        """
        Calculate current win/loss streak

        Args:
            df: Game DataFrame
            team_id: Team ID
            before_date: Calculate streak before this date

        Returns:
            Streak length (positive for wins, negative for losses)
        """
        # Get team's recent games
        team_games = df[
            ((df["home_team_id"] == team_id) | (df["visitor_team_id"] == team_id)) &
            (df["date"] < before_date)
        ].sort_values("date", ascending=False)

        if team_games.empty:
            return 0

        # Vectorized win/loss calculation
        is_home = team_games["home_team_id"] == team_id
        won = pd.Series(False, index=team_games.index)
        won[is_home] = team_games.loc[is_home, "home_team_score"] > team_games.loc[is_home, "visitor_team_score"]
        won[~is_home] = team_games.loc[~is_home, "visitor_team_score"] > team_games.loc[~is_home, "home_team_score"]

        # Calculate streak (stop at first change)
        if len(won) == 0:
            return 0

        results = won.tolist()
        first_result = results[0]
        streak = 0

        for result in results:
            if result == first_result:
                streak += 1 if first_result else -1
            else:
                break

        return streak

    def calculate_home_away_splits(
        self,
        df: pd.DataFrame,
        team_id: int,
        before_date: pd.Timestamp,
        n_games: int = 10
    ) -> Dict[str, float]:
        """
        Calculate home and away performance splits

        Args:
            df: Game DataFrame
            team_id: Team ID
            before_date: Calculate before this date
            n_games: Number of games to consider

        Returns:
            Dictionary with home/away splits
        """
        # Home games
        home_games = df[
            (df["home_team_id"] == team_id) &
            (df["date"] < before_date)
        ].tail(n_games)

        home_wins = (home_games["home_team_score"] > home_games["visitor_team_score"]).sum()
        home_win_pct = home_wins / len(home_games) if len(home_games) > 0 else 0.0

        # Away games
        away_games = df[
            (df["visitor_team_id"] == team_id) &
            (df["date"] < before_date)
        ].tail(n_games)

        away_wins = (away_games["visitor_team_score"] > away_games["home_team_score"]).sum()
        away_win_pct = away_wins / len(away_games) if len(away_games) > 0 else 0.0

        return {
            "home_games": len(home_games),
            "home_win_pct": home_win_pct,
            "away_games": len(away_games),
            "away_win_pct": away_win_pct
        }

    def is_back_to_back(
        self,
        df: pd.DataFrame,
        team_id: int,
        game_date: pd.Timestamp
    ) -> bool:
        """
        Check if team is playing back-to-back games

        Args:
            df: Game DataFrame
            team_id: Team ID
            game_date: Date of the game

        Returns:
            True if back-to-back, False otherwise
        """
        rest_days = self.calculate_rest_days(df, team_id, game_date)
        return rest_days == 1

    def create_game_features(
        self,
        df: pd.DataFrame,
        include_future_target: bool = True
    ) -> pd.DataFrame:
        """
        Create comprehensive feature set for each game

        Args:
            df: Game DataFrame
            include_future_target: Whether to include the target variable

        Returns:
            DataFrame with features for each game
        """
        logger.info("Creating game features...")

        df = df.copy()
        features = []

        # Use itertuples() for better performance (10-100x faster than iterrows)
        for game in df.itertuples():
            game_date = game.date
            home_team = game.home_team_id
            away_team = game.visitor_team_id

            # Team form features
            home_form = self.calculate_team_form(df, home_team, game_date, n_games=10)
            away_form = self.calculate_team_form(df, away_team, game_date, n_games=10)

            # Head-to-head
            h2h = self.calculate_head_to_head(df, home_team, away_team, game_date)

            # Rest days
            home_rest = self.calculate_rest_days(df, home_team, game_date)
            away_rest = self.calculate_rest_days(df, away_team, game_date)

            # Win streaks
            home_streak = self.calculate_win_streak(df, home_team, game_date)
            away_streak = self.calculate_win_streak(df, away_team, game_date)

            # Home/away splits
            home_splits = self.calculate_home_away_splits(df, home_team, game_date)
            away_splits = self.calculate_home_away_splits(df, away_team, game_date)

            # Back-to-back
            home_b2b = self.is_back_to_back(df, home_team, game_date)
            away_b2b = self.is_back_to_back(df, away_team, game_date)

            feature_dict = {
                "game_id": game.id,
                "date": game_date,
                "home_team_id": home_team,
                "away_team_id": away_team,

                # Home team form
                "home_win_pct": home_form["win_pct"],
                "home_avg_points": home_form["avg_points_scored"],
                "home_avg_allowed": home_form["avg_points_allowed"],
                "home_point_diff": home_form["avg_point_differential"],

                # Away team form
                "away_win_pct": away_form["win_pct"],
                "away_avg_points": away_form["avg_points_scored"],
                "away_avg_allowed": away_form["avg_points_allowed"],
                "away_point_diff": away_form["avg_point_differential"],

                # Head-to-head
                "h2h_games": h2h["h2h_games"],
                "home_h2h_win_pct": h2h["team1_win_pct"],

                # Rest and schedule
                "home_rest_days": home_rest,
                "away_rest_days": away_rest,
                "home_b2b": int(home_b2b),
                "away_b2b": int(away_b2b),

                # Streaks
                "home_streak": home_streak,
                "away_streak": away_streak,

                # Home/away splits
                "home_home_win_pct": home_splits["home_win_pct"],
                "away_away_win_pct": away_splits["away_win_pct"],
            }

            # Add target variable if requested
            if include_future_target:
                if game.home_team_score > game.visitor_team_score:
                    feature_dict["home_win"] = 1
                else:
                    feature_dict["home_win"] = 0

                feature_dict["home_score"] = game.home_team_score
                feature_dict["away_score"] = game.visitor_team_score

            features.append(feature_dict)

        features_df = pd.DataFrame(features)

        logger.info(f"Created features for {len(features_df)} games with {len(features_df.columns)} columns")

        return features_df


# Example usage
if __name__ == "__main__":
    # This would normally load from saved game data
    print("Game Feature Engineer - Ready for use!")
    print("Load game data and call create_game_features() to generate features")
