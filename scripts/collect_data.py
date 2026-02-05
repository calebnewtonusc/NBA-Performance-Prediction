#!/usr/bin/env python3
"""
Automated Data Collection Script

This script collects NBA data from APIs and saves it to the data directory.

Usage:
    python scripts/collect_data.py --seasons 2020 2021 2022 2023 2024
    python scripts/collect_data.py --quick  # Just collect recent data
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.data_collection.game_data import GameDataCollector
from src.data_collection.player_data import PlayerDataCollector
from src.data_collection.team_data import TeamDataCollector
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def collect_all_data(seasons: list, quick: bool = False):
    """
    Collect all NBA data

    Args:
        seasons: List of season years to collect
        quick: If True, only collect minimal data for testing
    """
    logger.info("Starting data collection...")

    # Collect teams (only need to do once)
    logger.info("Collecting team data...")
    with TeamDataCollector() as team_collector:
        teams = team_collector.collect_all_team_data()
        logger.info(f"Collected {len(teams)} teams")

    # Collect games
    logger.info("Collecting game data...")
    with GameDataCollector() as game_collector:
        for season in seasons:
            if quick:
                # Quick mode: just get 1 month of data
                games = game_collector.fetch_games_by_date_range(
                    f"{season}-10-01",
                    f"{season}-10-31"
                )
            else:
                # Full mode: get entire season
                games = game_collector.fetch_games_by_season(season)

            enriched_games = game_collector.enrich_game_data(games)
            game_collector.save_games_to_file(
                enriched_games,
                f"data/raw/games/{season}_season.json"
            )
            logger.info(f"Collected {len(enriched_games)} games for season {season}")

            # Generate team season reports
            with TeamDataCollector() as tc:
                tc.generate_season_report(season, enriched_games)

    # Collect player data
    logger.info("Collecting player data...")
    with PlayerDataCollector() as player_collector:
        # Collect all players
        players = player_collector.collect_all_player_data()
        logger.info(f"Collected {len(players)} players")

        # Collect player stats for each season
        for season in seasons:
            if not quick:  # Skip in quick mode as this is slow
                player_collector.collect_season_stats(season)
                logger.info(f"Collected player stats for season {season}")

    logger.info("Data collection complete!")
    logger.info(f"Data saved to: {Path('data/raw').absolute()}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Collect NBA data from APIs"
    )

    parser.add_argument(
        "--seasons",
        nargs="+",
        type=int,
        default=[2023, 2024],
        help="Seasons to collect (e.g., 2020 2021 2022)"
    )

    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick mode: collect minimal data for testing"
    )

    args = parser.parse_args()

    logger.info(f"Collecting data for seasons: {args.seasons}")
    if args.quick:
        logger.info("Quick mode enabled - collecting minimal data")

    try:
        collect_all_data(args.seasons, args.quick)
        logger.info("✓ Data collection successful!")

    except Exception as e:
        logger.error(f"Data collection failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
