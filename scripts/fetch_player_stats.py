#!/usr/bin/env python3
"""
Fetch Real Player Statistics from NBA API

Fetches player game logs for training prediction models.
"""

import sys
from pathlib import Path
import pandas as pd
import time

sys.path.append(str(Path(__file__).parent.parent))

from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players

print("Fetching player statistics...")

# Get top players (sample - can expand later)
all_players = players.get_active_players()
print(f"Found {len(all_players)} active players")

# Get top scorers (sample for now - could fetch all later)
top_players = [
    'Stephen Curry',
    'LeBron James',
    'Kevin Durant',
    'Giannis Antetokounmpo',
    'Luka Doncic',
    'Jayson Tatum',
    'Joel Embiid',
    'Nikola Jokic',
    'Damian Lillard',
    'Anthony Davis',
    'Devin Booker',
    'Kawhi Leonard',
    'Jimmy Butler',
    'Paul George',
    'Kyrie Irving',
]

player_stats_list = []

for player_name in top_players:
    try:
        print(f"\nFetching {player_name}...")

        # Find player
        player = players.find_players_by_full_name(player_name)
        if not player:
            print(f"  Player not found: {player_name}")
            continue

        player_id = player[0]['id']

        # Get 2023-24 season stats
        print(f"  Fetching 2023-24 season...")
        gamelog_23 = playergamelog.PlayerGameLog(
            player_id=player_id,
            season='2023-24'
        )
        df_23 = gamelog_23.get_data_frames()[0]
        df_23['season'] = '2023-24'

        # Get 2024-25 season stats
        print(f"  Fetching 2024-25 season...")
        time.sleep(0.6)  # Rate limiting
        gamelog_24 = playergamelog.PlayerGameLog(
            player_id=player_id,
            season='2024-25'
        )
        df_24 = gamelog_24.get_data_frames()[0]
        df_24['season'] = '2024-25'

        # Combine
        df_combined = pd.concat([df_23, df_24], ignore_index=True)
        df_combined['player_name'] = player_name
        df_combined['player_id'] = player_id

        player_stats_list.append(df_combined)
        print(f"  checkmark Fetched {len(df_combined)} games for {player_name}")

        time.sleep(0.6)  # Rate limiting

    except Exception as e:
        print(f"  Error fetching {player_name}: {e}")
        continue

# Combine all player stats
if player_stats_list:
    all_stats = pd.concat(player_stats_list, ignore_index=True)

    # Save to CSV
    data_dir = Path(__file__).parent.parent / 'data' / 'raw'
    data_dir.mkdir(parents=True, exist_ok=True)

    output_file = data_dir / 'player_stats_real.csv'
    all_stats.to_csv(output_file, index=False)

    print(f"\ncheckmark Saved {len(all_stats)} player game logs to {output_file}")
    print(f"  Players: {len(player_stats_list)}")
    print(f"  Games per player (avg): {len(all_stats) / len(player_stats_list):.0f}")
    print(f"\nSample columns:")
    print(all_stats.columns.tolist()[:10])
else:
    print("\n[xmark.circle] No player stats fetched")
