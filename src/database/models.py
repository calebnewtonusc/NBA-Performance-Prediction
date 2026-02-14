"""
Database Models for NBA Prediction System

SQLAlchemy models for PostgreSQL database
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
    JSON,
    Index,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.pool import QueuePool

Base = declarative_base()


# ==================== Database Models ====================


class Team(Base):
    """NBA Team"""

    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nba_team_id = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    abbreviation = Column(String(10), nullable=False)
    city = Column(String(50))
    conference = Column(String(10))  # East/West
    division = Column(String(20))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    home_games = relationship("Game", foreign_keys="Game.home_team_id", back_populates="home_team")
    away_games = relationship("Game", foreign_keys="Game.away_team_id", back_populates="away_team")

    def __repr__(self):
        return f"<Team(name='{self.name}', abbreviation='{self.abbreviation}')>"


class Game(Base):
    """NBA Game"""

    __tablename__ = "games"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nba_game_id = Column(Integer, unique=True, nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    season = Column(Integer, nullable=False, index=True)

    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)

    home_score = Column(Integer)
    away_score = Column(Integer)

    # Game status
    status = Column(String(20), default="scheduled")  # scheduled, in_progress, final
    quarter = Column(Integer)

    # Additional metadata
    venue = Column(String(100))
    attendance = Column(Integer)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_games")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_games")
    predictions = relationship("Prediction", back_populates="game")

    # Indexes
    __table_args__ = (
        Index("ix_games_date_home", "date", "home_team_id"),
        Index("ix_games_date_away", "date", "away_team_id"),
    )

    def __repr__(self):
        return f"<Game(date='{self.date}', home={self.home_team_id} vs away={self.away_team_id})>"


class Prediction(Base):
    """Model Predictions"""

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False, index=True)

    # Model info
    model_name = Column(String(50), nullable=False, index=True)
    model_version = Column(String(20), nullable=False)

    # Prediction
    predicted_winner = Column(String(10), nullable=False)  # 'home' or 'away'
    home_win_probability = Column(Float, nullable=False)
    away_win_probability = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)

    # Features used (JSON)
    features = Column(JSON)

    # Result tracking
    actual_winner = Column(String(10))  # Filled after game completion
    correct = Column(Boolean)  # True if prediction was correct

    # Metadata
    predicted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    user_id = Column(String(50))  # API user who made the prediction

    # Relationships
    game = relationship("Game", back_populates="predictions")

    # Indexes
    __table_args__ = (
        Index("ix_predictions_model", "model_name", "model_version"),
        Index("ix_predictions_date", "predicted_at"),
    )

    def __repr__(self):
        return f"<Prediction(game_id={self.game_id}, model='{self.model_name}:{self.model_version}', winner='{self.predicted_winner}')>"


class ModelMetadata(Base):
    """Model Metadata and Performance Tracking"""

    __tablename__ = "model_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, index=True)
    version = Column(String(20), nullable=False, index=True)

    # Model info
    model_type = Column(String(50), nullable=False)
    framework = Column(String(20))  # sklearn, pytorch, xgboost, etc.

    # Training info
    trained_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    training_samples = Column(Integer)
    training_duration_seconds = Column(Float)

    # Performance metrics (JSON)
    metrics = Column(JSON)  # accuracy, precision, recall, f1, etc.

    # Hyperparameters (JSON)
    hyperparameters = Column(JSON)

    # Status
    status = Column(String(20), default="active")  # active, deprecated, archived
    is_production = Column(Boolean, default=False)

    # Usage tracking
    prediction_count = Column(Integer, default=0)
    last_used_at = Column(DateTime)

    # Drift detection
    drift_detected = Column(Boolean, default=False)
    drift_score = Column(Float)
    last_drift_check = Column(DateTime)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Indexes
    __table_args__ = (Index("ix_model_name_version", "name", "version", unique=True),)

    def __repr__(self):
        return f"<ModelMetadata(name='{self.name}', version='{self.version}', status='{self.status}')>"


class APIUsage(Base):
    """API Usage Tracking"""

    __tablename__ = "api_usage"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), nullable=False, index=True)
    endpoint = Column(String(100), nullable=False, index=True)
    method = Column(String(10), nullable=False)

    # Request details
    request_data = Column(JSON)
    response_status = Column(Integer)
    response_time_ms = Column(Float)

    # Resource usage
    model_name = Column(String(50))
    model_version = Column(String(20))

    # Metadata
    ip_address = Column(String(45))
    user_agent = Column(String(200))

    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Indexes
    __table_args__ = (
        Index("ix_api_usage_user_timestamp", "user_id", "timestamp"),
        Index("ix_api_usage_endpoint", "endpoint", "timestamp"),
    )

    def __repr__(self):
        return f"<APIUsage(user='{self.user_id}', endpoint='{self.endpoint}', timestamp='{self.timestamp}')>"


class CachedPrediction(Base):
    """Cached Predictions for Performance"""

    __tablename__ = "cached_predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Cache key (hash of features + model)
    cache_key = Column(String(64), unique=True, nullable=False, index=True)

    # Model info
    model_name = Column(String(50), nullable=False)
    model_version = Column(String(20), nullable=False)

    # Prediction result
    prediction_result = Column(JSON, nullable=False)

    # Cache metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    expires_at = Column(DateTime, nullable=False, index=True)
    hit_count = Column(Integer, default=0)
    last_accessed = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<CachedPrediction(cache_key='{self.cache_key}', hits={self.hit_count})>"


# ==================== Database Manager ====================


class DatabaseManager:
    """Database connection and session manager"""

    def __init__(self, database_url: str):
        """
        Initialize database manager

        Args:
            database_url: PostgreSQL connection string
                         e.g., "postgresql://user:password@localhost/nba_predictions"
        """
        self.engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            echo=False,  # Set to True for SQL logging
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)
        print("[checkmark.circle] Database tables created successfully")

    def drop_tables(self):
        """Drop all tables (use with caution!)"""
        Base.metadata.drop_all(bind=self.engine)
        print("[exclamationmark.triangle]  Database tables dropped")

    def get_session(self):
        """Get database session"""
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def health_check(self) -> bool:
        """Check database connectivity"""
        try:
            session = self.SessionLocal()
            session.execute("SELECT 1")
            session.close()
            return True
        except Exception:
            return False


# ==================== Helper Functions ====================


def get_or_create_team(session, nba_team_id: int, name: str, abbreviation: str) -> Team:
    """Get team or create if doesn't exist"""
    team = session.query(Team).filter(Team.nba_team_id == nba_team_id).first()
    if not team:
        team = Team(nba_team_id=nba_team_id, name=name, abbreviation=abbreviation)
        session.add(team)
        session.commit()
    return team


def record_prediction(
    session,
    game_id: int,
    model_name: str,
    model_version: str,
    predicted_winner: str,
    home_win_prob: float,
    away_win_prob: float,
    confidence: float,
    features: dict,
    user_id: Optional[str] = None,
) -> Prediction:
    """Record a prediction in the database"""
    prediction = Prediction(
        game_id=game_id,
        model_name=model_name,
        model_version=model_version,
        predicted_winner=predicted_winner,
        home_win_probability=home_win_prob,
        away_win_probability=away_win_prob,
        confidence=confidence,
        features=features,
        user_id=user_id,
    )
    session.add(prediction)
    session.commit()
    return prediction


def update_prediction_result(session, prediction_id: int, actual_winner: str) -> Prediction:
    """Update prediction with actual result"""
    prediction = session.query(Prediction).filter(Prediction.id == prediction_id).first()
    if prediction:
        prediction.actual_winner = actual_winner
        prediction.correct = prediction.predicted_winner == actual_winner
        session.commit()
    return prediction


def get_model_accuracy(session, model_name: str, model_version: str, days: int = 30) -> float:
    """Calculate model accuracy over recent predictions"""
    from sqlalchemy import func

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    total = (
        session.query(func.count(Prediction.id))
        .filter(
            Prediction.model_name == model_name,
            Prediction.model_version == model_version,
            Prediction.predicted_at >= cutoff_date,
            Prediction.correct.isnot(None),
        )
        .scalar()
    )

    if total == 0:
        return 0.0

    correct = (
        session.query(func.count(Prediction.id))
        .filter(
            Prediction.model_name == model_name,
            Prediction.model_version == model_version,
            Prediction.predicted_at >= cutoff_date,
            Prediction.correct == True,  # noqa: E712
        )
        .scalar()
    )

    return correct / total if total > 0 else 0.0
