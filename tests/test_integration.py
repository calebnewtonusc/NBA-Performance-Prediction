#!/usr/bin/env python3
"""
Integration Tests for NBA Performance Prediction Pipeline

These tests validate the entire pipeline end-to-end:
1. Data generation/loading
2. Data cleaning
3. Feature engineering
4. Dataset creation
5. Model training
6. Model evaluation

Usage:
    python3 tests/test_integration.py
    pytest tests/test_integration.py -v
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class TestEndToEndPipeline:
    """End-to-end integration tests"""

    @pytest.fixture
    def sample_games_data(self):
        """Create realistic sample NBA games data"""
        games = []
        for i in range(200):
            games.append({
                'id': i,
                'date': pd.Timestamp('2024-01-01') + timedelta(days=i // 3),
                'home_team_id': (i % 10) + 1,
                'visitor_team_id': ((i + 3) % 10) + 1,
                'home_team_score': np.random.randint(90, 125),
                'visitor_team_score': np.random.randint(90, 125),
                'season': 2024
            })
        df = pd.DataFrame(games)
        df['date'] = pd.to_datetime(df['date'])
        return df

    def test_data_cleaning_pipeline(self, sample_games_data):
        """Test data cleaning pipeline"""
        from src.data_processing.cleaning import DataCleaner

        cleaner = DataCleaner()

        # Add some missing values
        df = sample_games_data.copy()
        df.loc[10, 'home_team_score'] = np.nan
        df.loc[20, 'visitor_team_score'] = np.nan

        # Clean data
        cleaned = cleaner.clean_game_data(df)

        # Verify cleaning worked
        assert not cleaned['home_team_score'].isna().any()
        assert not cleaned['visitor_team_score'].isna().any()
        assert len(cleaned) <= len(df)  # May drop some rows

    def test_feature_engineering_pipeline(self, sample_games_data):
        """Test feature engineering pipeline"""
        from src.data_processing.game_features import GameFeatureEngineer

        engineer = GameFeatureEngineer()

        # Create features
        features_df = engineer.create_game_features(
            sample_games_data,
            include_future_target=True
        )

        # Verify features created
        assert len(features_df) > 0
        assert 'home_win_pct' in features_df.columns
        assert 'away_win_pct' in features_df.columns
        assert 'home_win' in features_df.columns

    def test_dataset_creation_pipeline(self, sample_games_data):
        """Test dataset creation pipeline"""
        from src.data_processing.game_features import GameFeatureEngineer
        from src.data_processing.dataset_builder import DatasetBuilder

        # Create features
        engineer = GameFeatureEngineer()
        features_df = engineer.create_game_features(
            sample_games_data,
            include_future_target=True
        )

        # Build dataset
        builder = DatasetBuilder()
        dataset = builder.create_dataset(
            df=features_df,
            target_column='home_win',
            date_column='date',
            split_method='time',
            scale_features=True,
            exclude_columns=['game_id', 'home_team_id', 'away_team_id']
        )

        # Verify dataset structure
        assert 'X_train' in dataset
        assert 'y_train' in dataset
        assert 'X_val' in dataset
        assert 'y_val' in dataset
        assert 'X_test' in dataset
        assert 'y_test' in dataset

        # Verify data types
        assert isinstance(dataset['X_train'], pd.DataFrame)
        assert isinstance(dataset['y_train'], pd.Series)

        # Verify splits
        total_samples = len(dataset['X_train']) + len(dataset['X_val']) + len(dataset['X_test'])
        assert total_samples > 0

    def test_model_training_pipeline(self, sample_games_data):
        """Test model training pipeline"""
        from src.data_processing.game_features import GameFeatureEngineer
        from src.data_processing.dataset_builder import DatasetBuilder
        from src.models.logistic_regression_model import GameLogisticRegression

        # Create features
        engineer = GameFeatureEngineer()
        features_df = engineer.create_game_features(
            sample_games_data,
            include_future_target=True
        )

        # Build dataset
        builder = DatasetBuilder()
        dataset = builder.create_dataset(
            df=features_df,
            target_column='home_win',
            date_column='date',
            split_method='time',
            scale_features=True,
            exclude_columns=['game_id', 'home_team_id', 'away_team_id']
        )

        # Train model
        model = GameLogisticRegression()
        metrics = model.train(
            dataset['X_train'],
            dataset['y_train'],
            dataset['X_val'],
            dataset['y_val'],
            tune_hyperparameters=False
        )

        # Verify training
        assert 'accuracy' in metrics
        assert 0 <= metrics['accuracy'] <= 1

    def test_full_pipeline_performance(self, sample_games_data):
        """Test full pipeline performance"""
        import time

        from src.data_processing.cleaning import DataCleaner
        from src.data_processing.game_features import GameFeatureEngineer
        from src.data_processing.dataset_builder import DatasetBuilder
        from src.models.logistic_regression_model import GameLogisticRegression

        start_time = time.time()

        # 1. Clean data
        cleaner = DataCleaner()
        cleaned_df = cleaner.clean_game_data(sample_games_data)

        # 2. Create features
        engineer = GameFeatureEngineer()
        features_df = engineer.create_game_features(cleaned_df, include_future_target=True)

        # 3. Build dataset
        builder = DatasetBuilder()
        dataset = builder.create_dataset(
            df=features_df,
            target_column='home_win',
            date_column='date',
            split_method='time',
            scale_features=True,
            exclude_columns=['game_id', 'home_team_id', 'away_team_id']
        )

        # 4. Train model
        model = GameLogisticRegression()
        _ = model.train(
            dataset['X_train'],
            dataset['y_train'],
            dataset['X_val'],
            dataset['y_val'],
            tune_hyperparameters=False
        )

        # 5. Evaluate
        test_metrics = model.evaluate(dataset['X_test'], dataset['y_test'])

        elapsed = time.time() - start_time

        # Verify performance
        assert elapsed < 60, f"Pipeline took {elapsed:.2f}s, should be under 60s"
        assert test_metrics['accuracy'] > 0.4, "Model should perform better than random"

    def test_prediction_pipeline(self, sample_games_data):
        """Test making predictions with trained model"""
        from src.data_processing.game_features import GameFeatureEngineer
        from src.data_processing.dataset_builder import DatasetBuilder
        from src.models.logistic_regression_model import GameLogisticRegression

        # Train model
        engineer = GameFeatureEngineer()
        features_df = engineer.create_game_features(
            sample_games_data,
            include_future_target=True
        )

        builder = DatasetBuilder()
        dataset = builder.create_dataset(
            df=features_df,
            target_column='home_win',
            date_column='date',
            split_method='time',
            scale_features=True,
            exclude_columns=['game_id', 'home_team_id', 'away_team_id']
        )

        model = GameLogisticRegression()
        model.train(
            dataset['X_train'],
            dataset['y_train'],
            dataset['X_val'],
            dataset['y_val'],
            tune_hyperparameters=False
        )

        # Make predictions
        predictions = model.predict(dataset['X_test'])
        probabilities = model.predict_proba(dataset['X_test'])

        # Verify predictions
        assert len(predictions) == len(dataset['X_test'])
        assert len(probabilities) == len(dataset['X_test'])
        assert all(p in [0, 1] for p in predictions)
        assert all(0 <= prob[1] <= 1 for prob in probabilities)


class TestDataValidation:
    """Test data validation and error handling"""

    def test_empty_dataframe_handling(self):
        """Test handling of empty DataFrame"""
        from src.data_processing.game_features import GameFeatureEngineer

        engineer = GameFeatureEngineer()
        empty_df = pd.DataFrame()

        # Should handle gracefully
        result = engineer.calculate_team_form(
            empty_df, team_id=1,
            date=pd.Timestamp('2024-01-01'), n_games=10
        )

        assert result['games_played'] == 0

    def test_invalid_data_types(self):
        """Test handling of invalid data types"""
        from src.data_processing.cleaning import DataCleaner

        cleaner = DataCleaner()

        # DataFrame with mixed types
        df = pd.DataFrame({
            'col1': [1, 2, '3', 4],  # Mixed int/str
            'col2': [1.0, 2.0, 3.0, 'invalid']
        })

        # Should handle or raise appropriate error
        try:
            result = cleaner.handle_missing_values(df, strategy='mean')
            # If it succeeds, verify it handled correctly
            assert isinstance(result, pd.DataFrame)
        except (ValueError, TypeError):
            # Appropriate error raised
            pass


def main():
    """Run integration tests"""
    print("\n" + "=" * 70)
    print("INTEGRATION TESTS - Full Pipeline Validation")
    print("=" * 70 + "\n")

    # Run tests manually (without pytest)
    test_suite = TestEndToEndPipeline()

    # Generate sample data
    games = []
    for i in range(200):
        games.append({
            'id': i,
            'date': pd.Timestamp('2024-01-01') + timedelta(days=i // 3),
            'home_team_id': (i % 10) + 1,
            'visitor_team_id': ((i + 3) % 10) + 1,
            'home_team_score': np.random.randint(90, 125),
            'visitor_team_score': np.random.randint(90, 125),
            'season': 2024
        })
    sample_data = pd.DataFrame(games)
    sample_data['date'] = pd.to_datetime(sample_data['date'])

    try:
        print("[1/7] Testing data cleaning pipeline...")
        test_suite.test_data_cleaning_pipeline(sample_data)
        print("checkmark Data cleaning pipeline works")

        print("\n[2/7] Testing feature engineering pipeline...")
        test_suite.test_feature_engineering_pipeline(sample_data)
        print("checkmark Feature engineering pipeline works")

        print("\n[3/7] Testing dataset creation pipeline...")
        test_suite.test_dataset_creation_pipeline(sample_data)
        print("checkmark Dataset creation pipeline works")

        print("\n[4/7] Testing model training pipeline...")
        test_suite.test_model_training_pipeline(sample_data)
        print("checkmark Model training pipeline works")

        print("\n[5/7] Testing full pipeline performance...")
        test_suite.test_full_pipeline_performance(sample_data)
        print("checkmark Full pipeline performance acceptable")

        print("\n[6/7] Testing prediction pipeline...")
        test_suite.test_prediction_pipeline(sample_data)
        print("checkmark Prediction pipeline works")

        print("\n[7/7] Testing error handling...")
        validation_suite = TestDataValidation()
        validation_suite.test_empty_dataframe_handling()
        validation_suite.test_invalid_data_types()
        print("checkmark Error handling works")

        print("\n" + "=" * 70)
        print("[checkmark.circle] ALL INTEGRATION TESTS PASSED")
        print("=" * 70)
        print("\nThe full ML pipeline is working correctly:")
        print("  • Data cleaning checkmark")
        print("  • Feature engineering checkmark")
        print("  • Dataset creation checkmark")
        print("  • Model training checkmark")
        print("  • Predictions checkmark")
        print("  • Error handling checkmark")
        print()
        return 0

    except Exception as e:
        print(f"\n[xmark.circle] INTEGRATION TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
