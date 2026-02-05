#!/usr/bin/env python3
"""
Train Player Prediction Models (Linear/Ridge/Lasso Regression)

Uses player statistics to predict points, rebounds, assists.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import json
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

print("=" * 80)
print("TRAINING PLAYER PREDICTION MODELS")
print("=" * 80)

# Generate realistic synthetic player data
# (In production, this would come from real NBA API data)
print("\nGenerating synthetic player statistics...")

np.random.seed(42)
n_games = 1000

# Generate features
data = {
    'minutes_played': np.random.uniform(15, 38, n_games),
    'games_played_last_5': np.random.randint(3, 6, n_games),
    'avg_points_last_5': np.random.uniform(10, 30, n_games),
    'avg_assists_last_5': np.random.uniform(2, 10, n_games),
    'avg_rebounds_last_5': np.random.uniform(3, 12, n_games),
    'field_goal_pct_last_5': np.random.uniform(0.35, 0.55, n_games),
    'three_point_pct_last_5': np.random.uniform(0.25, 0.45, n_games),
    'free_throw_pct_last_5': np.random.uniform(0.70, 0.90, n_games),
    'opponent_defensive_rating': np.random.uniform(105, 120, n_games),
    'home_game': np.random.randint(0, 2, n_games),
}

df = pd.DataFrame(data)

# Generate correlated target variables (points)
# Points are correlated with minutes, past performance, shooting %
df['points'] = (
    df['minutes_played'] * 0.5 +
    df['avg_points_last_5'] * 0.4 +
    df['field_goal_pct_last_5'] * 20 +
    df['three_point_pct_last_5'] * 10 +
    np.random.normal(0, 3, n_games)  # Add noise
).clip(0, 50)

# Generate assists (correlated with minutes and past assists)
df['assists'] = (
    df['minutes_played'] * 0.15 +
    df['avg_assists_last_5'] * 0.5 +
    np.random.normal(0, 1.5, n_games)
).clip(0, 15)

# Generate rebounds (correlated with minutes and past rebounds)
df['rebounds'] = (
    df['minutes_played'] * 0.2 +
    df['avg_rebounds_last_5'] * 0.4 +
    np.random.normal(0, 2, n_games)
).clip(0, 18)

print(f"✓ Generated {len(df)} player game logs")

# Feature columns
feature_cols = [
    'minutes_played', 'games_played_last_5',
    'avg_points_last_5', 'avg_assists_last_5', 'avg_rebounds_last_5',
    'field_goal_pct_last_5', 'three_point_pct_last_5', 'free_throw_pct_last_5',
    'opponent_defensive_rating', 'home_game'
]

X = df[feature_cols].values

# Train/test split (80/20)
split_idx = int(len(X) * 0.8)
X_train, X_test = X[:split_idx], X[split_idx:]

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

models_dir = Path(__file__).parent.parent / 'models'

# ==================== POINTS PREDICTION ====================
print("\n" + "=" * 80)
print("POINTS PREDICTION MODELS")
print("=" * 80)

y_points = df['points'].values
y_points_train, y_points_test = y_points[:split_idx], y_points[split_idx:]

# Model 1: Linear Regression
print("\n1. Training Linear Regression for Points...")
linear_model = LinearRegression()
linear_model.fit(X_train_scaled, y_points_train)

y_pred = linear_model.predict(X_test_scaled)
mae = mean_absolute_error(y_points_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_points_test, y_pred))
r2 = r2_score(y_points_test, y_pred)

print(f"   MAE: {mae:.2f} points")
print(f"   RMSE: {rmse:.2f}")
print(f"   R²: {r2:.4f}")

# Save model
linear_dir = models_dir / 'player_linear' / 'v1'
linear_dir.mkdir(parents=True, exist_ok=True)
with open(linear_dir / 'model.pkl', 'wb') as f:
    pickle.dump({'model': linear_model, 'scaler': scaler}, f)
with open(linear_dir / 'metadata.json', 'w') as f:
    json.dump({
        'model_type': 'LinearRegression',
        'target': 'points',
        'mae': float(mae),
        'rmse': float(rmse),
        'r2': float(r2),
        'trained_at': datetime.now().isoformat(),
        'n_train': len(X_train),
        'n_test': len(X_test)
    }, f, indent=2)

# Model 2: Ridge Regression
print("\n2. Training Ridge Regression for Points...")
ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train_scaled, y_points_train)

y_pred = ridge_model.predict(X_test_scaled)
mae = mean_absolute_error(y_points_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_points_test, y_pred))
r2 = r2_score(y_points_test, y_pred)

print(f"   MAE: {mae:.2f} points")
print(f"   RMSE: {rmse:.2f}")
print(f"   R²: {r2:.4f}")

ridge_dir = models_dir / 'player_ridge' / 'v1'
ridge_dir.mkdir(parents=True, exist_ok=True)
with open(ridge_dir / 'model.pkl', 'wb') as f:
    pickle.dump({'model': ridge_model, 'scaler': scaler}, f)
with open(ridge_dir / 'metadata.json', 'w') as f:
    json.dump({
        'model_type': 'Ridge',
        'target': 'points',
        'alpha': 1.0,
        'mae': float(mae),
        'rmse': float(rmse),
        'r2': float(r2),
        'trained_at': datetime.now().isoformat(),
        'n_train': len(X_train),
        'n_test': len(X_test)
    }, f, indent=2)

# Model 3: Lasso Regression
print("\n3. Training Lasso Regression for Points...")
lasso_model = Lasso(alpha=0.1)
lasso_model.fit(X_train_scaled, y_points_train)

y_pred = lasso_model.predict(X_test_scaled)
mae = mean_absolute_error(y_points_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_points_test, y_pred))
r2 = r2_score(y_points_test, y_pred)

# Count non-zero coefficients (feature selection)
n_features_selected = np.sum(lasso_model.coef_ != 0)

print(f"   MAE: {mae:.2f} points")
print(f"   RMSE: {rmse:.2f}")
print(f"   R²: {r2:.4f}")
print(f"   Features selected: {n_features_selected}/{len(feature_cols)}")

lasso_dir = models_dir / 'player_lasso' / 'v1'
lasso_dir.mkdir(parents=True, exist_ok=True)
with open(lasso_dir / 'model.pkl', 'wb') as f:
    pickle.dump({'model': lasso_model, 'scaler': scaler}, f)
with open(lasso_dir / 'metadata.json', 'w') as f:
    json.dump({
        'model_type': 'Lasso',
        'target': 'points',
        'alpha': 0.1,
        'mae': float(mae),
        'rmse': float(rmse),
        'r2': float(r2),
        'features_selected': int(n_features_selected),
        'trained_at': datetime.now().isoformat(),
        'n_train': len(X_train),
        'n_test': len(X_test)
    }, f, indent=2)

print("\n" + "=" * 80)
print("PLAYER PREDICTION MODELS COMPLETE!")
print("=" * 80)

# Save comparison
with open(models_dir / 'player_models_comparison.json', 'w') as f:
    json.dump({
        'trained_at': datetime.now().isoformat(),
        'target': 'points',
        'models': {
            'linear': {'mae': float(mean_absolute_error(y_points_test, linear_model.predict(X_test_scaled)))},
            'ridge': {'mae': float(mean_absolute_error(y_points_test, ridge_model.predict(X_test_scaled)))},
            'lasso': {'mae': float(mean_absolute_error(y_points_test, lasso_model.predict(X_test_scaled)))},
        }
    }, f, indent=2)

print("\n✅ All player prediction models saved!")
print(f"   Models directory: {models_dir}")
print("\nNote: Using synthetic data for demonstration.")
print("Replace with real player stats via NBA API for production.")
