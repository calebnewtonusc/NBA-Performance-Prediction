#!/usr/bin/env python3
"""
Memory Profiling Script

Profile memory usage of NBA prediction pipeline to identify optimization opportunities.

Usage:
    python3 scripts/profile_memory.py

Requirements:
    pip install memory_profiler matplotlib
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from memory_profiler import profile
import gc


def create_large_dataset(n_games=10000):
    """Create large dataset for memory profiling"""
    print(f"Generating {n_games} games...")
    games = []
    for i in range(n_games):
        games.append({
            'id': i,
            'date': pd.Timestamp('2024-01-01') + timedelta(days=i // 5),
            'home_team_id': (i % 30) + 1,
            'visitor_team_id': ((i + 1) % 30) + 1,
            'home_team_score': np.random.randint(85, 125),
            'visitor_team_score': np.random.randint(85, 125)
        })
    df = pd.DataFrame(games)
    df['date'] = pd.to_datetime(df['date'])
    return df


@profile
def profile_data_cleaning():
    """Profile data cleaning memory usage"""
    print("\n[1/4] Profiling Data Cleaning...")
    from src.data_processing.cleaning import DataCleaner

    df = create_large_dataset(n_games=5000)
    cleaner = DataCleaner()

    # Add missing values
    df.loc[::100, 'home_team_score'] = np.nan

    # Clean data
    cleaned = cleaner.clean_game_data(df)

    del df, cleaned
    gc.collect()

    print("✓ Data cleaning profiling complete")


@profile
def profile_feature_engineering():
    """Profile feature engineering memory usage"""
    print("\n[2/4] Profiling Feature Engineering...")
    from src.data_processing.game_features import GameFeatureEngineer

    df = create_large_dataset(n_games=5000)
    engineer = GameFeatureEngineer()

    # Create features
    features = engineer.create_game_features(df, include_future_target=True)

    del df, features
    gc.collect()

    print("✓ Feature engineering profiling complete")


@profile
def profile_dataset_creation():
    """Profile dataset creation memory usage"""
    print("\n[3/4] Profiling Dataset Creation...")
    from src.data_processing.game_features import GameFeatureEngineer
    from src.data_processing.dataset_builder import DatasetBuilder

    df = create_large_dataset(n_games=5000)
    engineer = GameFeatureEngineer()
    features = engineer.create_game_features(df, include_future_target=True)

    builder = DatasetBuilder()
    dataset = builder.create_dataset(
        df=features,
        target_column='home_win',
        date_column='date',
        split_method='time',
        scale_features=True,
        exclude_columns=['game_id', 'home_team_id', 'away_team_id']
    )

    del df, features, dataset
    gc.collect()

    print("✓ Dataset creation profiling complete")


@profile
def profile_model_training():
    """Profile model training memory usage"""
    print("\n[4/4] Profiling Model Training...")
    from src.data_processing.game_features import GameFeatureEngineer
    from src.data_processing.dataset_builder import DatasetBuilder
    from src.models.logistic_regression_model import GameLogisticRegression

    df = create_large_dataset(n_games=1000)
    engineer = GameFeatureEngineer()
    features = engineer.create_game_features(df, include_future_target=True)

    builder = DatasetBuilder()
    dataset = builder.create_dataset(
        df=features,
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

    del df, features, dataset, model
    gc.collect()

    print("✓ Model training profiling complete")


def main():
    """Run memory profiling"""
    print("\n" + "=" * 70)
    print("MEMORY PROFILING - NBA Performance Prediction")
    print("=" * 70)
    print("\nThis will profile memory usage of the full pipeline.")
    print("Output will show line-by-line memory increments.\n")

    import sys
    import tracemalloc

    # Start memory tracking
    tracemalloc.start()

    try:
        # Profile each component
        profile_data_cleaning()
        profile_feature_engineering()
        profile_dataset_creation()
        profile_model_training()

        # Get memory statistics
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print("\n" + "=" * 70)
        print("MEMORY USAGE SUMMARY")
        print("=" * 70)
        print(f"Current Memory: {current / 1024 / 1024:.2f} MB")
        print(f"Peak Memory:    {peak / 1024 / 1024:.2f} MB")
        print("=" * 70)

        # Recommendations
        print("\n[chart.bar.fill] MEMORY OPTIMIZATION RECOMMENDATIONS:")
        if peak / 1024 / 1024 > 1000:
            print("  ⚠ High memory usage detected (>1GB)")
            print("  • Consider batch processing for large datasets")
            print("  • Use data streaming instead of loading all at once")
            print("  • Optimize DataFrame dtypes (use int32 vs int64)")
        elif peak / 1024 / 1024 > 500:
            print("  ✓ Moderate memory usage (500MB-1GB)")
            print("  • Current implementation is acceptable")
            print("  • Consider optimization for very large datasets")
        else:
            print("  [checkmark.circle] Excellent memory efficiency (<500MB)")
            print("  • Memory usage is well optimized")

        print("\n[lightbulb.fill] TIP: Run with mprof for graphical visualization:")
        print("  mprof run scripts/profile_memory.py")
        print("  mprof plot")
        print()

    except Exception as e:
        print(f"\n[xmark.circle] Profiling failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
