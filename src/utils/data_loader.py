"""
Data Loading Utilities

Helper functions for loading collected NBA data from files.

Usage:
    from src.utils.data_loader import load_games, load_players, load_teams

    games = load_games(season=2023)
    players = load_all_players()
"""

import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def load_games(
    season: Optional[int] = None,
    postseason: bool = False,
    data_dir: str = "data/raw/games"
) -> List[Dict[str, Any]]:
    """
    Load game data from files

    Args:
        season: Season year (None = all seasons)
        postseason: Whether to load postseason games
        data_dir: Directory containing game data

    Returns:
        List of game dictionaries
    """
    data_path = Path(data_dir)

    if season:
        suffix = "postseason" if postseason else "regular_season"
        filename = data_path / f"{season}_{suffix}.json"

        if not filename.exists():
            logger.warning(f"File not found: {filename}")
            return []

        with open(filename, 'r') as f:
            games = json.load(f)

        logger.info(f"Loaded {len(games)} games from {filename}")
        return games
    else:
        # Load all seasons
        all_games = []
        for file in data_path.glob("*_regular_season.json"):
            with open(file, 'r') as f:
                games = json.load(f)
                all_games.extend(games)

        logger.info(f"Loaded {len(all_games)} games from all seasons")
        return all_games


def load_games_as_dataframe(
    season: Optional[int] = None,
    postseason: bool = False,
    data_dir: str = "data/raw/games"
) -> pd.DataFrame:
    """
    Load game data as pandas DataFrame

    Args:
        season: Season year (None = all seasons)
        postseason: Whether to load postseason games
        data_dir: Directory containing game data

    Returns:
        DataFrame of games
    """
    games = load_games(season, postseason, data_dir)
    df = pd.DataFrame(games)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    return df


def load_all_players(data_dir: str = "data/raw/players") -> List[Dict[str, Any]]:
    """
    Load all player information

    Args:
        data_dir: Directory containing player data

    Returns:
        List of player dictionaries
    """
    filename = Path(data_dir) / "all_players.json"

    if not filename.exists():
        logger.warning(f"File not found: {filename}")
        return []

    with open(filename, 'r') as f:
        players = json.load(f)

    logger.info(f"Loaded {len(players)} players")
    return players


def load_player_stats(
    season: int,
    data_dir: str = "data/raw/players"
) -> List[Dict[str, Any]]:
    """
    Load player statistics for a season

    Args:
        season: Season year
        data_dir: Directory containing player data

    Returns:
        List of player stat dictionaries
    """
    filename = Path(data_dir) / f"player_stats_{season}.json"

    if not filename.exists():
        logger.warning(f"File not found: {filename}")
        return []

    with open(filename, 'r') as f:
        stats = json.load(f)

    logger.info(f"Loaded {len(stats)} player stats for season {season}")
    return stats


def load_player_stats_as_dataframe(
    season: int,
    data_dir: str = "data/raw/players"
) -> pd.DataFrame:
    """
    Load player statistics as DataFrame

    Args:
        season: Season year
        data_dir: Directory containing player data

    Returns:
        DataFrame of player stats
    """
    stats = load_player_stats(season, data_dir)
    df = pd.DataFrame(stats)

    return df


def load_all_teams(data_dir: str = "data/raw/teams") -> List[Dict[str, Any]]:
    """
    Load all team information

    Args:
        data_dir: Directory containing team data

    Returns:
        List of team dictionaries
    """
    filename = Path(data_dir) / "all_teams.json"

    if not filename.exists():
        logger.warning(f"File not found: {filename}")
        return []

    with open(filename, 'r') as f:
        teams = json.load(f)

    logger.info(f"Loaded {len(teams)} teams")
    return teams


def load_team_stats(
    season: int,
    data_dir: str = "data/raw/teams"
) -> Dict[int, Dict[str, Any]]:
    """
    Load team statistics for a season

    Args:
        season: Season year
        data_dir: Directory containing team data

    Returns:
        Dictionary mapping team_id to stats
    """
    filename = Path(data_dir) / f"team_stats_{season}.json"

    if not filename.exists():
        logger.warning(f"File not found: {filename}")
        return {}

    with open(filename, 'r') as f:
        stats = json.load(f)

    # Convert string keys to int
    stats = {int(k): v for k, v in stats.items()}

    logger.info(f"Loaded team stats for season {season}")
    return stats


def load_standings(
    season: int,
    conference: Optional[str] = None,
    data_dir: str = "data/raw/teams"
) -> List[Dict[str, Any]]:
    """
    Load team standings

    Args:
        season: Season year
        conference: Conference filter ('East' or 'West', None = both)
        data_dir: Directory containing team data

    Returns:
        List of team standings
    """
    if conference:
        filename = Path(data_dir) / f"conference_standings_{season}.json"

        if not filename.exists():
            logger.warning(f"File not found: {filename}")
            return []

        with open(filename, 'r') as f:
            standings = json.load(f)

        return standings.get(conference, [])
    else:
        filename = Path(data_dir) / f"standings_{season}.json"

        if not filename.exists():
            logger.warning(f"File not found: {filename}")
            return []

        with open(filename, 'r') as f:
            standings = json.load(f)

        logger.info(f"Loaded standings for season {season}")
        return standings


def load_player_mapping(data_dir: str = "data/external") -> Dict[int, Dict[str, Any]]:
    """
    Load player ID to info mapping

    Args:
        data_dir: Directory containing mappings

    Returns:
        Dictionary mapping player_id to player info
    """
    filename = Path(data_dir) / "player_mappings.json"

    if not filename.exists():
        logger.warning(f"File not found: {filename}")
        return {}

    with open(filename, 'r') as f:
        mapping = json.load(f)

    # Convert string keys to int
    mapping = {int(k): v for k, v in mapping.items()}

    logger.info(f"Loaded mapping for {len(mapping)} players")
    return mapping


def load_team_mapping(data_dir: str = "data/external") -> Dict[int, Dict[str, Any]]:
    """
    Load team ID to info mapping

    Args:
        data_dir: Directory containing mappings

    Returns:
        Dictionary mapping team_id to team info
    """
    filename = Path(data_dir) / "team_mappings.json"

    if not filename.exists():
        logger.warning(f"File not found: {filename}")
        return {}

    with open(filename, 'r') as f:
        mapping = json.load(f)

    # Convert string keys to int
    mapping = {int(k): v for k, v in mapping.items()}

    logger.info(f"Loaded mapping for {len(mapping)} teams")
    return mapping


# Example usage
if __name__ == "__main__":
    # Example: Load 2023 season games
    games_df = load_games_as_dataframe(season=2023)
    print(f"Loaded {len(games_df)} games")

    # Example: Load all teams
    teams = load_all_teams()
    print(f"Loaded {len(teams)} teams")
