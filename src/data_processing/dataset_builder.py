"""
Dataset Builder Module

This module handles creating train/validation/test splits and
preparing datasets for model training:
- Time-based splitting (no data leakage)
- Feature scaling and normalization
- Dataset versioning
- Data export to various formats

Usage:
    from src.data_processing.dataset_builder import DatasetBuilder

    builder = DatasetBuilder()
    X_train, X_val, X_test, y_train, y_val, y_test = builder.create_train_test_split(df)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, List, Optional, Dict, Any
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import json
from datetime import datetime
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class DatasetBuilder:
    """Build and manage train/validation/test datasets"""

    def __init__(self, output_dir: str = "data/processed"):
        """
        Initialize the dataset builder

        Args:
            output_dir: Directory to save processed datasets
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.scaler = None
        self.feature_names = None

    def create_time_based_split(
        self,
        df: pd.DataFrame,
        date_column: str,
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Create time-based train/validation/test split

        This prevents data leakage by ensuring training data comes before
        validation and test data chronologically.

        Args:
            df: Input DataFrame
            date_column: Column containing dates
            train_ratio: Proportion for training set
            val_ratio: Proportion for validation set
            test_ratio: Proportion for test set

        Returns:
            Tuple of (train_df, val_df, test_df)
        """
        if abs(train_ratio + val_ratio + test_ratio - 1.0) >= 0.01:
            raise ValueError("Ratios must sum to 1.0")

        # Sort by date
        df = df.sort_values(date_column).reset_index(drop=True)

        # Calculate split indices
        n = len(df)
        train_end = int(n * train_ratio)
        val_end = int(n * (train_ratio + val_ratio))

        # Split
        train_df = df.iloc[:train_end].copy()
        val_df = df.iloc[train_end:val_end].copy()
        test_df = df.iloc[val_end:].copy()

        logger.info(f"Time-based split: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")
        logger.info(f"Train dates: {train_df[date_column].min()} to {train_df[date_column].max()}")
        logger.info(f"Val dates: {val_df[date_column].min()} to {val_df[date_column].max()}")
        logger.info(f"Test dates: {test_df[date_column].min()} to {test_df[date_column].max()}")

        return train_df, val_df, test_df

    def create_random_split(
        self,
        df: pd.DataFrame,
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        random_state: int = 42
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Create random train/validation/test split

        Args:
            df: Input DataFrame
            train_ratio: Proportion for training set
            val_ratio: Proportion for validation set
            test_ratio: Proportion for test set
            random_state: Random seed

        Returns:
            Tuple of (train_df, val_df, test_df)
        """
        if abs(train_ratio + val_ratio + test_ratio - 1.0) >= 0.01:
            raise ValueError("Ratios must sum to 1.0")

        # First split: train vs (val + test)
        train_df, temp_df = train_test_split(
            df,
            train_size=train_ratio,
            random_state=random_state
        )

        # Second split: val vs test
        val_ratio_adjusted = val_ratio / (val_ratio + test_ratio)
        val_df, test_df = train_test_split(
            temp_df,
            train_size=val_ratio_adjusted,
            random_state=random_state
        )

        logger.info(f"Random split: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")

        return train_df, val_df, test_df

    def prepare_features_and_target(
        self,
        df: pd.DataFrame,
        target_column: str,
        feature_columns: Optional[List[str]] = None,
        exclude_columns: Optional[List[str]] = None
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Separate features and target variable

        Args:
            df: Input DataFrame
            target_column: Name of target column
            feature_columns: Specific columns to use as features (None = all except target)
            exclude_columns: Columns to exclude from features

        Returns:
            Tuple of (X, y)
        """
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in DataFrame")

        y = df[target_column].copy()

        if feature_columns is not None:
            X = df[feature_columns].copy()
        else:
            # Use all columns except target and excluded columns
            exclude = [target_column]
            if exclude_columns:
                exclude.extend(exclude_columns)

            X = df.drop(columns=exclude, errors="ignore").copy()

        # Only keep numeric columns
        X = X.select_dtypes(include=[np.number])

        self.feature_names = X.columns.tolist()

        logger.info(f"Prepared features: {X.shape[1]} columns, {X.shape[0]} rows")

        return X, y

    def scale_features(
        self,
        X_train: pd.DataFrame,
        X_val: Optional[pd.DataFrame] = None,
        X_test: Optional[pd.DataFrame] = None,
        method: str = "standard"
    ) -> Tuple:
        """
        Scale features using training data statistics

        Args:
            X_train: Training features
            X_val: Validation features (optional)
            X_test: Test features (optional)
            method: Scaling method ('standard' or 'minmax')

        Returns:
            Tuple of scaled dataframes (train, val, test)
        """
        if method == "standard":
            self.scaler = StandardScaler()
        elif method == "minmax":
            self.scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown scaling method: {method}")

        # Fit on training data only
        X_train_scaled = pd.DataFrame(
            self.scaler.fit_transform(X_train),
            columns=X_train.columns,
            index=X_train.index
        )

        logger.info(f"Scaled features using {method} scaling")

        # Transform validation and test data
        results = [X_train_scaled]

        if X_val is not None:
            X_val_scaled = pd.DataFrame(
                self.scaler.transform(X_val),
                columns=X_val.columns,
                index=X_val.index
            )
            results.append(X_val_scaled)

        if X_test is not None:
            X_test_scaled = pd.DataFrame(
                self.scaler.transform(X_test),
                columns=X_test.columns,
                index=X_test.index
            )
            results.append(X_test_scaled)

        return tuple(results)

    def create_dataset(
        self,
        df: pd.DataFrame,
        target_column: str,
        date_column: Optional[str] = None,
        split_method: str = "time",
        scale_features: bool = True,
        scaling_method: str = "standard",
        exclude_columns: Optional[List[str]] = None,
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15
    ) -> Dict[str, Any]:
        """
        Complete dataset creation pipeline

        Args:
            df: Input DataFrame with features and target
            target_column: Name of target column
            date_column: Column for time-based splitting (required if split_method='time')
            split_method: 'time' or 'random'
            scale_features: Whether to scale features
            scaling_method: 'standard' or 'minmax'
            exclude_columns: Columns to exclude from features
            train_ratio: Training set proportion
            val_ratio: Validation set proportion
            test_ratio: Test set proportion

        Returns:
            Dictionary with all dataset components
        """
        logger.info("Creating dataset...")

        # Split into train/val/test
        if split_method == "time":
            if date_column is None:
                raise ValueError("date_column required for time-based splitting")
            train_df, val_df, test_df = self.create_time_based_split(
                df, date_column, train_ratio, val_ratio, test_ratio
            )
        else:
            train_df, val_df, test_df = self.create_random_split(
                df, train_ratio, val_ratio, test_ratio
            )

        # Prepare features and targets
        if exclude_columns is None:
            exclude_columns = []
        if date_column:
            exclude_columns.append(date_column)

        X_train, y_train = self.prepare_features_and_target(train_df, target_column, exclude_columns=exclude_columns)
        X_val, y_val = self.prepare_features_and_target(val_df, target_column, exclude_columns=exclude_columns)
        X_test, y_test = self.prepare_features_and_target(test_df, target_column, exclude_columns=exclude_columns)

        # Scale features
        if scale_features:
            X_train, X_val, X_test = self.scale_features(
                X_train, X_val, X_test, method=scaling_method
            )

        dataset = {
            "X_train": X_train,
            "X_val": X_val,
            "X_test": X_test,
            "y_train": y_train,
            "y_val": y_val,
            "y_test": y_test,
            "feature_names": self.feature_names,
            "target_name": target_column,
            "scaler": self.scaler
        }

        logger.info("Dataset creation complete!")

        return dataset

    def save_dataset(
        self,
        dataset: Dict[str, Any],
        name: str,
        version: str = "v1"
    ):
        """
        Save dataset to disk

        Args:
            dataset: Dataset dictionary from create_dataset()
            name: Dataset name (e.g., 'game_predictions')
            version: Version string
        """
        dataset_dir = self.output_dir / name / version
        dataset_dir.mkdir(parents=True, exist_ok=True)

        # Save data splits
        dataset["X_train"].to_csv(dataset_dir / "X_train.csv", index=False)
        dataset["X_val"].to_csv(dataset_dir / "X_val.csv", index=False)
        dataset["X_test"].to_csv(dataset_dir / "X_test.csv", index=False)

        dataset["y_train"].to_csv(dataset_dir / "y_train.csv", index=False, header=["target"])
        dataset["y_val"].to_csv(dataset_dir / "y_val.csv", index=False, header=["target"])
        dataset["y_test"].to_csv(dataset_dir / "y_test.csv", index=False, header=["target"])

        # Save metadata
        metadata = {
            "name": name,
            "version": version,
            "created_at": datetime.now().isoformat(),
            "feature_names": dataset["feature_names"],
            "target_name": dataset["target_name"],
            "train_samples": len(dataset["X_train"]),
            "val_samples": len(dataset["X_val"]),
            "test_samples": len(dataset["X_test"]),
            "n_features": len(dataset["feature_names"])
        }

        with open(dataset_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Saved dataset to {dataset_dir}")

    def load_dataset(
        self,
        name: str,
        version: str = "v1"
    ) -> Dict[str, Any]:
        """
        Load dataset from disk

        Args:
            name: Dataset name
            version: Version string

        Returns:
            Dataset dictionary
        """
        dataset_dir = self.output_dir / name / version

        if not dataset_dir.exists():
            raise ValueError(f"Dataset not found: {dataset_dir}")

        # Load data splits
        X_train = pd.read_csv(dataset_dir / "X_train.csv")
        X_val = pd.read_csv(dataset_dir / "X_val.csv")
        X_test = pd.read_csv(dataset_dir / "X_test.csv")

        y_train = pd.read_csv(dataset_dir / "y_train.csv")["target"]
        y_val = pd.read_csv(dataset_dir / "y_val.csv")["target"]
        y_test = pd.read_csv(dataset_dir / "y_test.csv")["target"]

        # Load metadata
        with open(dataset_dir / "metadata.json", "r") as f:
            metadata = json.load(f)

        dataset = {
            "X_train": X_train,
            "X_val": X_val,
            "X_test": X_test,
            "y_train": y_train,
            "y_val": y_val,
            "y_test": y_test,
            "feature_names": metadata["feature_names"],
            "target_name": metadata["target_name"]
        }

        logger.info(f"Loaded dataset from {dataset_dir}")

        return dataset

    def generate_dataset_report(
        self,
        dataset: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate summary report for a dataset

        Args:
            dataset: Dataset dictionary

        Returns:
            Report dictionary
        """
        report = {
            "summary": {
                "n_features": len(dataset["feature_names"]),
                "train_samples": len(dataset["X_train"]),
                "val_samples": len(dataset["X_val"]),
                "test_samples": len(dataset["X_test"]),
                "total_samples": len(dataset["X_train"]) + len(dataset["X_val"]) + len(dataset["X_test"])
            },
            "target_distribution": {
                "train": {
                    "mean": float(dataset["y_train"].mean()),
                    "std": float(dataset["y_train"].std()),
                    "min": float(dataset["y_train"].min()),
                    "max": float(dataset["y_train"].max())
                },
                "val": {
                    "mean": float(dataset["y_val"].mean()),
                    "std": float(dataset["y_val"].std()),
                    "min": float(dataset["y_val"].min()),
                    "max": float(dataset["y_val"].max())
                },
                "test": {
                    "mean": float(dataset["y_test"].mean()),
                    "std": float(dataset["y_test"].std()),
                    "min": float(dataset["y_test"].min()),
                    "max": float(dataset["y_test"].max())
                }
            },
            "feature_names": dataset["feature_names"]
        }

        return report


# Example usage
if __name__ == "__main__":
    print("Dataset Builder - Ready for use!")
    print("Load your processed features and call create_dataset() to build train/val/test splits")
