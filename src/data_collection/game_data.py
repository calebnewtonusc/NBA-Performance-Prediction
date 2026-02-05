"""
Game Data Collection Module

This module handles fetching NBA game data from the API, including:
- Game schedules
- Game results (scores, outcomes)
- Team statistics per game
- Historical game data

Usage:
    from src.data_collection.game_data import GameDataCollector

    collector = GameDataCollector()
    games = collector.fetch_games_by_season(2023)
    collector.save_games_to_file(games, "data/raw/games/2023_season.json")
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.data_collection.base_client import BaseAPIClient
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class GameDataCollector:
    """Collector for NBA game data"""

    def __init__(self, base_url: str = "https://www.balldontlie.io/api/v1"):
        """
        Initialize the game data collector

        Args:
            base_url: Base URL for the NBA API
        """
        self.client = BaseAPIClient(base_url=base_url, rate_limit_delay=1.0)
        self.data_dir = Path("data/raw/games")
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def fetch_games_by_date_range(
        self,
        start_date: str,
        end_date: str,
        per_page: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Fetch games within a date range

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            per_page: Number of results per page

        Returns:
            List of game dictionaries
        """
        logger.info(f"Fetching games from {start_date} to {end_date}")

        all_games = []
        page = 1

        while True:
            try:
                response = self.client.get("/games", params={
                    "start_date": start_date,
                    "end_date": end_date,
                    "per_page": per_page,
                    "page": page
                })

                games = response.get("data", [])
                if not games:
                    break

                all_games.extend(games)
                logger.info(f"Fetched page {page}: {len(games)} games (total: {len(all_games)})")

                # Check if there are more pages
                meta = response.get("meta", {})
                if page >= meta.get("total_pages", 1):
                    break

                page += 1

            except Exception as e:
                logger.error(f"Error fetching games page {page}: {str(e)}")
                break

        logger.info(f"Total games fetched: {len(all_games)}")
        return all_games

    def fetch_games_by_season(
        self,
        season: int,
        postseason: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Fetch all games for a specific season

        Args:
            season: Season year (e.g., 2023 for 2023-24 season)
            postseason: Whether to fetch postseason games

        Returns:
            List of game dictionaries
        """
        logger.info(f"Fetching {'postseason' if postseason else 'regular season'} games for {season}")

        # NBA season typically runs from October to April
        # Regular season: Oct - Apr
        # Postseason: Apr - Jun
        if postseason:
            start_date = f"{season}-04-01"
            end_date = f"{season}-06-30"
        else:
            start_date = f"{season}-10-01"
            end_date = f"{season + 1}-04-15"

        return self.fetch_games_by_date_range(start_date, end_date)

    def fetch_games_by_team(
        self,
        team_id: int,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Fetch games for a specific team

        Args:
            team_id: Team ID
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            List of game dictionaries
        """
        logger.info(f"Fetching games for team {team_id}")

        all_games = []
        page = 1

        while True:
            try:
                response = self.client.get("/games", params={
                    "team_ids[]": [team_id],
                    "start_date": start_date,
                    "end_date": end_date,
                    "per_page": 100,
                    "page": page
                })

                games = response.get("data", [])
                if not games:
                    break

                all_games.extend(games)

                meta = response.get("meta", {})
                if page >= meta.get("total_pages", 1):
                    break

                page += 1

            except Exception as e:
                logger.error(f"Error fetching team games page {page}: {str(e)}")
                break

        return all_games

    def fetch_game_by_id(self, game_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch a specific game by ID

        Args:
            game_id: Game ID

        Returns:
            Game dictionary or None if not found
        """
        try:
            response = self.client.get(f"/games/{game_id}")
            return response.get("data")
        except Exception as e:
            logger.error(f"Error fetching game {game_id}: {str(e)}")
            return None

    def enrich_game_data(self, games: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enrich game data with additional computed fields

        Args:
            games: List of game dictionaries

        Returns:
            List of enriched game dictionaries
        """
        enriched_games = []

        for game in games:
            enriched = game.copy()

            # Add winner
            home_score = game.get("home_team_score", 0)
            visitor_score = game.get("visitor_team_score", 0)

            if home_score > visitor_score:
                enriched["winner"] = "home"
                enriched["winner_team_id"] = game["home_team"]["id"]
                enriched["loser_team_id"] = game["visitor_team"]["id"]
            elif visitor_score > home_score:
                enriched["winner"] = "away"
                enriched["winner_team_id"] = game["visitor_team"]["id"]
                enriched["loser_team_id"] = game["home_team"]["id"]
            else:
                enriched["winner"] = "tie"
                enriched["winner_team_id"] = None
                enriched["loser_team_id"] = None

            # Add score differential
            enriched["score_differential"] = abs(home_score - visitor_score)

            # Add total points
            enriched["total_points"] = home_score + visitor_score

            # Parse date
            game_date = game.get("date", "")
            if game_date:
                enriched["game_date_parsed"] = game_date.split("T")[0]

            enriched_games.append(enriched)

        return enriched_games

    def save_games_to_file(
        self,
        games: List[Dict[str, Any]],
        filename: str
    ):
        """
        Save games to a JSON file

        Args:
            games: List of game dictionaries
            filename: Output filename (relative or absolute path)
        """
        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w') as f:
            json.dump(games, f, indent=2)

        logger.info(f"Saved {len(games)} games to {filepath}")

    def load_games_from_file(self, filename: str) -> List[Dict[str, Any]]:
        """
        Load games from a JSON file

        Args:
            filename: Input filename

        Returns:
            List of game dictionaries
        """
        with open(filename, 'r') as f:
            games = json.load(f)

        logger.info(f"Loaded {len(games)} games from {filename}")
        return games

    def collect_historical_data(
        self,
        start_season: int = 2020,
        end_season: int = 2024
    ):
        """
        Collect and save historical game data for multiple seasons

        Args:
            start_season: Starting season year
            end_season: Ending season year
        """
        for season in range(start_season, end_season + 1):
            logger.info(f"Collecting data for {season}-{season + 1} season")

            # Fetch regular season games
            games = self.fetch_games_by_season(season, postseason=False)

            # Enrich the data
            enriched_games = self.enrich_game_data(games)

            # Save to file
            filename = self.data_dir / f"{season}_regular_season.json"
            self.save_games_to_file(enriched_games, filename)

            # Small delay between seasons
            time.sleep(2)

        logger.info("Historical data collection complete!")

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
    with GameDataCollector() as collector:
        # Collect historical data
        collector.collect_historical_data(start_season=2020, end_season=2024)
