#!/usr/bin/env python3
"""
Generate Sample Data for Testing

Creates synthetic NBA data for testing without API calls.

Usage:
    python scripts/generate_sample_data.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def generate_sample_teams():
    """Generate sample team data"""
    teams = [
        {"id": 1, "abbreviation": "LAL", "city": "Los Angeles", "conference": "West", "division": "Pacific", "full_name": "Los Angeles Lakers", "name": "Lakers"},
        {"id": 2, "abbreviation": "BOS", "city": "Boston", "conference": "East", "division": "Atlantic", "full_name": "Boston Celtics", "name": "Celtics"},
        {"id": 3, "abbreviation": "GSW", "city": "Golden State", "conference": "West", "division": "Pacific", "full_name": "Golden State Warriors", "name": "Warriors"},
        {"id": 4, "abbreviation": "MIA", "city": "Miami", "conference": "East", "division": "Southeast", "full_name": "Miami Heat", "name": "Heat"},
        {"id": 5, "abbreviation": "MIL", "city": "Milwaukee", "conference": "East", "division": "Central", "full_name": "Milwaukee Bucks", "name": "Bucks"},
        {"id": 6, "abbreviation": "DEN", "city": "Denver", "conference": "West", "division": "Northwest", "full_name": "Denver Nuggets", "name": "Nuggets"},
        {"id": 7, "abbreviation": "PHX", "city": "Phoenix", "conference": "West", "division": "Pacific", "full_name": "Phoenix Suns", "name": "Suns"},
        {"id": 8, "abbreviation": "PHI", "city": "Philadelphia", "conference": "East", "division": "Atlantic", "full_name": "Philadelphia 76ers", "name": "76ers"},
        {"id": 9, "abbreviation": "DAL", "city": "Dallas", "conference": "West", "division": "Southwest", "full_name": "Dallas Mavericks", "name": "Mavericks"},
        {"id": 10, "abbreviation": "BKN", "city": "Brooklyn", "conference": "East", "division": "Atlantic", "full_name": "Brooklyn Nets", "name": "Nets"},
    ]
    return teams


def generate_sample_games(n_games=100):
    """Generate sample game data"""
    np.random.seed(42)
    teams = generate_sample_teams()
    games = []

    start_date = datetime(2023, 10, 1)

    for i in range(n_games):
        game_date = start_date + timedelta(days=i // 5)  # ~5 games per day

        home_team = teams[np.random.randint(0, len(teams))]
        away_team = teams[np.random.randint(0, len(teams))]

        # Make sure home and away are different
        while away_team["id"] == home_team["id"]:
            away_team = teams[np.random.randint(0, len(teams))]

        home_score = np.random.randint(95, 125)
        away_score = np.random.randint(95, 125)

        game = {
            "id": i + 1,
            "date": game_date.isoformat() + "Z",
            "home_team": home_team,
            "home_team_score": home_score,
            "visitor_team": away_team,
            "visitor_team_score": away_score,
            "status": "Final",
            "season": 2023,
            "period": 4,
            "postseason": False,
            # Enriched fields
            "winner": "home" if home_score > away_score else "away",
            "winner_team_id": home_team["id"] if home_score > away_score else away_team["id"],
            "loser_team_id": away_team["id"] if home_score > away_score else home_team["id"],
            "score_differential": abs(home_score - away_score),
            "total_points": home_score + away_score,
            "game_date_parsed": game_date.strftime("%Y-%m-%d")
        }

        games.append(game)

    return games


def generate_sample_players():
    """Generate sample player data"""
    np.random.seed(42)
    teams = generate_sample_teams()

    players = [
        {"id": 1, "first_name": "LeBron", "last_name": "James", "position": "F", "height_feet": 6, "height_inches": 9, "weight_pounds": 250, "team": teams[0]},
        {"id": 2, "first_name": "Jayson", "last_name": "Tatum", "position": "F", "height_feet": 6, "height_inches": 8, "weight_pounds": 210, "team": teams[1]},
        {"id": 3, "first_name": "Stephen", "last_name": "Curry", "position": "G", "height_feet": 6, "height_inches": 2, "weight_pounds": 185, "team": teams[2]},
        {"id": 4, "first_name": "Jimmy", "last_name": "Butler", "position": "F", "height_feet": 6, "height_inches": 7, "weight_pounds": 230, "team": teams[3]},
        {"id": 5, "first_name": "Giannis", "last_name": "Antetokounmpo", "position": "F", "height_feet": 6, "height_inches": 11, "weight_pounds": 242, "team": teams[4]},
        {"id": 6, "first_name": "Nikola", "last_name": "Jokic", "position": "C", "height_feet": 6, "height_inches": 11, "weight_pounds": 284, "team": teams[5]},
        {"id": 7, "first_name": "Kevin", "last_name": "Durant", "position": "F", "height_feet": 6, "height_inches": 10, "weight_pounds": 240, "team": teams[6]},
        {"id": 8, "first_name": "Joel", "last_name": "Embiid", "position": "C", "height_feet": 7, "height_inches": 0, "weight_pounds": 280, "team": teams[7]},
        {"id": 9, "first_name": "Luka", "last_name": "Doncic", "position": "G", "height_feet": 6, "height_inches": 7, "weight_pounds": 230, "team": teams[8]},
        {"id": 10, "first_name": "Kyrie", "last_name": "Irving", "position": "G", "height_feet": 6, "height_inches": 2, "weight_pounds": 195, "team": teams[9]},
    ]

    return players


def generate_sample_player_stats(n_games=50):
    """Generate sample player statistics"""
    np.random.seed(42)
    players = generate_sample_players()
    stats = []

    start_date = datetime(2023, 10, 1)

    stat_id = 1
    for game_num in range(n_games):
        game_date = start_date + timedelta(days=game_num)

        # Generate stats for random players in this game
        for _ in range(10):  # 10 players per game
            player = players[np.random.randint(0, len(players))]

            pts = np.random.randint(5, 40)
            fga = np.random.randint(8, 25)
            fgm = min(int(fga * np.random.uniform(0.35, 0.55)), fga)

            stat = {
                "id": stat_id,
                "pts": pts,
                "ast": np.random.randint(0, 12),
                "reb": np.random.randint(2, 15),
                "stl": np.random.randint(0, 4),
                "blk": np.random.randint(0, 3),
                "turnover": np.random.randint(0, 5),
                "pf": np.random.randint(0, 5),
                "fgm": fgm,
                "fga": fga,
                "fg_pct": round(fgm / fga, 3) if fga > 0 else 0,
                "fg3m": np.random.randint(0, 6),
                "fg3a": np.random.randint(0, 10),
                "ftm": np.random.randint(0, 10),
                "fta": np.random.randint(0, 12),
                "oreb": np.random.randint(0, 5),
                "dreb": np.random.randint(2, 10),
                "min": f"{np.random.randint(20, 40)}:00",
                "player": {
                    "id": player["id"],
                    "first_name": player["first_name"],
                    "last_name": player["last_name"]
                },
                "game": {
                    "id": game_num + 1,
                    "date": game_date.isoformat() + "Z",
                    "season": 2023
                },
                "team": player["team"]
            }

            stats.append(stat)
            stat_id += 1

    return stats


def save_sample_data():
    """Generate and save all sample data"""
    logger.info("Generating sample data...")

    # Create directories
    data_dir = Path("data/raw")
    (data_dir / "games").mkdir(parents=True, exist_ok=True)
    (data_dir / "teams").mkdir(parents=True, exist_ok=True)
    (data_dir / "players").mkdir(parents=True, exist_ok=True)
    Path("data/external").mkdir(parents=True, exist_ok=True)

    # Generate and save teams
    teams = generate_sample_teams()
    with open(data_dir / "teams" / "all_teams.json", "w") as f:
        json.dump(teams, f, indent=2)
    logger.info(f"✓ Generated {len(teams)} sample teams")

    # Generate and save games
    games = generate_sample_games(200)
    with open(data_dir / "games" / "2023_season.json", "w") as f:
        json.dump(games, f, indent=2)
    logger.info(f"✓ Generated {len(games)} sample games")

    # Generate and save players
    players = generate_sample_players()
    with open(data_dir / "players" / "all_players.json", "w") as f:
        json.dump(players, f, indent=2)
    logger.info(f"✓ Generated {len(players)} sample players")

    # Generate and save player stats
    stats = generate_sample_player_stats(100)
    with open(data_dir / "players" / "player_stats_2023.json", "w") as f:
        json.dump(stats, f, indent=2)
    logger.info(f"✓ Generated {len(stats)} sample player stats")

    # Create team mappings
    team_mappings = {team["id"]: {
        "abbreviation": team["abbreviation"],
        "city": team["city"],
        "conference": team["conference"],
        "division": team["division"],
        "full_name": team["full_name"],
        "name": team["name"]
    } for team in teams}
    with open("data/external/team_mappings.json", "w") as f:
        json.dump(team_mappings, f, indent=2)

    # Create player mappings
    player_mappings = {player["id"]: {
        "first_name": player["first_name"],
        "last_name": player["last_name"],
        "full_name": f"{player['first_name']} {player['last_name']}",
        "position": player["position"],
        "height_feet": player["height_feet"],
        "height_inches": player["height_inches"],
        "weight_pounds": player["weight_pounds"],
        "team": player["team"]
    } for player in players}
    with open("data/external/player_mappings.json", "w") as f:
        json.dump(player_mappings, f, indent=2)

    logger.info("✓ Sample data generation complete!")
    logger.info(f"Data saved to: {data_dir.absolute()}")


def main():
    """Main function"""
    save_sample_data()


if __name__ == "__main__":
    main()
