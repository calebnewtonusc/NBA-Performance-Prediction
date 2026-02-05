#!/usr/bin/env python3
"""
Quick Prediction Example

Demonstrates how to make NBA game predictions with a trained model.

Usage:
    python3 examples/quick_prediction_example.py
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
from datetime import datetime


def main():
    """Run quick prediction example"""
    print("\n" + "=" * 70)
    print("NBA GAME PREDICTION - Quick Example")
    print("=" * 70)

    # 1. Load trained model
    print("\n[Step 1] Loading trained model...")
    from src.models.model_manager import ModelManager

    manager = ModelManager()

    try:
        model = manager.load_model('game_logistic', 'v1')
        print("✓ Model loaded successfully")
    except FileNotFoundError:
        print("⚠ No trained model found. Training sample model...")

        # Train a quick model with sample data
        from scripts.generate_sample_data import generate_sample_games
        from src.data_processing.game_features import GameFeatureEngineer
        from src.data_processing.dataset_builder import DatasetBuilder
        from src.models.logistic_regression_model import GameLogisticRegression

        # Generate sample data
        games_df = pd.DataFrame(generate_sample_games(200))

        # Create features
        engineer = GameFeatureEngineer()
        features_df = engineer.create_game_features(games_df, include_future_target=True)

        # Build dataset
        builder = DatasetBuilder()
        dataset = builder.create_dataset(
            df=features_df,
            target_column='home_win',
            date_column='date',
            split_method='time',
            scale_features=True,
            exclude_columns=['game_id', 'home_team_id', 'away_team_id', 'home_score', 'away_score']
        )

        # Train model
        model = GameLogisticRegression()
        model.train(
            dataset['X_train'],
            dataset['y_train'],
            dataset['X_val'],
            dataset['y_val'],
            tune_hyperparameters=False
        )

        # Save model
        test_metrics = model.evaluate(dataset['X_test'], dataset['y_test'])
        manager.save_model(model, 'game_logistic', 'v1', {'metrics': test_metrics})
        print("✓ Sample model trained and saved")

    # 2. Prepare game features
    print("\n[Step 2] Preparing game features...")

    # Example: Lakers vs Warriors game
    game_features = pd.DataFrame([{
        'home_win_pct': 0.650,       # Lakers winning 65% recently
        'away_win_pct': 0.550,       # Warriors winning 55% recently
        'home_avg_points': 112.5,    # Lakers scoring average
        'away_avg_points': 108.3,    # Warriors scoring average
        'home_avg_allowed': 105.2,   # Lakers defense
        'away_avg_allowed': 107.8,   # Warriors defense
        'home_point_diff': 7.3,      # Lakers point differential
        'away_point_diff': 0.5,      # Warriors point differential
        'h2h_games': 3,              # 3 recent head-to-head games
        'home_h2h_win_pct': 0.667,   # Lakers won 2/3
        'home_rest_days': 2,         # 2 days rest
        'away_rest_days': 1,         # 1 day rest (back-to-back)
        'home_b2b': 0,               # Not back-to-back
        'away_b2b': 1,               # Warriors on back-to-back
        'home_streak': 3,            # Lakers on 3-game win streak
        'away_streak': -1,           # Warriors lost last game
        'home_home_win_pct': 0.720,  # Lakers strong at home
        'away_away_win_pct': 0.480,  # Warriors weak on road
    }])

    print("✓ Game features prepared")
    print(f"\nMatchup: Lakers (Home) vs Warriors (Away)")
    print(f"Lakers recent form: {game_features['home_win_pct'].values[0]:.1%} wins")
    print(f"Warriors recent form: {game_features['away_win_pct'].values[0]:.1%} wins")

    # 3. Make prediction
    print("\n[Step 3] Making prediction...")

    prediction = model.predict(game_features)[0]
    probability = model.predict_proba(game_features)[0]

    print("\n" + "=" * 70)
    print("PREDICTION RESULT")
    print("=" * 70)

    winner = "Lakers (Home)" if prediction == 1 else "Warriors (Away)"
    confidence = probability[1] if prediction == 1 else probability[0]

    print(f"\nPredicted Winner: {winner}")
    print(f"Confidence: {confidence:.1%}")
    print(f"\nProbabilities:")
    print(f"  Lakers win:    {probability[1]:.1%}")
    print(f"  Warriors win:  {probability[0]:.1%}")

    # 4. Feature importance
    print("\n[Step 4] Key factors...")

    feature_importance = model.get_feature_importance(game_features.columns.tolist())
    top_features = feature_importance.head(5)

    print("\nTop 5 most important factors:")
    for idx, row in top_features.iterrows():
        print(f"  {row['feature']:.<30} {row['importance']:.4f}")

    print("\n" + "=" * 70)
    print("✅ PREDICTION COMPLETE")
    print("=" * 70)

    print("\n💡 TIP: Adjust the feature values above to predict different scenarios!")
    print()


if __name__ == "__main__":
    main()
