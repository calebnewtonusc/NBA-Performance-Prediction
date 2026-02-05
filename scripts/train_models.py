#!/usr/bin/env python3
"""
Automated Model Training Script

Train all NBA prediction models on collected data.

Usage:
    python scripts/train_models.py --all
    python scripts/train_models.py --game-models
    python scripts/train_models.py --player-models
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.data_processing.game_features import GameFeatureEngineer
from src.data_processing.player_features import PlayerFeatureEngineer
from src.data_processing.dataset_builder import DatasetBuilder
from src.data_processing.cleaning import DataCleaner
from src.models.logistic_regression_model import GameLogisticRegression
from src.models.decision_tree_model import GameDecisionTree
from src.models.random_forest_model import GameRandomForest
from src.models.linear_regression_model import PlayerLinearRegression
from src.models.ridge_lasso_regression import PlayerRidgeRegression, PlayerLassoRegression
from src.models.multi_output_regression import PlayerMultiOutputRegression
from src.models.model_manager import ModelManager
from src.evaluation.model_comparison import ModelComparison
from src.utils.data_loader import load_games_as_dataframe, load_player_stats_as_dataframe
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def train_game_models():
    """Train all game prediction models"""
    logger.info("=" * 60)
    logger.info("TRAINING GAME PREDICTION MODELS")
    logger.info("=" * 60)

    # Load and prepare data
    logger.info("Loading game data...")
    try:
        games_df = load_games_as_dataframe(season=2023)
    except:
        logger.warning("Could not load real data, using sample data...")
        # Generate sample data if real data doesn't exist
        from scripts.generate_sample_data import generate_sample_games
        import pandas as pd
        games_df = pd.DataFrame(generate_sample_games(200))

    logger.info(f"Loaded {len(games_df)} games")

    # Clean data
    cleaner = DataCleaner()
    games_df = cleaner.clean_game_data(games_df)
    logger.info(f"Cleaned data: {len(games_df)} games remaining")

    # Engineer features
    logger.info("Engineering features...")
    engineer = GameFeatureEngineer()
    features_df = engineer.create_game_features(games_df)
    logger.info(f"Created {len(features_df.columns)} features")

    # Build dataset
    logger.info("Building train/val/test datasets...")
    builder = DatasetBuilder()
    dataset = builder.create_dataset(
        df=features_df,
        target_column='home_win',
        date_column='date',
        split_method='time',
        scale_features=True,
        exclude_columns=['game_id', 'home_team_id', 'away_team_id', 'home_score', 'away_score']
    )

    # Save dataset
    builder.save_dataset(dataset, name='game_predictions', version='v1')
    logger.info("✓ Dataset saved")

    # Initialize model manager
    manager = ModelManager()

    # Train models
    logger.info("\n" + "=" * 60)
    logger.info("1. Training Logistic Regression...")
    logger.info("=" * 60)

    log_model = GameLogisticRegression()
    log_metrics = log_model.train(
        dataset['X_train'],
        dataset['y_train'],
        dataset['X_val'],
        dataset['y_val']
    )
    log_test_metrics = log_model.evaluate(dataset['X_test'], dataset['y_test'])
    manager.save_model(log_model, 'game_logistic', 'v1', {'metrics': log_test_metrics})
    logger.info(f"✓ Logistic Regression - Accuracy: {log_test_metrics['accuracy']:.4f}")

    logger.info("\n" + "=" * 60)
    logger.info("2. Training Decision Tree...")
    logger.info("=" * 60)

    tree_model = GameDecisionTree()
    tree_metrics = tree_model.train(
        dataset['X_train'],
        dataset['y_train'],
        dataset['X_val'],
        dataset['y_val'],
        tune_hyperparameters=False  # Skip tuning for speed
    )
    tree_test_metrics = tree_model.evaluate(dataset['X_test'], dataset['y_test'])
    manager.save_model(tree_model, 'game_tree', 'v1', {'metrics': tree_test_metrics})
    logger.info(f"✓ Decision Tree - Accuracy: {tree_test_metrics['accuracy']:.4f}")

    logger.info("\n" + "=" * 60)
    logger.info("3. Training Random Forest...")
    logger.info("=" * 60)

    rf_model = GameRandomForest()
    rf_metrics = rf_model.train(
        dataset['X_train'],
        dataset['y_train'],
        dataset['X_val'],
        dataset['y_val'],
        tune_hyperparameters=False  # Skip tuning for speed
    )
    rf_test_metrics = rf_model.evaluate(dataset['X_test'], dataset['y_test'])
    manager.save_model(rf_model, 'game_forest', 'v1', {'metrics': rf_test_metrics})
    logger.info(f"✓ Random Forest - Accuracy: {rf_test_metrics['accuracy']:.4f}")

    # Compare models
    logger.info("\n" + "=" * 60)
    logger.info("MODEL COMPARISON")
    logger.info("=" * 60)

    comparison = ModelComparison(task_type='classification')
    comparison.add_model('Logistic Regression', log_model, dataset['X_test'], dataset['y_test'])
    comparison.add_model('Decision Tree', tree_model, dataset['X_test'], dataset['y_test'])
    comparison.add_model('Random Forest', rf_model, dataset['X_test'], dataset['y_test'])

    results = comparison.compare_all()
    print("\n")
    print(results)

    best_name, best_model = comparison.get_best_model()
    logger.info(f"\n✓ Best model: {best_name}")

    # Set best as production
    if best_name == 'Logistic Regression':
        manager.set_production_model('game_logistic', 'v1')
    elif best_name == 'Decision Tree':
        manager.set_production_model('game_tree', 'v1')
    else:
        manager.set_production_model('game_forest', 'v1')

    logger.info("✓ Game models training complete!")


def train_player_models():
    """Train all player statistics prediction models"""
    logger.info("\n" + "=" * 60)
    logger.info("TRAINING PLAYER STATISTICS MODELS")
    logger.info("=" * 60)

    # Load and prepare data
    logger.info("Loading player stats data...")
    try:
        stats_df = load_player_stats_as_dataframe(season=2023)
    except:
        logger.warning("Could not load real data, using sample data...")
        # Generate sample data if real data doesn't exist
        from scripts.generate_sample_data import generate_sample_player_stats
        import pandas as pd
        stats_df = pd.DataFrame(generate_sample_player_stats(100))

    logger.info(f"Loaded {len(stats_df)} player stat records")

    # Clean data
    cleaner = DataCleaner()
    stats_df = cleaner.clean_player_stats(stats_df)
    logger.info(f"Cleaned data: {len(stats_df)} records remaining")

    # Engineer features
    logger.info("Engineering features...")
    engineer = PlayerFeatureEngineer()
    features_df = engineer.create_player_features(stats_df, include_target=True, target_column='pts')
    logger.info(f"Created {len(features_df.columns)} features")

    # Build dataset
    logger.info("Building train/val/test datasets...")
    builder = DatasetBuilder()

    # Single output dataset (points)
    dataset_single = builder.create_dataset(
        df=features_df,
        target_column='target',
        date_column='game_date',
        split_method='time',
        scale_features=True,
        exclude_columns=['player_id', 'game_id']
    )

    # Save dataset
    builder.save_dataset(dataset_single, name='player_points', version='v1')

    # Initialize model manager
    manager = ModelManager()

    # Train Linear Regression
    logger.info("\n" + "=" * 60)
    logger.info("1. Training Linear Regression...")
    logger.info("=" * 60)

    linear_model = PlayerLinearRegression()
    linear_model.train(
        dataset_single['X_train'],
        dataset_single['y_train'],
        dataset_single['X_val'],
        dataset_single['y_val']
    )
    linear_metrics = linear_model.evaluate(dataset_single['X_test'], dataset_single['y_test'])
    manager.save_model(linear_model, 'player_linear', 'v1', {'metrics': linear_metrics})
    logger.info(f"✓ Linear Regression - MAE: {linear_metrics['mae']:.2f}, R²: {linear_metrics['r2']:.4f}")

    # Train Ridge Regression
    logger.info("\n" + "=" * 60)
    logger.info("2. Training Ridge Regression...")
    logger.info("=" * 60)

    ridge_model = PlayerRidgeRegression()
    ridge_model.train(
        dataset_single['X_train'],
        dataset_single['y_train'],
        dataset_single['X_val'],
        dataset_single['y_val'],
        tune_alpha=False
    )
    ridge_metrics = ridge_model.evaluate(dataset_single['X_test'], dataset_single['y_test'])
    manager.save_model(ridge_model, 'player_ridge', 'v1', {'metrics': ridge_metrics})
    logger.info(f"✓ Ridge Regression - MAE: {ridge_metrics['mae']:.2f}, R²: {ridge_metrics['r2']:.4f}")

    # Train Lasso Regression
    logger.info("\n" + "=" * 60)
    logger.info("3. Training Lasso Regression...")
    logger.info("=" * 60)

    lasso_model = PlayerLassoRegression()
    lasso_model.train(
        dataset_single['X_train'],
        dataset_single['y_train'],
        dataset_single['X_val'],
        dataset_single['y_val'],
        tune_alpha=False
    )
    lasso_metrics = lasso_model.evaluate(dataset_single['X_test'], dataset_single['y_test'])
    manager.save_model(lasso_model, 'player_lasso', 'v1', {'metrics': lasso_metrics})
    logger.info(f"✓ Lasso Regression - MAE: {lasso_metrics['mae']:.2f}, R²: {lasso_metrics['r2']:.4f}")
    logger.info(f"  Selected {len(lasso_model.get_selected_features())} features")

    # Compare models
    logger.info("\n" + "=" * 60)
    logger.info("MODEL COMPARISON")
    logger.info("=" * 60)

    comparison = ModelComparison(task_type='regression')
    comparison.add_model('Linear Regression', linear_model, dataset_single['X_test'], dataset_single['y_test'])
    comparison.add_model('Ridge Regression', ridge_model, dataset_single['X_test'], dataset_single['y_test'])
    comparison.add_model('Lasso Regression', lasso_model, dataset_single['X_test'], dataset_single['y_test'])

    results = comparison.compare_all()
    print("\n")
    print(results)

    best_name, best_model = comparison.get_best_model('mae')
    logger.info(f"\n✓ Best model: {best_name}")

    logger.info("✓ Player models training complete!")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Train NBA prediction models"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Train all models"
    )

    parser.add_argument(
        "--game-models",
        action="store_true",
        help="Train game prediction models only"
    )

    parser.add_argument(
        "--player-models",
        action="store_true",
        help="Train player statistics models only"
    )

    args = parser.parse_args()

    # Default to all if nothing specified
    if not (args.all or args.game_models or args.player_models):
        args.all = True

    try:
        if args.all or args.game_models:
            train_game_models()

        if args.all or args.player_models:
            train_player_models()

        logger.info("\n" + "=" * 60)
        logger.info("✓ ALL TRAINING COMPLETE!")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
