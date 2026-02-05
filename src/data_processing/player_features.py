"""
Player Feature Engineering Module

This module creates features for predicting player performance:
- Rolling averages for player stats
- Player efficiency rating (PER)
- Usage rate and pace statistics
- Matchup-based features
- Playing time trends
- Hot/cold streak indicators

Usage:
    from src.data_processing.player_features import PlayerFeatureEngineer

    engineer = PlayerFeatureEngineer()
    features_df = engineer.create_player_features(player_stats_df)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class PlayerFeatureEngineer:
    """Feature engineering for player performance prediction"""

    def __init__(self):
        """Initialize the feature engineer"""
        pass

    def prepare_player_stats_dataframe(self, stats: List[Dict]) -> pd.DataFrame:
        """
        Convert list of player stat dictionaries to DataFrame

        Args:
            stats: List of player stat dictionaries from API

        Returns:
            Prepared DataFrame
        """
        df = pd.DataFrame(stats)

        # Extract player and game info if nested
        if "player" in df.columns and isinstance(df["player"].iloc[0], dict):
            df["player_id"] = df["player"].apply(lambda x: x.get("id") if isinstance(x, dict) else x)
            df["player_name"] = df["player"].apply(
                lambda x: f"{x.get('first_name', '')} {x.get('last_name', '')}" if isinstance(x, dict) else ""
            )

        if "game" in df.columns and isinstance(df["game"].iloc[0], dict):
            df["game_id"] = df["game"].apply(lambda x: x.get("id") if isinstance(x, dict) else x)
            df["game_date"] = df["game"].apply(lambda x: x.get("date") if isinstance(x, dict) else None)
            df["game_date"] = pd.to_datetime(df["game_date"])

        # Sort by player and date
        if "player_id" in df.columns and "game_date" in df.columns:
            df = df.sort_values(["player_id", "game_date"]).reset_index(drop=True)

        return df

    def calculate_player_rolling_averages(
        self,
        df: pd.DataFrame,
        stat_columns: List[str],
        windows: List[int] = [3, 5, 10]
    ) -> pd.DataFrame:
        """
        Calculate rolling averages for player statistics

        Args:
            df: Player stats DataFrame (must be sorted by player_id and date)
            stat_columns: Columns to calculate rolling averages for
            windows: Window sizes for rolling averages

        Returns:
            DataFrame with rolling average columns added
        """
        df = df.copy()

        for window in windows:
            for col in stat_columns:
                if col not in df.columns:
                    continue

                # Calculate rolling average per player
                df[f"{col}_rolling_{window}"] = df.groupby("player_id")[col].transform(
                    lambda x: x.shift(1).rolling(window=window, min_periods=1).mean()
                )

        logger.info(f"Created rolling averages for {len(stat_columns)} stats with windows {windows}")

        return df

    def calculate_player_efficiency_rating(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculate Player Efficiency Rating (PER)
        Simplified version for demonstration

        Args:
            df: Player stats DataFrame

        Returns:
            DataFrame with PER column added
        """
        df = df.copy()

        # Simplified PER calculation
        # Real PER is more complex and requires league averages
        df["PER"] = (
            df["pts"] +
            df["reb"] +
            df["ast"] +
            df["stl"] +
            df["blk"] -
            df["turnover"] -
            (df["fga"] - df["fgm"]) -
            (df["fta"] - df["ftm"])
        )

        # Normalize by minutes played
        df["min_decimal"] = df["min"].apply(self._convert_minutes_to_decimal)
        df["PER"] = df.apply(
            lambda row: (row["PER"] / row["min_decimal"]) if row["min_decimal"] > 0 else 0,
            axis=1
        )

        logger.info("Calculated Player Efficiency Rating")

        return df

    def _convert_minutes_to_decimal(self, min_str: str) -> float:
        """
        Convert minutes string (MM:SS) to decimal

        Args:
            min_str: Minutes string in MM:SS format

        Returns:
            Minutes as decimal
        """
        if pd.isna(min_str) or min_str == "":
            return 0.0

        try:
            if isinstance(min_str, str) and ":" in min_str:
                parts = min_str.split(":")
                minutes = int(parts[0])
                seconds = int(parts[1]) if len(parts) > 1 else 0
                return minutes + seconds / 60.0
            else:
                return float(min_str)
        except:
            return 0.0

    def calculate_usage_rate(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculate usage rate (simplified)
        Usage rate estimates percentage of team plays used by player

        Args:
            df: Player stats DataFrame

        Returns:
            DataFrame with usage_rate column added
        """
        df = df.copy()

        # Simplified usage rate
        df["usage_rate"] = (
            df["fga"] + 0.44 * df["fta"] + df["turnover"]
        )

        logger.info("Calculated usage rate")

        return df

    def calculate_true_shooting_percentage(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculate True Shooting Percentage (TS%)
        More accurate shooting metric than FG%

        Args:
            df: Player stats DataFrame

        Returns:
            DataFrame with TS% column added
        """
        df = df.copy()

        df["TS_pct"] = df.apply(
            lambda row: row["pts"] / (2 * (row["fga"] + 0.44 * row["fta"]))
            if (row["fga"] + 0.44 * row["fta"]) > 0 else 0,
            axis=1
        )

        logger.info("Calculated True Shooting Percentage")

        return df

    def calculate_player_streak(
        self,
        df: pd.DataFrame,
        metric: str = "pts",
        threshold: float = None
    ) -> pd.DataFrame:
        """
        Calculate hot/cold streak indicators

        Args:
            df: Player stats DataFrame (sorted by player_id and date)
            metric: Metric to track (e.g., 'pts', 'fg_pct')
            threshold: Threshold for "hot" (if None, uses player's average)

        Returns:
            DataFrame with streak columns added
        """
        df = df.copy()

        # Calculate player's average for the metric
        player_avg = df.groupby("player_id")[metric].transform("mean")

        if threshold is None:
            # Use above/below average
            df[f"{metric}_hot"] = (df[metric] > player_avg).astype(int)
        else:
            df[f"{metric}_hot"] = (df[metric] > threshold).astype(int)

        # Calculate streak (consecutive hot games)
        df[f"{metric}_streak"] = df.groupby("player_id")[f"{metric}_hot"].transform(
            lambda x: x.groupby((x != x.shift()).cumsum()).cumcount() + 1
        )

        # Make negative for cold streaks
        df[f"{metric}_streak"] = df.apply(
            lambda row: row[f"{metric}_streak"] if row[f"{metric}_hot"] == 1 else -row[f"{metric}_streak"],
            axis=1
        )

        logger.info(f"Calculated {metric} streak indicators")

        return df

    def calculate_consistency_score(
        self,
        df: pd.DataFrame,
        stat_columns: List[str] = ["pts", "ast", "reb"],
        window: int = 10
    ) -> pd.DataFrame:
        """
        Calculate consistency score (inverse of variance)

        Args:
            df: Player stats DataFrame
            stat_columns: Statistics to measure consistency for
            window: Window size for consistency calculation

        Returns:
            DataFrame with consistency scores added
        """
        df = df.copy()

        for col in stat_columns:
            if col not in df.columns:
                continue

            # Calculate rolling standard deviation
            rolling_std = df.groupby("player_id")[col].transform(
                lambda x: x.rolling(window=window, min_periods=1).std()
            )

            # Consistency score (lower std = more consistent)
            # Normalize by mean to make it relative
            rolling_mean = df.groupby("player_id")[col].transform(
                lambda x: x.rolling(window=window, min_periods=1).mean()
            )

            df[f"{col}_consistency"] = 1 - (rolling_std / (rolling_mean + 1))  # +1 to avoid division by zero
            df[f"{col}_consistency"] = df[f"{col}_consistency"].clip(0, 1)  # Clip to [0, 1]

        logger.info(f"Calculated consistency scores for {len(stat_columns)} stats")

        return df

    def calculate_rest_impact(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculate days of rest and performance correlation

        Args:
            df: Player stats DataFrame

        Returns:
            DataFrame with rest_days column added
        """
        df = df.copy()

        # Calculate days between games for each player
        df["rest_days"] = df.groupby("player_id")["game_date"].diff().dt.days

        # Fill first game with average rest
        df["rest_days"] = df["rest_days"].fillna(2)

        logger.info("Calculated rest days")

        return df

    def calculate_opponent_strength(
        self,
        df: pd.DataFrame,
        team_stats: Optional[Dict[int, Dict]] = None
    ) -> pd.DataFrame:
        """
        Add opponent strength features

        Args:
            df: Player stats DataFrame
            team_stats: Dictionary of team statistics (team_id -> stats)

        Returns:
            DataFrame with opponent strength features
        """
        df = df.copy()

        if team_stats is None:
            # Placeholder - in real use, this would come from team_data
            logger.warning("No team stats provided, using placeholder opponent strength")
            df["opponent_strength"] = 0.5
        else:
            # Would add logic to look up opponent team stats here
            pass

        return df

    def create_player_features(
        self,
        df: pd.DataFrame,
        include_target: bool = True,
        target_column: str = "pts"
    ) -> pd.DataFrame:
        """
        Create comprehensive feature set for player predictions

        Args:
            df: Player stats DataFrame
            include_target: Whether to include target variable
            target_column: Column to use as prediction target

        Returns:
            DataFrame with all features
        """
        logger.info("Creating comprehensive player features...")

        df = self.prepare_player_stats_dataframe(df) if "player_id" not in df.columns else df

        # Calculate all features
        stat_columns = ["pts", "ast", "reb", "stl", "blk", "fgm", "fga", "fg3m", "fg3a"]

        df = self.calculate_player_rolling_averages(df, stat_columns, windows=[3, 5, 10])
        df = self.calculate_player_efficiency_rating(df)
        df = self.calculate_usage_rate(df)
        df = self.calculate_true_shooting_percentage(df)
        df = self.calculate_player_streak(df, metric="pts")
        df = self.calculate_consistency_score(df, stat_columns=["pts", "ast", "reb"])
        df = self.calculate_rest_impact(df)

        # Target variable
        if include_target:
            df["target"] = df[target_column]

        logger.info(f"Created features for {len(df)} player performances with {len(df.columns)} columns")

        return df

    def create_season_averages(
        self,
        df: pd.DataFrame,
        season_col: str = "season"
    ) -> pd.DataFrame:
        """
        Calculate season averages for each player

        Args:
            df: Player stats DataFrame
            season_col: Column containing season year

        Returns:
            DataFrame with season averages
        """
        logger.info("Calculating season averages...")

        stat_columns = ["pts", "ast", "reb", "stl", "blk", "fgm", "fga", "fg3m", "fg3a", "ftm", "fta"]

        # Group by player and season
        if season_col not in df.columns:
            # If no season column, treat all as one season
            season_stats = df.groupby("player_id")[stat_columns].mean().reset_index()
        else:
            season_stats = df.groupby(["player_id", season_col])[stat_columns].agg(["mean", "std"]).reset_index()

        logger.info(f"Calculated season averages for {len(season_stats)} player-seasons")

        return season_stats


# Example usage
if __name__ == "__main__":
    print("Player Feature Engineer - Ready for use!")
    print("Load player stats data and call create_player_features() to generate features")
