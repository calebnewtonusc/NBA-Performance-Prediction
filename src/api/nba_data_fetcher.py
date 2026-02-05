"""
Fetch live NBA data from nba_api
"""
from typing import Dict, Optional
import logging
import pandas as pd

try:
    from nba_api.stats.endpoints import leaguegamefinder
    from nba_api.stats.static import teams as nba_teams_static
    NBA_API_AVAILABLE = True
except ImportError:
    NBA_API_AVAILABLE = False
    logging.warning("nba_api not installed - using fallback estimates")

logger = logging.getLogger(__name__)

class NBADataFetcher:
    """Fetch live NBA team statistics"""

    def __init__(self):
        self.cache = {}  # Simple in-memory cache
        if NBA_API_AVAILABLE:
            self.all_teams = {team['abbreviation']: team for team in nba_teams_static.get_teams()}
        else:
            self.all_teams = {}

    def get_team_stats(self, team_abbr: str, season: int = 2024) -> Optional[Dict]:
        """
        Fetch current season stats for a team

        Args:
            team_abbr: Team abbreviation (e.g., 'BOS', 'LAL')
            season: NBA season year

        Returns:
            Dictionary with team stats or None if not found
        """
        try:
            team_abbr = team_abbr.upper()

            # Check cache (5-minute TTL in production, skip for now)
            cache_key = f"{team_abbr}_{season}"
            if cache_key in self.cache:
                return self.cache[cache_key]

            if NBA_API_AVAILABLE and team_abbr in self.all_teams:
                # Fetch real data from nba_api
                team_id = self.all_teams[team_abbr]['id']
                season_str = f"{season}-{str(season+1)[-2:]}"  # e.g., "2024-25"

                gamefinder = leaguegamefinder.LeagueGameFinder(
                    team_id_nullable=team_id,
                    season_nullable=season_str,
                    league_id_nullable='00'
                )

                games = gamefinder.get_data_frames()[0]

                if len(games) > 0:
                    # Calculate stats from actual games
                    wins = (games['WL'] == 'W').sum()
                    total_games = len(games)
                    win_pct = wins / total_games if total_games > 0 else 0.5

                    avg_points = games['PTS'].mean()
                    # Points allowed = opponent's points
                    avg_allowed = games['PTS'].mean()  # Approximate - would need opponent data

                    # Estimate avg_allowed from point differential
                    avg_plus_minus = games['PLUS_MINUS'].mean()
                    avg_allowed = avg_points - avg_plus_minus

                    stats = {
                        'win_pct': float(win_pct),
                        'avg_points': float(avg_points),
                        'avg_allowed': float(avg_allowed),
                        'point_diff': float(avg_plus_minus),
                    }

                    self.cache[cache_key] = stats
                    return stats

            # Fallback to estimates if API unavailable or fails
            logger.warning(f"Using fallback estimates for {team_abbr}")
            team_estimates = {
                'BOS': {'win_pct': 0.700, 'avg_points': 118.5, 'avg_allowed': 111.2},
                'LAL': {'win_pct': 0.550, 'avg_points': 113.8, 'avg_allowed': 112.5},
                'GSW': {'win_pct': 0.600, 'avg_points': 116.2, 'avg_allowed': 113.8},
                'MIA': {'win_pct': 0.520, 'avg_points': 110.5, 'avg_allowed': 109.8},
                'MIL': {'win_pct': 0.650, 'avg_points': 115.7, 'avg_allowed': 110.3},
                'PHX': {'win_pct': 0.580, 'avg_points': 114.2, 'avg_allowed': 112.1},
                'DEN': {'win_pct': 0.620, 'avg_points': 115.8, 'avg_allowed': 111.5},
                'DAL': {'win_pct': 0.590, 'avg_points': 116.3, 'avg_allowed': 113.2},
                'PHI': {'win_pct': 0.540, 'avg_points': 112.7, 'avg_allowed': 111.9},
                'NYK': {'win_pct': 0.560, 'avg_points': 111.2, 'avg_allowed': 108.5},
            }

            default_stats = {'win_pct': 0.500, 'avg_points': 112.0, 'avg_allowed': 112.0}
            stats = team_estimates.get(team_abbr, default_stats)

            return {
                'win_pct': stats['win_pct'],
                'avg_points': stats['avg_points'],
                'avg_allowed': stats['avg_allowed'],
                'point_diff': stats['avg_points'] - stats['avg_allowed'],
            }

        except Exception as e:
            logger.error(f"Error fetching stats for {team_abbr}: {e}")
            return None

    def get_game_features(self, home_team: str, away_team: str) -> Dict:
        """
        Build complete feature set for a game

        Args:
            home_team: Home team abbreviation
            away_team: Away team abbreviation

        Returns:
            Dictionary with all required features
        """
        home_stats = self.get_team_stats(home_team)
        away_stats = self.get_team_stats(away_team)

        if not home_stats or not away_stats:
            raise ValueError(f"Could not fetch stats for {home_team} vs {away_team}")

        return {
            'home_win_pct': home_stats['win_pct'],
            'away_win_pct': away_stats['win_pct'],
            'home_avg_points': home_stats['avg_points'],
            'away_avg_points': away_stats['avg_points'],
            'home_avg_allowed': home_stats['avg_allowed'],
            'away_avg_allowed': away_stats['avg_allowed'],
            'home_point_diff': home_stats['point_diff'],
            'away_point_diff': away_stats['point_diff'],
            # Defaults for additional features
            'h2h_games': 4,
            'home_h2h_win_pct': 0.5,
            'home_rest_days': 1,
            'away_rest_days': 1,
            'home_b2b': 0,
            'away_b2b': 0,
            'home_streak': 0,
            'away_streak': 0,
            'home_home_win_pct': home_stats['win_pct'] + 0.05,  # Home court advantage
            'away_away_win_pct': away_stats['win_pct'] - 0.05,  # Road disadvantage
        }
