#!/usr/bin/env python3
"""
Fetch Real NBA Data from NBA API

Fetches historical game data and team stats for model training.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

sys.path.append(str(Path(__file__).parent.parent))

from nba_api.stats.endpoints import leaguegamefinder, teamdashboardbygeneralsplits
from nba_api.stats.static import teams

print("Fetching real NBA data...")

# Get all NBA teams
nba_teams = teams.get_teams()
print(f"Found {len(nba_teams)} NBA teams")

# Fetch games from 2023-24 and 2024-25 seasons
print("\nFetching 2023-24 season games...")
try:
    gamefinder_23 = leaguegamefinder.LeagueGameFinder(
        season_nullable='2023-24',
        league_id_nullable='00'
    )
    games_23 = gamefinder_23.get_data_frames()[0]
    print(f"checkmark Fetched {len(games_23)} game records from 2023-24 season")
    time.sleep(1)  # Rate limiting
except Exception as e:
    print(f"Error fetching 2023-24 data: {e}")
    games_23 = pd.DataFrame()

print("\nFetching 2024-25 season games...")
try:
    gamefinder_24 = leaguegamefinder.LeagueGameFinder(
        season_nullable='2024-25',
        league_id_nullable='00'
    )
    games_24 = gamefinder_24.get_data_frames()[0]
    print(f"checkmark Fetched {len(games_24)} game records from 2024-25 season")
except Exception as e:
    print(f"Error fetching 2024-25 data: {e}")
    games_24 = pd.DataFrame()

# Combine seasons
if not games_23.empty and not games_24.empty:
    all_games = pd.concat([games_23, games_24], ignore_index=True)
elif not games_23.empty:
    all_games = games_23
elif not games_24.empty:
    all_games = all_games_24
else:
    print("ERROR: No game data fetched!")
    sys.exit(1)

print(f"\nTotal game records: {len(all_games)}")

# Process into game-level data (currently each game appears twice - once per team)
# Group by game ID to get home/away format
all_games['GAME_DATE'] = pd.to_datetime(all_games['GAME_DATE'])
all_games = all_games.sort_values('GAME_DATE')

# Extract home vs away from MATCHUP (e.g., "LAL vs. BOS" or "LAL @ BOS")
all_games['IS_HOME'] = all_games['MATCHUP'].str.contains('vs.')

# Create game-level dataset
games_processed = []
game_ids = all_games['GAME_ID'].unique()

print(f"\nProcessing {len(game_ids)} unique games...")

for game_id in game_ids:
    game_data = all_games[all_games['GAME_ID'] == game_id]

    if len(game_data) != 2:
        continue  # Skip if data is incomplete

    home_game = game_data[game_data['IS_HOME'] == True]
    away_game = game_data[game_data['IS_HOME'] == False]

    if home_game.empty or away_game.empty:
        continue

    home_game = home_game.iloc[0]
    away_game = away_game.iloc[0]

    games_processed.append({
        'game_id': game_id,
        'date': home_game['GAME_DATE'],
        'season': home_game['SEASON_ID'],
        'home_team_id': home_game['TEAM_ID'],
        'home_team_abbr': home_game['TEAM_ABBREVIATION'],
        'home_team_name': home_game['TEAM_NAME'],
        'away_team_id': away_game['TEAM_ID'],
        'away_team_abbr': away_game['TEAM_ABBREVIATION'],
        'away_team_name': away_game['TEAM_NAME'],
        'home_score': home_game['PTS'],
        'away_score': away_game['PTS'],
        'home_win': 1 if home_game['WL'] == 'W' else 0,
    })

games_df = pd.DataFrame(games_processed)
print(f"checkmark Processed {len(games_df)} complete games")

# Save to data directory
data_dir = Path(__file__).parent.parent / 'data' / 'raw'
data_dir.mkdir(parents=True, exist_ok=True)

output_file = data_dir / 'nba_games_real.csv'
games_df.to_csv(output_file, index=False)
print(f"\ncheckmark Saved real NBA game data to {output_file}")

print(f"\nSample of fetched data:")
print(games_df.head())
print(f"\nDate range: {games_df['date'].min()} to {games_df['date'].max()}")
print(f"Home team win rate: {games_df['home_win'].mean():.1%}")
