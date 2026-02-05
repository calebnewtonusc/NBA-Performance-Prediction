#!/usr/bin/env python3
"""
Train Model with Real NBA Data

Builds features from real game data and trains the prediction model.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

sys.path.append(str(Path(__file__).parent.parent))

print("Loading real NBA game data...")
data_file = Path(__file__).parent.parent / 'data' / 'raw' / 'nba_games_real.csv'
games_df = pd.read_csv(data_file)
games_df['date'] = pd.to_datetime(games_df['date'])
games_df = games_df.sort_values('date').reset_index(drop=True)

print(f"Loaded {len(games_df)} games from {games_df['date'].min().date()} to {games_df['date'].max().date()}")

# Calculate rolling team statistics
print("\nCalculating team statistics...")

def calculate_team_stats(games_df, min_games=10):
    """Calculate rolling statistics for each team"""

    team_stats = {}
    features_list = []

    for idx, game in games_df.iterrows():
        if idx % 200 == 0:
            print(f"  Processing game {idx}/{len(games_df)}...")

        home_team = game['home_team_abbr']
        away_team = game['away_team_abbr']

        # Get historical stats for both teams (up to this game, not including it)
        home_stats = team_stats.get(home_team, {
            'games': 0, 'wins': 0, 'points_scored': [], 'points_allowed': [],
            'home_games': 0, 'home_wins': 0
        })
        away_stats = team_stats.get(away_team, {
            'games': 0, 'wins': 0, 'points_scored': [], 'points_allowed': [],
            'away_games': 0, 'away_wins': 0
        })

        # Only create features if both teams have enough history
        if home_stats['games'] >= min_games and away_stats['games'] >= min_games:
            # Calculate features
            home_win_pct = home_stats['wins'] / home_stats['games']
            away_win_pct = away_stats['wins'] / away_stats['games']

            home_avg_points = np.mean(home_stats['points_scored'][-20:])  # Last 20 games
            away_avg_points = np.mean(away_stats['points_scored'][-20:])

            home_avg_allowed = np.mean(home_stats['points_allowed'][-20:])
            away_avg_allowed = np.mean(away_stats['points_allowed'][-20:])

            home_home_win_pct = home_stats['home_wins'] / home_stats['home_games'] if home_stats['home_games'] > 0 else 0.5
            away_away_win_pct = away_stats['away_wins'] / away_stats['away_games'] if away_stats['away_games'] > 0 else 0.5

            features_list.append({
                'game_id': game['game_id'],
                'date': game['date'],
                'home_team': home_team,
                'away_team': away_team,
                'home_win_pct': home_win_pct,
                'away_win_pct': away_win_pct,
                'home_avg_points': home_avg_points,
                'away_avg_points': away_avg_points,
                'home_avg_allowed': home_avg_allowed,
                'away_avg_allowed': away_avg_allowed,
                'home_point_diff': home_avg_points - home_avg_allowed,
                'away_point_diff': away_avg_points - away_avg_allowed,
                'home_home_win_pct': home_home_win_pct,
                'away_away_win_pct': away_away_win_pct,
                # Add default values for other features
                'h2h_games': 4,
                'home_h2h_win_pct': 0.5,
                'home_rest_days': 1,
                'away_rest_days': 1,
                'home_b2b': 0,
                'away_b2b': 0,
                'home_streak': 0,
                'away_streak': 0,
                # Target
                'home_win': game['home_win']
            })

        # Update team stats with this game's results
        # Home team
        if home_team not in team_stats:
            team_stats[home_team] = {
                'games': 0, 'wins': 0, 'points_scored': [], 'points_allowed': [],
                'home_games': 0, 'home_wins': 0, 'away_games': 0, 'away_wins': 0
            }

        team_stats[home_team]['games'] += 1
        team_stats[home_team]['wins'] += game['home_win']
        team_stats[home_team]['points_scored'].append(game['home_score'])
        team_stats[home_team]['points_allowed'].append(game['away_score'])
        team_stats[home_team]['home_games'] += 1
        team_stats[home_team]['home_wins'] += game['home_win']

        # Away team
        if away_team not in team_stats:
            team_stats[away_team] = {
                'games': 0, 'wins': 0, 'points_scored': [], 'points_allowed': [],
                'home_games': 0, 'home_wins': 0, 'away_games': 0, 'away_wins': 0
            }

        team_stats[away_team]['games'] += 1
        team_stats[away_team]['wins'] += (1 - game['home_win'])
        team_stats[away_team]['points_scored'].append(game['away_score'])
        team_stats[away_team]['points_allowed'].append(game['home_score'])
        team_stats[away_team]['away_games'] += 1
        team_stats[away_team]['away_wins'] += (1 - game['home_win'])

    return pd.DataFrame(features_list)

features_df = calculate_team_stats(games_df, min_games=10)
print(f"✓ Created features for {len(features_df)} games (after min_games filter)")

# Prepare training data
feature_columns = [
    'home_win_pct', 'away_win_pct',
    'home_avg_points', 'away_avg_points',
    'home_avg_allowed', 'away_avg_allowed',
    'home_point_diff', 'away_point_diff',
    'h2h_games', 'home_h2h_win_pct',
    'home_rest_days', 'away_rest_days',
    'home_b2b', 'away_b2b',
    'home_streak', 'away_streak',
    'home_home_win_pct', 'away_away_win_pct'
]

X = features_df[feature_columns].values
y = features_df['home_win'].values

print(f"\nDataset shape: X={X.shape}, y={y.shape}")
print(f"Home team wins: {y.mean():.1%}")

# Split data (chronological - last 20% for testing)
split_idx = int(len(X) * 0.8)
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

print(f"Training set: {len(X_train)} games")
print(f"Test set: {len(X_test)} games")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train logistic regression model
print("\nTraining Logistic Regression model...")
model = LogisticRegression(
    max_iter=1000,
    random_state=42,
    class_weight='balanced'  # Handle any class imbalance
)
model.fit(X_train_scaled, y_train)

# Evaluate
train_acc = model.score(X_train_scaled, y_train)
test_acc = model.score(X_test_scaled, y_test)

print(f"✓ Training accuracy: {train_acc:.4f}")
print(f"✓ Test accuracy: {test_acc:.4f}")

# Check prediction probabilities distribution
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
print(f"\nPrediction confidence distribution:")
print(f"  Mean: {y_pred_proba.mean():.3f}")
print(f"  Std: {y_pred_proba.std():.3f}")
print(f"  Min: {y_pred_proba.min():.3f}")
print(f"  Max: {y_pred_proba.max():.3f}")
print(f"  Predictions > 99%: {(y_pred_proba > 0.99).sum()} / {len(y_pred_proba)}")
print(f"  Predictions 50-70%: {((y_pred_proba > 0.5) & (y_pred_proba < 0.7)).sum()} / {len(y_pred_proba)}")

# Save model
print("\nSaving model...")
models_dir = Path(__file__).parent.parent / 'models' / 'game_logistic' / 'v1'
models_dir.mkdir(parents=True, exist_ok=True)

model_file = models_dir / 'model.pkl'
with open(model_file, 'wb') as f:
    # Save both model and scaler
    pickle.dump({'model': model, 'scaler': scaler}, f)

print(f"✓ Model saved to {model_file}")

# Save metadata
import json
metadata = {
    'train_accuracy': float(train_acc),
    'test_accuracy': float(test_acc),
    'n_train_games': int(len(X_train)),
    'n_test_games': int(len(X_test)),
    'date_range': f"{features_df['date'].min()} to {features_df['date'].max()}",
    'trained_on': 'real_nba_data',
    'home_win_rate': float(y.mean())
}

metadata_file = models_dir / 'metadata.json'
with open(metadata_file, 'w') as f:
    json.dump(metadata, f, indent=2, default=str)

print(f"✓ Metadata saved to {metadata_file}")
print("\n✅ Model training complete with REAL NBA data!")
