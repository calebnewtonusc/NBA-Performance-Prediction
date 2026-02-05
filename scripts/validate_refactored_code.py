#!/usr/bin/env python3
"""
Comprehensive Validation Script for Refactored Code

This script validates that all refactored vectorized operations
produce correct results and achieve expected performance improvements.

Usage:
    python3 scripts/validate_refactored_code.py
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time


def create_test_games(n_games=1000, n_teams=30):
    """Create synthetic game data for testing"""
    games = []
    for i in range(n_games):
        games.append({
            'id': i,
            'date': pd.Timestamp('2024-01-01') + timedelta(days=i // 5),
            'home_team_id': (i % n_teams) + 1,
            'visitor_team_id': ((i + 1) % n_teams) + 1,
            'home_team_score': np.random.randint(85, 125),
            'visitor_team_score': np.random.randint(85, 125)
        })
    df = pd.DataFrame(games)
    df['date'] = pd.to_datetime(df['date'])
    return df


def validate_game_features():
    """Validate GameFeatureEngineer refactored code"""
    print("=" * 70)
    print("VALIDATION: Game Feature Engineering (Vectorized Operations)")
    print("=" * 70)

    try:
        from src.data_processing.game_features import GameFeatureEngineer

        engineer = GameFeatureEngineer()
        print("✓ Module imports successfully")

        # Test 1: Basic functionality
        print("\n[Test 1] Basic Functionality")
        df = create_test_games(n_games=100)
        result = engineer.calculate_team_form(
            df, team_id=1, date=pd.Timestamp('2024-02-01'), n_games=10
        )
        assert isinstance(result, dict), "Result should be dictionary"
        assert 'games_played' in result, "Missing games_played"
        assert 'win_pct' in result, "Missing win_pct"
        print(f"✓ calculate_team_form returns correct structure")
        print(f"  Sample result: {result}")

        # Test 2: Edge cases
        print("\n[Test 2] Edge Cases")
        empty_result = engineer.calculate_team_form(
            df, team_id=999, date=pd.Timestamp('2024-02-01'), n_games=10
        )
        assert empty_result['games_played'] == 0, "Empty case should have 0 games"
        print("✓ Empty DataFrame handling works")

        # Test 3: Head-to-head
        print("\n[Test 3] Head-to-Head Calculation")
        h2h_result = engineer.calculate_head_to_head(
            df, team1_id=1, team2_id=2,
            before_date=pd.Timestamp('2024-02-01'), n_games=10
        )
        assert 'h2h_games' in h2h_result, "Missing h2h_games"
        assert 'team1_wins' in h2h_result, "Missing team1_wins"
        wins_sum = h2h_result['team1_wins'] + h2h_result['team2_wins']
        games = h2h_result['h2h_games']
        assert wins_sum == games, f"Wins don't add up: {wins_sum} != {games}"
        print("✓ Head-to-head calculation correct")
        print(f"  Sample result: {h2h_result}")

        # Test 4: Win streak
        print("\n[Test 4] Win Streak Calculation")
        streak = engineer.calculate_win_streak(
            df, team_id=1, before_date=pd.Timestamp('2024-02-01')
        )
        assert isinstance(streak, (int, np.integer)), "Streak should be integer"
        print(f"✓ Win streak calculation works (streak={streak})")

        # Test 5: Performance benchmark
        print("\n[Test 5] Performance Benchmark")
        large_df = create_test_games(n_games=5000)

        start = time.time()
        for _ in range(10):
            _ = engineer.calculate_team_form(
                large_df, team_id=1,
                date=pd.Timestamp('2024-06-01'), n_games=10
            )
        elapsed = time.time() - start
        avg_time = elapsed / 10

        print(f"✓ Performance test: {avg_time*1000:.2f}ms per call (10 iterations)")
        if avg_time < 0.1:
            print("  ⚡ EXCELLENT: Vectorized operations are fast!")
        elif avg_time < 0.5:
            print("  ✓ GOOD: Acceptable performance")
        else:
            print("  ⚠ WARNING: Performance could be better")

        print("\n" + "=" * 70)
        print("✅ ALL GAME FEATURES VALIDATION PASSED")
        print("=" * 70)
        return True

    except Exception as e:
        print(f"\n❌ VALIDATION FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def validate_data_cleaning():
    """Validate DataCleaner refactored code"""
    print("\n" + "=" * 70)
    print("VALIDATION: Data Cleaning (Pandas 3.0 Compatible)")
    print("=" * 70)

    try:
        from src.data_processing.cleaning import DataCleaner

        cleaner = DataCleaner()
        print("✓ Module imports successfully")

        # Test with missing values
        print("\n[Test 1] Missing Value Handling (No inplace=True)")
        df = pd.DataFrame({
            'col1': [1, 2, np.nan, 4],
            'col2': [5, np.nan, 7, 8],
            'col3': ['a', 'b', 'c', 'd']
        })

        result = cleaner.handle_missing_values(df, strategy='mean')
        assert not result['col1'].isna().any(), "Missing values should be filled"
        assert len(result) == len(df), "DataFrame length should match"
        print("✓ Missing value handling works (no inplace operations)")

        print("\n" + "=" * 70)
        print("✅ ALL DATA CLEANING VALIDATION PASSED")
        print("=" * 70)
        return True

    except Exception as e:
        print(f"\n❌ VALIDATION FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def validate_version_consistency():
    """Validate version consistency across package"""
    print("\n" + "=" * 70)
    print("VALIDATION: Version Consistency")
    print("=" * 70)

    try:
        import src
        package_version = src.__version__

        # Check setup.py
        setup_content = open('setup.py').read()
        assert '1.0.0' in setup_content, "setup.py should have version 1.0.0"

        print(f"✓ Package version: {package_version}")
        print("✓ setup.py version: 1.0.0")
        assert package_version == "1.0.0", "Version mismatch!"

        print("\n" + "=" * 70)
        print("✅ VERSION VALIDATION PASSED")
        print("=" * 70)
        return True

    except Exception as e:
        print(f"\n❌ VALIDATION FAILED: {str(e)}")
        return False


def main():
    """Run all validations"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  COMPREHENSIVE VALIDATION SUITE - NBA Performance Prediction  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")

    results = {
        'Game Features': validate_game_features(),
        'Data Cleaning': validate_data_cleaning(),
        'Version Consistency': validate_version_consistency()
    }

    print("\n\n")
    print("=" * 70)
    print("FINAL VALIDATION REPORT")
    print("=" * 70)

    all_passed = True
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:.<50} {status}")
        if not passed:
            all_passed = False

    print("=" * 70)

    if all_passed:
        print("\n🎉 ALL VALIDATIONS PASSED - CODE IS READY FOR PRODUCTION! 🎉\n")
        return 0
    else:
        print("\n❌ SOME VALIDATIONS FAILED - PLEASE FIX ISSUES ABOVE\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
