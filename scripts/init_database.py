#!/usr/bin/env python3
"""
Database Initialization Script

Creates all tables and performs initial setup for the NBA Prediction API.

Usage:
    python3 scripts/init_database.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://nba_user:nba_password_change_in_production@localhost:5432/nba_predictions"
)

print("=" * 70)
print("NBA Prediction API - Database Initialization")
print("=" * 70)
print()
print(f"Database URL: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")
print()

try:
    from src.database import DatabaseManager

    # Create database manager
    db_manager = DatabaseManager(DATABASE_URL)

    # Test connection
    print("[1/3] Testing database connection...")
    if db_manager.health_check():
        print("[checkmark.circle] Database connection successful")
    else:
        print("[xmark.circle] Database connection failed!")
        sys.exit(1)

    # Create tables
    print("\n[2/3] Creating database tables...")
    db_manager.create_tables()
    print("[checkmark.circle] All tables created successfully")

    # Verify tables
    print("\n[3/3] Verifying tables...")
    session = next(db_manager.get_session())
    try:
        from src.database.models import Team, Game, Prediction, ModelMetadata

        # Try to query each table
        session.query(Team).first()
        session.query(Game).first()
        session.query(Prediction).first()
        session.query(ModelMetadata).first()

        print("[checkmark.circle] All tables verified")
    finally:
        session.close()

    print()
    print("=" * 70)
    print("[checkmark.circle] DATABASE INITIALIZATION COMPLETE!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Start the API: uvicorn src.api.main:app --host 0.0.0.0 --port 8000")
    print("  2. Or use Docker: docker-compose up -d")
    print()

except ImportError as e:
    print(f"\n[xmark.circle] Import error: {e}")
    print("\nInstall required packages:")
    print("  pip install -r requirements-api.txt")
    sys.exit(1)

except Exception as e:
    print(f"\n[xmark.circle] Initialization failed: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
