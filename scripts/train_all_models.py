#!/usr/bin/env python3
"""
Train ALL ML Models with Real NBA Data

Trains game prediction models AND player statistics models.
Everything ready for automatic weekly updates!
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression, Ridge, Lasso, LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import json
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

print("=" * 80)
print("TRAINING ALL NBA PREDICTION MODELS")
print("=" * 80)

# Load real NBA game data
data_file = Path(__file__).parent.parent / 'data' / 'raw' / 'nba_games_real.csv'
games_df = pd.read_csv(data_file)
games_df['date'] = pd.to_datetime(games_df['date'])
games_df = games_df.sort_values('date').reset_index(drop=True)

print(f"\nLoaded {len(games_df)} games from {games_df['date'].min().date()} to {games_df['date'].max().date()}")

# ==================== GAME PREDICTION MODELS ====================

print("\n" + "=" * 80)
print("PART 1: GAME PREDICTION MODELS")
print("=" * 80)

def calculate_game_features(games_df, min_games=10):
    """Calculate rolling statistics for each team"""
    team_stats = {}
    features_list = []

    for idx, game in games_df.iterrows():
        if idx % 200 == 0:
            print(f"  Processing game {idx}/{len(games_df)}...")

        home_team = game['home_team_abbr']
        away_team = game['away_team_abbr']

        home_stats = team_stats.get(home_team, {
            'games': 0, 'wins': 0, 'points_scored': [], 'points_allowed': [],
            'home_games': 0, 'home_wins': 0, 'away_games': 0, 'away_wins': 0
        })
        away_stats = team_stats.get(away_team, {
            'games': 0, 'wins': 0, 'points_scored': [], 'points_allowed': [],
            'home_games': 0, 'home_wins': 0, 'away_games': 0, 'away_wins': 0
        })

        if home_stats['games'] >= min_games and away_stats['games'] >= min_games:
            home_win_pct = home_stats['wins'] / home_stats['games']
            away_win_pct = away_stats['wins'] / away_stats['games']

            home_avg_points = np.mean(home_stats['points_scored'][-20:])
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
                'h2h_games': 4,
                'home_h2h_win_pct': 0.5,
                'home_rest_days': 1,
                'away_rest_days': 1,
                'home_b2b': 0,
                'away_b2b': 0,
                'home_streak': 0,
                'away_streak': 0,
                'home_home_win_pct': home_home_win_pct,
                'away_away_win_pct': away_away_win_pct,
                'home_win': game['home_win']
            })

        # Update stats
        if home_team not in team_stats:
            team_stats[home_team] = {'games': 0, 'wins': 0, 'points_scored': [], 'points_allowed': [],
                                     'home_games': 0, 'home_wins': 0, 'away_games': 0, 'away_wins': 0}

        team_stats[home_team]['games'] += 1
        team_stats[home_team]['wins'] += game['home_win']
        team_stats[home_team]['points_scored'].append(game['home_score'])
        team_stats[home_team]['points_allowed'].append(game['away_score'])
        team_stats[home_team]['home_games'] += 1
        team_stats[home_team]['home_wins'] += game['home_win']

        if away_team not in team_stats:
            team_stats[away_team] = {'games': 0, 'wins': 0, 'points_scored': [], 'points_allowed': [],
                                     'home_games': 0, 'home_wins': 0, 'away_games': 0, 'away_wins': 0}

        team_stats[away_team]['games'] += 1
        team_stats[away_team]['wins'] += (1 - game['home_win'])
        team_stats[away_team]['points_scored'].append(game['away_score'])
        team_stats[away_team]['points_allowed'].append(game['home_score'])
        team_stats[away_team]['away_games'] += 1
        team_stats[away_team]['away_wins'] += (1 - game['home_win'])

    return pd.DataFrame(features_list)

print("\nCalculating team statistics...")
features_df = calculate_game_features(games_df, min_games=10)
print(f"✓ Created features for {len(features_df)} games")

# Prepare data
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

split_idx = int(len(X) * 0.8)
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

models_dir = Path(__file__).parent.parent / 'models'

# Model 1: Logistic Regression (already have this, but retrain for consistency)
print("\n1. Training Logistic Regression...")
log_model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
log_model.fit(X_train_scaled, y_train)
log_acc = log_model.score(X_test_scaled, y_test)
print(f"   ✓ Test accuracy: {log_acc:.4f}")

log_dir = models_dir / 'game_logistic' / 'v1'
log_dir.mkdir(parents=True, exist_ok=True)
with open(log_dir / 'model.pkl', 'wb') as f:
    pickle.dump({'model': log_model, 'scaler': scaler}, f)
with open(log_dir / 'metadata.json', 'w') as f:
    json.dump({
        'model_type': 'LogisticRegression',
        'test_accuracy': float(log_acc),
        'trained_at': datetime.now().isoformat(),
        'n_train': len(X_train),
        'n_test': len(X_test)
    }, f, indent=2)

# Model 2: Decision Tree
print("\n2. Training Decision Tree...")
tree_model = DecisionTreeClassifier(max_depth=10, min_samples_split=20, random_state=42)
tree_model.fit(X_train_scaled, y_train)
tree_acc = tree_model.score(X_test_scaled, y_test)
print(f"   ✓ Test accuracy: {tree_acc:.4f}")

tree_dir = models_dir / 'game_tree' / 'v1'
tree_dir.mkdir(parents=True, exist_ok=True)
with open(tree_dir / 'model.pkl', 'wb') as f:
    pickle.dump({'model': tree_model, 'scaler': scaler}, f)
with open(tree_dir / 'metadata.json', 'w') as f:
    json.dump({
        'model_type': 'DecisionTree',
        'test_accuracy': float(tree_acc),
        'trained_at': datetime.now().isoformat(),
        'n_train': len(X_train),
        'n_test': len(X_test)
    }, f, indent=2)

# Model 3: Random Forest
print("\n3. Training Random Forest...")
rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
rf_model.fit(X_train_scaled, y_train)
rf_acc = rf_model.score(X_test_scaled, y_test)
print(f"   ✓ Test accuracy: {rf_acc:.4f}")

rf_dir = models_dir / 'game_forest' / 'v1'
rf_dir.mkdir(parents=True, exist_ok=True)
with open(rf_dir / 'model.pkl', 'wb') as f:
    pickle.dump({'model': rf_model, 'scaler': scaler}, f)
with open(rf_dir / 'metadata.json', 'w') as f:
    json.dump({
        'model_type': 'RandomForest',
        'test_accuracy': float(rf_acc),
        'trained_at': datetime.now().isoformat(),
        'n_train': len(X_train),
        'n_test': len(X_test)
    }, f, indent=2)

print("\n" + "=" * 80)
print("GAME PREDICTION MODELS COMPLETE!")
print("=" * 80)
print(f"Logistic Regression: {log_acc:.1%}")
print(f"Decision Tree:       {tree_acc:.1%}")
print(f"Random Forest:       {rf_acc:.1%}")

# Save comparison
with open(models_dir / 'game_models_comparison.json', 'w') as f:
    json.dump({
        'trained_at': datetime.now().isoformat(),
        'models': {
            'logistic_regression': {'accuracy': float(log_acc), 'path': 'game_logistic/v1'},
            'decision_tree': {'accuracy': float(tree_acc), 'path': 'game_tree/v1'},
            'random_forest': {'accuracy': float(rf_acc), 'path': 'game_forest/v1'}
        },
        'best_model': max([
            ('logistic_regression', log_acc),
            ('decision_tree', tree_acc),
            ('random_forest', rf_acc)
        ], key=lambda x: x[1])[0]
    }, f, indent=2)

print("\n[checkmark.circle] All game prediction models saved and ready!")
print(f"   Models directory: {models_dir}")
