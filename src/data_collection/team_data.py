"""
Team Data Collection Module

This module handles fetching NBA team data from the API, including:
- Team information and rosters
- Team season statistics
- Team standings

Usage:
    from src.data_collection.team_data import TeamDataCollector

    collector = TeamDataCollector()
    teams = collector.fetch_all_teams()
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from collections import defaultdict
from src.data_collection.base_client import BaseAPIClient
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class TeamDataCollector:
    """Collector for NBA team data"""

    def __init__(self, base_url: str = "https://www.balldontlie.io/api/v1"):
        """
        Initialize the team data collector

        Args:
            base_url: Base URL for the NBA API
        """
        self.client = BaseAPIClient(base_url=base_url, rate_limit_delay=1.0)
        self.data_dir = Path("data/raw/teams")
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def fetch_all_teams(self) -> List[Dict[str, Any]]:
        """
        Fetch all NBA teams

        Returns:
            List of team dictionaries
        """
        logger.info("Fetching all NBA teams")

        try:
            response = self.client.get("/teams")
            teams = response.get("data", [])
            logger.info(f"Fetched {len(teams)} teams")
            return teams

        except Exception as e:
            logger.error(f"Error fetching teams: {str(e)}")
            return []

    def fetch_team_by_id(self, team_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch a specific team by ID

        Args:
            team_id: Team ID

        Returns:
            Team dictionary or None if not found
        """
        try:
            response = self.client.get(f"/teams/{team_id}")
            return response.get("data")
        except Exception as e:
            logger.error(f"Error fetching team {team_id}: {str(e)}")
            return None

    def create_team_mapping(
        self,
        teams: List[Dict[str, Any]]
    ) -> Dict[int, Dict[str, Any]]:
        """
        Create a mapping from team ID to team info

        Args:
            teams: List of team dictionaries

        Returns:
            Dictionary mapping team_id to team info
        """
        mapping = {}
        for team in teams:
            team_id = team.get("id")
            if team_id:
                mapping[team_id] = {
                    "abbreviation": team.get("abbreviation"),
                    "city": team.get("city"),
                    "conference": team.get("conference"),
                    "division": team.get("division"),
                    "full_name": team.get("full_name"),
                    "name": team.get("name")
                }

        return mapping

    def calculate_team_season_stats(
        self,
        games: List[Dict[str, Any]],
        team_id: int
    ) -> Dict[str, Any]:
        """
        Calculate season statistics for a team from game data

        Args:
            games: List of game dictionaries
            team_id: Team ID to calculate stats for

        Returns:
            Dictionary of season statistics
        """
        stats = {
            "team_id": team_id,
            "games_played": 0,
            "wins": 0,
            "losses": 0,
            "home_wins": 0,
            "home_losses": 0,
            "away_wins": 0,
            "away_losses": 0,
            "points_scored": 0,
            "points_allowed": 0,
            "total_score_differential": 0
        }

        for game in games:
            home_team_id = game.get("home_team", {}).get("id")
            visitor_team_id = game.get("visitor_team", {}).get("id")
            home_score = game.get("home_team_score", 0)
            visitor_score = game.get("visitor_team_score", 0)

            # Skip if team not in this game
            if team_id not in [home_team_id, visitor_team_id]:
                continue

            # Skip if game hasn't finished
            if game.get("status") != "Final":
                continue

            stats["games_played"] += 1

            is_home = (team_id == home_team_id)

            if is_home:
                team_score = home_score
                opponent_score = visitor_score
                if home_score > visitor_score:
                    stats["wins"] += 1
                    stats["home_wins"] += 1
                else:
                    stats["losses"] += 1
                    stats["home_losses"] += 1
            else:
                team_score = visitor_score
                opponent_score = home_score
                if visitor_score > home_score:
                    stats["wins"] += 1
                    stats["away_wins"] += 1
                else:
                    stats["losses"] += 1
                    stats["away_losses"] += 1

            stats["points_scored"] += team_score
            stats["points_allowed"] += opponent_score
            stats["total_score_differential"] += (team_score - opponent_score)

        # Calculate averages
        if stats["games_played"] > 0:
            stats["win_percentage"] = round(
                stats["wins"] / stats["games_played"], 3
            )
            stats["avg_points_scored"] = round(
                stats["points_scored"] / stats["games_played"], 1
            )
            stats["avg_points_allowed"] = round(
                stats["points_allowed"] / stats["games_played"], 1
            )
            stats["avg_score_differential"] = round(
                stats["total_score_differential"] / stats["games_played"], 1
            )
            stats["home_win_pct"] = round(
                stats["home_wins"] / max(stats["home_wins"] + stats["home_losses"], 1), 3
            )
            stats["away_win_pct"] = round(
                stats["away_wins"] / max(stats["away_wins"] + stats["away_losses"], 1), 3
            )
        else:
            stats["win_percentage"] = 0.0
            stats["avg_points_scored"] = 0.0
            stats["avg_points_allowed"] = 0.0
            stats["avg_score_differential"] = 0.0
            stats["home_win_pct"] = 0.0
            stats["away_win_pct"] = 0.0

        return stats

    def calculate_all_team_season_stats(
        self,
        games: List[Dict[str, Any]],
        teams: List[Dict[str, Any]]
    ) -> Dict[int, Dict[str, Any]]:
        """
        Calculate season statistics for all teams

        Args:
            games: List of game dictionaries
            teams: List of team dictionaries

        Returns:
            Dictionary mapping team_id to season statistics
        """
        logger.info("Calculating season statistics for all teams")

        team_stats = {}
        for team in teams:
            team_id = team.get("id")
            if team_id:
                team_stats[team_id] = self.calculate_team_season_stats(games, team_id)
                team_stats[team_id]["team_info"] = {
                    "abbreviation": team.get("abbreviation"),
                    "full_name": team.get("full_name"),
                    "conference": team.get("conference"),
                    "division": team.get("division")
                }

        return team_stats

    def calculate_standings(
        self,
        team_stats: Dict[int, Dict[str, Any]],
        conference: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Calculate team standings from season statistics

        Args:
            team_stats: Dictionary of team statistics
            conference: Optional conference filter ('East' or 'West')

        Returns:
            List of teams sorted by wins (standings)
        """
        standings = []

        for team_id, stats in team_stats.items():
            team_info = stats.get("team_info", {})

            # Filter by conference if specified
            if conference and team_info.get("conference") != conference:
                continue

            standings.append({
                "team_id": team_id,
                "team_name": team_info.get("full_name"),
                "abbreviation": team_info.get("abbreviation"),
                "conference": team_info.get("conference"),
                "division": team_info.get("division"),
                "wins": stats.get("wins", 0),
                "losses": stats.get("losses", 0),
                "win_percentage": stats.get("win_percentage", 0),
                "avg_points_scored": stats.get("avg_points_scored", 0),
                "avg_points_allowed": stats.get("avg_points_allowed", 0)
            })

        # Sort by wins (descending), then by win percentage
        standings.sort(
            key=lambda x: (x["wins"], x["win_percentage"]),
            reverse=True
        )

        # Add rank
        for i, team in enumerate(standings):
            team["rank"] = i + 1

        return standings

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

    def collect_all_team_data(self):
        """Collect all team information and save to file"""
        teams = self.fetch_all_teams()
        self.save_to_file(teams, self.data_dir / "all_teams.json")

        # Create and save team mapping
        mapping = self.create_team_mapping(teams)
        self.save_to_file(mapping, Path("data/external/team_mappings.json"))

        return teams

    def generate_season_report(self, season: int, games: List[Dict[str, Any]]):
        """
        Generate comprehensive season report for all teams

        Args:
            season: Season year
            games: List of game dictionaries for the season
        """
        logger.info(f"Generating season report for {season}")

        # Get teams
        teams = self.fetch_all_teams()

        # Calculate team statistics
        team_stats = self.calculate_all_team_season_stats(games, teams)
        self.save_to_file(
            team_stats,
            self.data_dir / f"team_stats_{season}.json"
        )

        # Calculate overall standings
        overall_standings = self.calculate_standings(team_stats)
        self.save_to_file(
            overall_standings,
            self.data_dir / f"standings_{season}.json"
        )

        # Calculate conference standings
        east_standings = self.calculate_standings(team_stats, conference="East")
        west_standings = self.calculate_standings(team_stats, conference="West")

        self.save_to_file(
            {"East": east_standings, "West": west_standings},
            self.data_dir / f"conference_standings_{season}.json"
        )

        logger.info(f"Season report for {season} completed")

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
    from src.data_collection.game_data import GameDataCollector

    with TeamDataCollector() as team_collector:
        # Collect all teams
        teams = team_collector.collect_all_team_data()
        print(f"Collected {len(teams)} teams")

        # Generate season reports
        with GameDataCollector() as game_collector:
            for season in range(2020, 2025):
                games = game_collector.load_games_from_file(
                    f"data/raw/games/{season}_regular_season.json"
                )
                team_collector.generate_season_report(season, games)
