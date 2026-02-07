"""
Player Data Collection Module

This module handles fetching NBA player data from the API, including:
- Player roster information
- Player game statistics
- Player season averages
- Player ID to name mappings

Usage:
    from src.data_collection.player_data import PlayerDataCollector

    collector = PlayerDataCollector()
    players = collector.fetch_all_players()
    stats = collector.fetch_player_stats_by_season(2023)
"""

import json
import requests
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.data_collection.base_client import BaseAPIClient
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class PlayerDataCollector:
    """Collector for NBA player data"""

    def __init__(self, base_url: str = "https://api.balldontlie.io/v1", api_key: Optional[str] = None):
        """
        Initialize the player data collector

        Args:
            base_url: Base URL for the NBA API (default: https://api.balldontlie.io/v1)
            api_key: API key for balldontlie.io (required - get free key at app.balldontlie.io)
        """
        import os

        # Try to get API key from parameter, environment variable, or config
        self.api_key = api_key or os.getenv('BALLDONTLIE_API_KEY')

        if not self.api_key:
            logger.warning(
                "No API key provided for balldontlie.io! "
                "Get a free API key at https://app.balldontlie.io and set BALLDONTLIE_API_KEY environment variable."
            )

        self.client = BaseAPIClient(
            base_url=base_url,
            api_key=self.api_key,
            rate_limit_delay=12.0  # Free tier: 5 requests/min = 12 seconds between requests
        )
        self.data_dir = Path("data/raw/players")
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def fetch_all_players(self, per_page: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch all NBA players

        Args:
            per_page: Number of results per page

        Returns:
            List of player dictionaries
        """
        logger.info("Fetching all NBA players")

        all_players = []
        page = 1

        while True:
            try:
                response = self.client.get("/players", params={
                    "per_page": per_page,
                    "page": page
                })

                players = response.get("data", [])
                if not players:
                    break

                all_players.extend(players)
                logger.info(f"Fetched page {page}: {len(players)} players (total: {len(all_players)})")

                # Check if there are more pages
                meta = response.get("meta", {})
                if page >= meta.get("total_pages", 1):
                    break

                page += 1

            except Exception as e:
                logger.error(f"Error fetching players page {page}: {str(e)}")
                break

        logger.info(f"Total players fetched: {len(all_players)}")
        return all_players

    def fetch_player_by_id(self, player_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch a specific player by ID

        Args:
            player_id: Player ID

        Returns:
            Player dictionary or None if not found
        """
        try:
            response = self.client.get(f"/players/{player_id}")
            return response.get("data")
        except Exception as e:
            logger.error(f"Error fetching player {player_id}: {str(e)}")
            return None

    def search_players(self, search_term: str) -> Dict[str, Any]:
        """
        Search for players by name using the balldontlie.io API

        Args:
            search_term: Player name to search for

        Returns:
            Dictionary with players list, metadata, and data source info

        Raises:
            Exception: If API key is missing or API request fails
        """
        logger.info(f"Searching for players matching '{search_term}'")

        if not self.api_key:
            error_msg = (
                "balldontlie.io API key is required. "
                "Get a free API key at https://app.balldontlie.io and set the "
                "BALLDONTLIE_API_KEY environment variable."
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        all_players = []
        cursor = None
        max_pages = 10  # Safety limit

        try:
            for page_num in range(max_pages):
                params = {
                    "search": search_term,
                    "per_page": 100
                }

                if cursor:
                    params["cursor"] = cursor

                response = self.client.get("/players", params=params)

                players = response.get("data", [])
                if not players:
                    break

                all_players.extend(players)

                # Check for pagination cursor
                meta = response.get("meta", {})
                cursor = meta.get("next_cursor")

                # If no more pages, break
                if not cursor:
                    break

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                error_msg = (
                    "Invalid API key for balldontlie.io. "
                    "Please verify your API key at https://app.balldontlie.io"
                )
                logger.error(error_msg)
                raise ValueError(error_msg)
            elif e.response.status_code == 429:
                error_msg = (
                    "Rate limit exceeded for balldontlie.io API. "
                    "Free tier allows 5 requests/minute. Please wait and try again."
                )
                logger.error(error_msg)
                raise ValueError(error_msg)
            else:
                logger.error(f"API request failed: {str(e)}")
                raise

        except Exception as e:
            error_msg = f"Failed to search players: {str(e)}"
            logger.error(error_msg)
            raise

        logger.info(f"Found {len(all_players)} players from balldontlie.io API")
        return {
            "players": all_players,
            "data_source": "api",
            "timestamp": self._get_timestamp()
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()

    def fetch_player_stats_by_season(
        self,
        season: int,
        player_ids: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch player statistics for a specific season

        Args:
            season: Season year (e.g., 2023)
            player_ids: Optional list of specific player IDs to fetch

        Returns:
            List of player stat dictionaries
        """
        logger.info(f"Fetching player stats for season {season}")

        all_stats = []
        page = 1

        while True:
            try:
                params = {
                    "seasons[]": [season],
                    "per_page": 100,
                    "page": page
                }

                if player_ids:
                    params["player_ids[]"] = player_ids

                response = self.client.get("/stats", params=params)

                stats = response.get("data", [])
                if not stats:
                    break

                all_stats.extend(stats)
                logger.info(f"Fetched page {page}: {len(stats)} stats (total: {len(all_stats)})")

                # Check if there are more pages
                meta = response.get("meta", {})
                if page >= meta.get("total_pages", 1):
                    break

                page += 1

            except Exception as e:
                logger.error(f"Error fetching stats page {page}: {str(e)}")
                break

        logger.info(f"Total stats fetched: {len(all_stats)}")
        return all_stats

    def fetch_player_stats_by_game(
        self,
        game_ids: List[int]
    ) -> List[Dict[str, Any]]:
        """
        Fetch player statistics for specific games

        Args:
            game_ids: List of game IDs

        Returns:
            List of player stat dictionaries
        """
        logger.info(f"Fetching player stats for {len(game_ids)} games")

        all_stats = []
        page = 1

        while True:
            try:
                response = self.client.get("/stats", params={
                    "game_ids[]": game_ids,
                    "per_page": 100,
                    "page": page
                })

                stats = response.get("data", [])
                if not stats:
                    break

                all_stats.extend(stats)

                meta = response.get("meta", {})
                if page >= meta.get("total_pages", 1):
                    break

                page += 1

            except Exception as e:
                logger.error(f"Error fetching game stats page {page}: {str(e)}")
                break

        return all_stats

    def fetch_player_stats_by_date_range(
        self,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Fetch player statistics within a date range

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            List of player stat dictionaries
        """
        logger.info(f"Fetching player stats from {start_date} to {end_date}")

        all_stats = []
        page = 1

        while True:
            try:
                response = self.client.get("/stats", params={
                    "start_date": start_date,
                    "end_date": end_date,
                    "per_page": 100,
                    "page": page
                })

                stats = response.get("data", [])
                if not stats:
                    break

                all_stats.extend(stats)
                logger.info(f"Fetched page {page}: {len(stats)} stats (total: {len(all_stats)})")

                meta = response.get("meta", {})
                if page >= meta.get("total_pages", 1):
                    break

                page += 1

            except Exception as e:
                logger.error(f"Error fetching stats page {page}: {str(e)}")
                break

        return all_stats

    def create_player_mapping(
        self,
        players: List[Dict[str, Any]]
    ) -> Dict[int, Dict[str, Any]]:
        """
        Create a mapping from player ID to player info

        Args:
            players: List of player dictionaries

        Returns:
            Dictionary mapping player_id to player info
        """
        mapping = {}
        for player in players:
            player_id = player.get("id")
            if player_id:
                mapping[player_id] = {
                    "first_name": player.get("first_name"),
                    "last_name": player.get("last_name"),
                    "full_name": f"{player.get('first_name')} {player.get('last_name')}",
                    "position": player.get("position"),
                    "height_feet": player.get("height_feet"),
                    "height_inches": player.get("height_inches"),
                    "weight_pounds": player.get("weight_pounds"),
                    "team": player.get("team", {})
                }

        return mapping

    def calculate_player_season_averages(
        self,
        stats: List[Dict[str, Any]]
    ) -> Dict[int, Dict[str, float]]:
        """
        Calculate season averages for each player from game stats

        Args:
            stats: List of player game statistics

        Returns:
            Dictionary mapping player_id to season averages
        """
        player_totals = {}
        player_games = {}

        for stat in stats:
            player_id = stat.get("player", {}).get("id")
            if not player_id:
                continue

            if player_id not in player_totals:
                player_totals[player_id] = {
                    "pts": 0, "ast": 0, "reb": 0, "stl": 0, "blk": 0,
                    "turnover": 0, "fgm": 0, "fga": 0, "fg3m": 0, "fg3a": 0,
                    "ftm": 0, "fta": 0, "oreb": 0, "dreb": 0, "pf": 0
                }
                player_games[player_id] = 0

            player_games[player_id] += 1

            for key in player_totals[player_id]:
                value = stat.get(key, 0)
                if value is not None:
                    player_totals[player_id][key] += value

        # Calculate averages
        player_averages = {}
        for player_id, totals in player_totals.items():
            games_played = player_games[player_id]
            if games_played > 0:
                player_averages[player_id] = {
                    key: round(value / games_played, 2)
                    for key, value in totals.items()
                }
                player_averages[player_id]["games_played"] = games_played

                # Calculate percentages
                if totals["fga"] > 0:
                    player_averages[player_id]["fg_pct"] = round(
                        totals["fgm"] / totals["fga"], 3
                    )
                if totals["fg3a"] > 0:
                    player_averages[player_id]["fg3_pct"] = round(
                        totals["fg3m"] / totals["fg3a"], 3
                    )
                if totals["fta"] > 0:
                    player_averages[player_id]["ft_pct"] = round(
                        totals["ftm"] / totals["fta"], 3
                    )

        return player_averages

    def save_to_file(self, data: Any, filename: str):
        """
        Save data to a JSON file

        Args:
            data: Data to save
            filename: Output filename
        """
        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved data to {filepath}")

    def load_from_file(self, filename: str) -> Any:
        """
        Load data from a JSON file

        Args:
            filename: Input filename

        Returns:
            Loaded data
        """
        with open(filename, 'r') as f:
            data = json.load(f)

        logger.info(f"Loaded data from {filename}")
        return data

    def collect_all_player_data(self):
        """Collect all player information and save to file"""
        players = self.fetch_all_players()
        self.save_to_file(players, self.data_dir / "all_players.json")

        # Create and save player mapping
        mapping = self.create_player_mapping(players)
        self.save_to_file(mapping, Path("data/external/player_mappings.json"))

        return players

    def collect_season_stats(self, season: int):
        """
        Collect all player stats for a season

        Args:
            season: Season year
        """
        stats = self.fetch_player_stats_by_season(season)
        self.save_to_file(
            stats,
            self.data_dir / f"player_stats_{season}.json"
        )

        # Calculate and save averages
        averages = self.calculate_player_season_averages(stats)
        self.save_to_file(
            averages,
            self.data_dir / f"player_averages_{season}.json"
        )

        return stats

    def close(self):
        """Close the API client"""
        self.client.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Example usage
if __name__ == "__main__":
    with PlayerDataCollector() as collector:
        # Collect all players
        players = collector.collect_all_player_data()
        print(f"Collected {len(players)} players")

        # Collect stats for recent seasons
        for season in range(2020, 2025):
            collector.collect_season_stats(season)
