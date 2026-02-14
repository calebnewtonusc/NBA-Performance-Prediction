"""
Database Connection Pooling Configuration

Optimized connection management for PostgreSQL with SQLAlchemy
"""

import os
from sqlalchemy import create_engine, event, pool
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

# Base class for ORM models
Base = declarative_base()

# Database configuration from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nba_user:password@localhost:5432/nba_predictions"
)

# Connection pool settings
POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))  # Number of persistent connections
POOL_MAX_OVERFLOW = int(os.getenv("DB_POOL_MAX_OVERFLOW", "20"))  # Max overflow connections
POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))  # Seconds to wait for connection
POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "3600"))  # Recycle connections after 1 hour
POOL_PRE_PING = os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"  # Check connection validity


def create_db_engine(echo: bool = False):
    """
    Create SQLAlchemy engine with connection pooling

    Args:
        echo: Whether to log SQL statements

    Returns:
        SQLAlchemy engine with optimized connection pool
    """
    engine = create_engine(
        DATABASE_URL,
        # Connection pool configuration
        poolclass=pool.QueuePool,
        pool_size=POOL_SIZE,
        max_overflow=POOL_MAX_OVERFLOW,
        pool_timeout=POOL_TIMEOUT,
        pool_recycle=POOL_RECYCLE,
        pool_pre_ping=POOL_PRE_PING,  # Verify connections before using
        # Performance settings
        echo=echo,
        future=True,  # Use SQLAlchemy 2.0 style
        # Connection options
        connect_args={
            "options": "-c timezone=utc",  # Set timezone
            "application_name": "nba_prediction_api",
        }
    )

    # Event listeners for connection management
    @event.listens_for(engine, "connect")
    def receive_connect(dbapi_conn, connection_record):
        """Log new database connections"""
        logger.debug(f"New database connection established: {id(dbapi_conn)}")

    @event.listens_for(engine, "checkout")
    def receive_checkout(dbapi_conn, connection_record, connection_proxy):
        """Log connection checkout from pool"""
        logger.debug(f"Connection checked out from pool: {id(dbapi_conn)}")

    @event.listens_for(engine, "checkin")
    def receive_checkin(dbapi_conn, connection_record):
        """Log connection return to pool"""
        logger.debug(f"Connection returned to pool: {id(dbapi_conn)}")

    return engine


# Create global engine instance
engine = create_db_engine(echo=os.getenv("SQL_ECHO", "false").lower() == "true")

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Prevent lazy loading after commit
)

# Thread-safe session
ScopedSession = scoped_session(SessionLocal)


@contextmanager
def get_db_session():
    """
    Context manager for database sessions

    Usage:
        with get_db_session() as session:
            user = session.query(User).first()
            session.commit()
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()


def get_db():
    """
    Dependency injection for FastAPI

    Usage:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    logger.info("[checkmark.circle] Database tables initialized")


def get_pool_status():
    """
    Get connection pool statistics

    Returns:
        Dictionary with pool metrics
    """
    pool_obj = engine.pool
    return {
        "size": pool_obj.size(),
        "checked_in": pool_obj.checkedin(),
        "checked_out": pool_obj.checkedout(),
        "overflow": pool_obj.overflow(),
        "total_connections": pool_obj.size() + pool_obj.overflow(),
        "max_overflow": POOL_MAX_OVERFLOW,
        "timeout": POOL_TIMEOUT,
    }


def close_db_connections():
    """Close all database connections (for cleanup)"""
    engine.dispose()
    logger.info("[checkmark.circle] All database connections closed")


# Health check function
def check_db_health() -> bool:
    """
    Check database connectivity

    Returns:
        True if database is accessible, False otherwise
    """
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


if __name__ == "__main__":
    # Test connection pooling
    print("🔗 Testing database connection pool...")

    # Check health
    if check_db_health():
        print("[checkmark.circle] Database connection successful!")

        # Get pool status
        status = get_pool_status()
        print(f"\n[chart.bar.fill] Pool Status:")
        print(f"  Size: {status['size']}")
        print(f"  Checked In: {status['checked_in']}")
        print(f"  Checked Out: {status['checked_out']}")
        print(f"  Overflow: {status['overflow']}")
        print(f"  Total Connections: {status['total_connections']}")

        # Test session
        with get_db_session() as session:
            result = session.execute("SELECT NOW() as current_time")
            row = result.fetchone()
            print(f"\n[clock.fill] Database time: {row[0]}")

        print("\n[checkmark.circle] All tests passed!")
    else:
        print("[xmark.circle] Database connection failed!")
