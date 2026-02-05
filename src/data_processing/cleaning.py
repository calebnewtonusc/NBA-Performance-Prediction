"""
Data Cleaning Module

This module provides functions for cleaning and validating NBA data:
- Missing data handling
- Outlier detection
- Data type conversion
- Data quality reporting

Usage:
    from src.data_processing.cleaning import DataCleaner

    cleaner = DataCleaner()
    clean_df = cleaner.clean_player_stats(df)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class DataCleaner:
    """Data cleaning utilities for NBA datasets"""

    def __init__(self):
        """Initialize the data cleaner"""
        pass

    def handle_missing_values(
        self,
        df: pd.DataFrame,
        strategy: str = "mean",
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Handle missing values in a DataFrame

        Args:
            df: Input DataFrame
            strategy: Imputation strategy ('mean', 'median', 'mode', 'zero', 'drop')
            columns: Columns to apply strategy to (None = all numeric columns)

        Returns:
            DataFrame with missing values handled
        """
        df = df.copy()

        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()

        logger.info(f"Handling missing values with strategy: {strategy}")

        for col in columns:
            if col not in df.columns:
                continue

            missing_count = df[col].isna().sum()
            if missing_count == 0:
                continue

            logger.info(f"Column '{col}': {missing_count} missing values")

            if strategy == "mean":
                df[col] = df[col].fillna(df[col].mean())
            elif strategy == "median":
                df[col] = df[col].fillna(df[col].median())
            elif strategy == "mode":
                df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 0)
            elif strategy == "zero":
                df[col] = df[col].fillna(0)
            elif strategy == "drop":
                df = df.dropna(subset=[col])

        return df

    def detect_outliers_iqr(
        self,
        df: pd.DataFrame,
        column: str,
        multiplier: float = 1.5
    ) -> Tuple[pd.Series, float, float]:
        """
        Detect outliers using IQR method

        Args:
            df: Input DataFrame
            column: Column name to check
            multiplier: IQR multiplier (default: 1.5)

        Returns:
            Tuple of (outlier_mask, lower_bound, upper_bound)
        """
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR

        outliers = (df[column] < lower_bound) | (df[column] > upper_bound)

        logger.info(f"Column '{column}': {outliers.sum()} outliers detected")

        return outliers, lower_bound, upper_bound

    def remove_outliers(
        self,
        df: pd.DataFrame,
        columns: List[str],
        method: str = "iqr",
        multiplier: float = 1.5
    ) -> pd.DataFrame:
        """
        Remove outliers from DataFrame

        Args:
            df: Input DataFrame
            columns: Columns to check for outliers
            method: Detection method ('iqr' or 'zscore')
            multiplier: Threshold multiplier

        Returns:
            DataFrame with outliers removed
        """
        df = df.copy()
        original_len = len(df)

        for col in columns:
            if col not in df.columns:
                continue

            if method == "iqr":
                outliers, _, _ = self.detect_outliers_iqr(df, col, multiplier)
                df = df[~outliers]
            elif method == "zscore":
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                df = df[z_scores < multiplier]

        removed = original_len - len(df)
        logger.info(f"Removed {removed} rows with outliers ({removed/original_len*100:.2f}%)")

        return df

    def cap_outliers(
        self,
        df: pd.DataFrame,
        columns: List[str],
        multiplier: float = 1.5
    ) -> pd.DataFrame:
        """
        Cap outliers at upper/lower bounds instead of removing

        Args:
            df: Input DataFrame
            columns: Columns to cap
            multiplier: IQR multiplier

        Returns:
            DataFrame with capped outliers
        """
        df = df.copy()

        for col in columns:
            if col not in df.columns:
                continue

            outliers, lower_bound, upper_bound = self.detect_outliers_iqr(df, col, multiplier)

            df.loc[df[col] < lower_bound, col] = lower_bound
            df.loc[df[col] > upper_bound, col] = upper_bound

            logger.info(f"Column '{col}': Capped {outliers.sum()} outliers")

        return df

    def validate_game_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate game data and return quality report

        Args:
            df: Game DataFrame

        Returns:
            Dictionary with validation results
        """
        report = {
            "total_rows": len(df),
            "issues": [],
            "warnings": []
        }

        required_columns = [
            "id", "date", "home_team_score", "visitor_team_score", "status"
        ]

        # Check for required columns
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            report["issues"].append(f"Missing required columns: {missing_cols}")

        # Check for negative scores
        if "home_team_score" in df.columns:
            negative_home = (df["home_team_score"] < 0).sum()
            if negative_home > 0:
                report["issues"].append(f"{negative_home} games with negative home scores")

        if "visitor_team_score" in df.columns:
            negative_visitor = (df["visitor_team_score"] < 0).sum()
            if negative_visitor > 0:
                report["issues"].append(f"{negative_visitor} games with negative visitor scores")

        # Check for unrealistic scores (> 200)
        if "home_team_score" in df.columns:
            high_scores = (df["home_team_score"] > 200).sum()
            if high_scores > 0:
                report["warnings"].append(f"{high_scores} games with scores > 200")

        # Check for duplicate game IDs
        if "id" in df.columns:
            duplicates = df["id"].duplicated().sum()
            if duplicates > 0:
                report["issues"].append(f"{duplicates} duplicate game IDs")

        # Check missing values
        missing_summary = df.isnull().sum()
        missing_cols = missing_summary[missing_summary > 0]
        if not missing_cols.empty:
            report["warnings"].append(f"Columns with missing values: {missing_cols.to_dict()}")

        return report

    def validate_player_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate player statistics data

        Args:
            df: Player stats DataFrame

        Returns:
            Dictionary with validation results
        """
        report = {
            "total_rows": len(df),
            "issues": [],
            "warnings": []
        }

        # Check for negative statistics
        stat_columns = ["pts", "ast", "reb", "stl", "blk", "fga", "fgm", "fta", "ftm"]
        for col in stat_columns:
            if col in df.columns:
                negative = (df[col] < 0).sum()
                if negative > 0:
                    report["issues"].append(f"{negative} records with negative {col}")

        # Check for impossible percentages
        if "fg_pct" in df.columns:
            invalid_pct = ((df["fg_pct"] < 0) | (df["fg_pct"] > 1)).sum()
            if invalid_pct > 0:
                report["issues"].append(f"{invalid_pct} records with invalid FG%")

        # Check made > attempted
        if "fgm" in df.columns and "fga" in df.columns:
            impossible = (df["fgm"] > df["fga"]).sum()
            if impossible > 0:
                report["issues"].append(f"{impossible} records where FGM > FGA")

        # Check for unrealistic point totals (> 100 in a game)
        if "pts" in df.columns:
            unrealistic = (df["pts"] > 100).sum()
            if unrealistic > 0:
                report["warnings"].append(f"{unrealistic} records with > 100 points")

        return report

    def clean_player_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean player statistics DataFrame

        Args:
            df: Raw player stats DataFrame

        Returns:
            Cleaned DataFrame
        """
        df = df.copy()
        logger.info(f"Cleaning player stats: {len(df)} rows")

        # Validate first
        report = self.validate_player_stats(df)
        if report["issues"]:
            logger.warning(f"Data issues found: {report['issues']}")

        # Remove records with negative statistics
        stat_columns = ["pts", "ast", "reb", "stl", "blk"]
        for col in stat_columns:
            if col in df.columns:
                df = df[df[col] >= 0]

        # Fix impossible made > attempted
        if "fgm" in df.columns and "fga" in df.columns:
            df.loc[df["fgm"] > df["fga"], "fgm"] = df["fga"]

        if "ftm" in df.columns and "fta" in df.columns:
            df.loc[df["ftm"] > df["fta"], "ftm"] = df["fta"]

        if "fg3m" in df.columns and "fg3a" in df.columns:
            df.loc[df["fg3m"] > df["fg3a"], "fg3m"] = df["fg3a"]

        # Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df = self.handle_missing_values(df, strategy="zero", columns=numeric_cols.tolist())

        logger.info(f"Cleaning complete: {len(df)} rows remaining")

        return df

    def clean_game_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean game data DataFrame

        Args:
            df: Raw game DataFrame

        Returns:
            Cleaned DataFrame
        """
        df = df.copy()
        logger.info(f"Cleaning game data: {len(df)} rows")

        # Validate first
        report = self.validate_game_data(df)
        if report["issues"]:
            logger.warning(f"Data issues found: {report['issues']}")

        # Remove games with negative scores
        if "home_team_score" in df.columns and "visitor_team_score" in df.columns:
            df = df[(df["home_team_score"] >= 0) & (df["visitor_team_score"] >= 0)]

        # Remove duplicate game IDs
        if "id" in df.columns:
            df = df.drop_duplicates(subset=["id"], keep="first")

        # Remove games that aren't finished
        if "status" in df.columns:
            df = df[df["status"] == "Final"]

        logger.info(f"Cleaning complete: {len(df)} rows remaining")

        return df

    def generate_quality_report(self, df: pd.DataFrame, name: str = "Dataset") -> Dict[str, Any]:
        """
        Generate comprehensive data quality report

        Args:
            df: DataFrame to analyze
            name: Name of the dataset

        Returns:
            Dictionary with quality metrics
        """
        report = {
            "name": name,
            "rows": len(df),
            "columns": len(df.columns),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
            "missing_values": {},
            "duplicates": df.duplicated().sum(),
            "dtypes": df.dtypes.value_counts().to_dict()
        }

        # Missing values per column
        missing = df.isnull().sum()
        missing_pct = (missing / len(df) * 100).round(2)
        report["missing_values"] = {
            col: {"count": int(missing[col]), "percentage": float(missing_pct[col])}
            for col in df.columns if missing[col] > 0
        }

        # Numeric column statistics
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if not numeric_cols.empty:
            report["numeric_summary"] = df[numeric_cols].describe().to_dict()

        return report


# Example usage
if __name__ == "__main__":
    # Example with sample data
    import pandas as pd

    # Create sample player stats
    data = {
        "player_id": [1, 2, 3, 4, 5],
        "pts": [25, 30, -5, 15, 200],  # Has issues
        "ast": [5, 7, 3, None, 8],
        "reb": [10, 8, 6, 4, 12],
        "fgm": [10, 12, 5, 6, 15],
        "fga": [20, 25, 18, 5, 30]  # FGA < FGM for player 4
    }

    df = pd.DataFrame(data)

    cleaner = DataCleaner()

    # Validate
    report = cleaner.validate_player_stats(df)
    print("Validation Report:", report)

    # Clean
    clean_df = cleaner.clean_player_stats(df)
    print("\nCleaned Data:")
    print(clean_df)

    # Quality report
    quality = cleaner.generate_quality_report(clean_df, "Player Stats")
    print("\nQuality Report:", quality)
