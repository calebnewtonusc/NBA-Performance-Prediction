"""
Database Integration for NBA Prediction System

PostgreSQL database with SQLAlchemy ORM
"""

from src.database.models import (
    Base,
    Team,
    Game,
    Prediction,
    ModelMetadata,
    APIUsage,
    CachedPrediction,
    DatabaseManager,
    get_or_create_team,
    record_prediction,
    update_prediction_result,
    get_model_accuracy,
)

__all__ = [
    "Base",
    "Team",
    "Game",
    "Prediction",
    "ModelMetadata",
    "APIUsage",
    "CachedPrediction",
    "DatabaseManager",
    "get_or_create_team",
    "record_prediction",
    "update_prediction_result",
    "get_model_accuracy",
]
