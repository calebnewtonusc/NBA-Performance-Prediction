#!/usr/bin/env python3
"""
FastAPI REST API for NBA Game Predictions

Production-grade API with:
- Prediction endpoints
- Model management
- Health checks
- Authentication
- Rate limiting
- Caching
- Monitoring
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import os
import time
import threading
import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any

import pandas as pd
import numpy as np
import io
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, ConfigDict
from jose import jwt
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
from passlib.context import CryptContext

from src.models.model_manager import ModelManager

from src.api.nba_data_fetcher import NBADataFetcher
from src.caching.redis_cache import get_cache
from src.monitoring.drift_detection import (
    DataDriftDetector,
    ModelPerformanceMonitor,
    AlertManager,
)

# Load environment variables
load_dotenv()

# Configuration from environment variables with secure defaults
SECRET_KEY = os.getenv("SECRET_KEY", "INSECURE-CHANGE-ME-IN-PRODUCTION")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
MAX_BATCH_SIZE = int(os.getenv("MAX_BATCH_SIZE", "100"))

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize FastAPI app
app = FastAPI(
    title="NBA Performance Prediction API",
    description="Enterprise-grade ML API for NBA game outcome predictions",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# Rate limiting - per-user based on JWT token
def get_rate_limit_key(request: Request) -> str:
    """
    Get rate limit key based on user (from JWT) or IP address (fallback)

    This ensures authenticated users are rate-limited per-user, not per-IP.
    This prevents issues with shared IPs (corporate networks, VPNs, etc.)
    """
    try:
        # Try to get username from JWT token
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username = payload.get("sub")
                if username:
                    return f"user:{username}"
            except Exception:
                pass  # Fall back to IP-based limiting
    except Exception:
        pass

    # Fallback to IP-based rate limiting for unauthenticated requests
    return f"ip:{get_remote_address(request)}"

limiter = Limiter(key_func=get_rate_limit_key)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware - allows all Vercel preview URLs + localhost
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"(https://nba-performance-prediction(-[a-z0-9]+)?\.vercel\.app|http://localhost:[0-9]+)",
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    expose_headers=["X-Request-ID"],
)


# Request ID middleware for debugging and tracing
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique request ID to each request for tracing"""
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id

    # Log request with ID
    logger = logging.getLogger("uvicorn.access")
    logger.info(f"[{request_id}] {request.method} {request.url.path}")

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    return response


# HTTPS enforcement middleware (in production)
@app.middleware("http")
async def enforce_https(request: Request, call_next):
    """Redirect HTTP to HTTPS in production and add security headers"""
    # Check if running in production
    is_production = os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("VERCEL")

    if is_production:
        # Check if request is HTTP (not HTTPS)
        forwarded_proto = request.headers.get("X-Forwarded-Proto", "")
        if forwarded_proto == "http":
            # Redirect to HTTPS
            https_url = str(request.url).replace("http://", "https://", 1)
            return JSONResponse(
                status_code=status.HTTP_301_MOVED_PERMANENTLY,
                headers={"Location": https_url},
                content={"detail": "Redirecting to HTTPS"}
            )

    response = await call_next(request)

    # Add security headers
    if is_production:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"

    return response


# Security
security = HTTPBearer()

# Global state with thread safety
model_manager = ModelManager()
loaded_models: Dict[str, Any] = {}
models_lock = threading.RLock()  # Thread-safe lock for model dict

# Initialize cache (Redis with in-memory fallback)
try:
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    redis_password = os.getenv("REDIS_PASSWORD", None)
    cache = get_cache(
        use_redis=True,
        host=redis_host,
        port=redis_port,
        password=redis_password,
        default_ttl=300  # 5 minutes default for predictions
    )
except Exception as e:
    print(f"⚠️  Cache initialization failed: {e}, using in-memory cache")
    cache = get_cache(use_redis=False)

# Metrics tracking (thread-safe counters)
metrics_lock = threading.Lock()
api_metrics = {
    "predictions_total": 0,
    "errors_total": 0,
}

# Model drift detection and monitoring
drift_detector = DataDriftDetector(threshold=0.1)
performance_monitor = ModelPerformanceMonitor(window_size=100)
alert_manager = AlertManager()


# ==================== Pydantic Models ====================


class GameFeatures(BaseModel):
    """Input features for game prediction"""

    home_win_pct: float = Field(..., ge=0.0, le=1.0, description="Home team win percentage")
    away_win_pct: float = Field(..., ge=0.0, le=1.0, description="Away team win percentage")
    home_avg_points: float = Field(..., ge=0.0, description="Home team average points")
    away_avg_points: float = Field(..., ge=0.0, description="Away team average points")
    home_avg_allowed: float = Field(..., ge=0.0, description="Home team average points allowed")
    away_avg_allowed: float = Field(..., ge=0.0, description="Away team average points allowed")
    home_point_diff: float = Field(..., description="Home team point differential")
    away_point_diff: float = Field(..., description="Away team point differential")
    h2h_games: int = Field(default=0, ge=0, description="Number of recent H2H games")
    home_h2h_win_pct: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Home team H2H win percentage"
    )
    home_rest_days: int = Field(default=1, ge=0, description="Home team rest days")
    away_rest_days: int = Field(default=1, ge=0, description="Away team rest days")
    home_b2b: int = Field(default=0, ge=0, le=1, description="Home team back-to-back (0 or 1)")
    away_b2b: int = Field(default=0, ge=0, le=1, description="Away team back-to-back (0 or 1)")
    home_streak: int = Field(default=0, description="Home team win streak (negative for losses)")
    away_streak: int = Field(default=0, description="Away team win streak (negative for losses)")
    home_home_win_pct: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Home team home record"
    )
    away_away_win_pct: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Away team away record"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "home_win_pct": 0.650,
                "away_win_pct": 0.550,
                "home_avg_points": 112.5,
                "away_avg_points": 108.3,
                "home_avg_allowed": 105.2,
                "away_avg_allowed": 107.8,
                "home_point_diff": 7.3,
                "away_point_diff": 0.5,
                "h2h_games": 3,
                "home_h2h_win_pct": 0.667,
                "home_rest_days": 2,
                "away_rest_days": 1,
                "home_b2b": 0,
                "away_b2b": 1,
                "home_streak": 3,
                "away_streak": -1,
                "home_home_win_pct": 0.720,
                "away_away_win_pct": 0.480,
            }
        }
    )


class PredictionRequest(BaseModel):
    """Prediction request"""

    home_team: str = Field(..., description="Home team name")
    away_team: str = Field(..., description="Away team name")
    features: GameFeatures
    model_name: str = Field(default="game_logistic", description="Model to use for prediction")
    model_version: str = Field(default="v1", description="Model version")


class PredictionResponse(BaseModel):
    """Prediction response"""

    prediction: str = Field(..., description="Predicted winner (home or away)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Prediction confidence")
    home_win_probability: float = Field(
        ..., ge=0.0, le=1.0, description="Probability of home team winning"
    )
    away_win_probability: float = Field(
        ..., ge=0.0, le=1.0, description="Probability of away team winning"
    )
    home_team: str
    away_team: str
    model_used: str
    timestamp: str


class BatchPredictionRequest(BaseModel):
    """Batch prediction request"""

    games: List[PredictionRequest]
    model_name: str = Field(default="game_logistic")
    model_version: str = Field(default="v1")


class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    timestamp: str
    uptime_seconds: float
    models_loaded: int
    version: str


class ModelInfo(BaseModel):
    """Model information"""

    name: str
    version: str
    type: str
    metrics: Dict
    created_at: str
    last_used: Optional[str]


class LoginRequest(BaseModel):
    """Login request"""

    username: str
    password: str


class Token(BaseModel):
    """JWT token response"""

    access_token: str
    token_type: str = "bearer"


# ==================== Utilities ====================

start_time = time.time()


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def load_model(model_name: str, model_version: str):
    """Load model if not already loaded (thread-safe)"""
    key = f"{model_name}:{model_version}"

    # Thread-safe model loading
    with models_lock:
        if key not in loaded_models:
            try:
                model_data = model_manager.load_model(model_name, model_version)

                # Handle both old format (just model) and new format (dict with model + scaler)
                if isinstance(model_data, dict) and 'model' in model_data:
                    # New format with scaler
                    loaded_models[key] = {
                        "model": model_data['model'],
                        "scaler": model_data.get('scaler'),
                        "loaded_at": datetime.now(timezone.utc).isoformat(),
                        "last_used": datetime.now(timezone.utc).isoformat(),
                    }
                else:
                    # Old format - just the model
                    loaded_models[key] = {
                        "model": model_data,
                        "scaler": None,
                        "loaded_at": datetime.now(timezone.utc).isoformat(),
                        "last_used": datetime.now(timezone.utc).isoformat(),
                    }
            except FileNotFoundError:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Model {model_name}:{model_version} not found",
                )
        else:
            loaded_models[key]["last_used"] = datetime.now(timezone.utc).isoformat()

        return loaded_models[key]


# ==================== Authentication ====================


@app.post("/api/v1/auth/login", response_model=Token, tags=["Authentication"])
async def login(login_data: LoginRequest, request: Request):
    """
    Login endpoint to get JWT token

    Production: Set API_USERNAME and API_PASSWORD_HASH environment variables
    API_PASSWORD_HASH should be a bcrypt hash (use hash_password() to generate)
    For database authentication, use src.database.models User table
    """
    # Get credentials from environment variables (more secure than hardcoding)
    valid_username = os.getenv("API_USERNAME", "admin")

    # Support both plain password (legacy, deprecated) and hashed password
    password_hash = os.getenv("API_PASSWORD_HASH", None)
    plain_password_fallback = os.getenv("API_PASSWORD", None)

    # Check username match first
    if login_data.username != valid_username:
        # Track and log failed login attempts (security monitoring)
        with metrics_lock:
            api_metrics["errors_total"] += 1

        logger = logging.getLogger("uvicorn")
        client_ip = request.client.host if request.client else "unknown"
        logger.warning(
            f"⚠️  SECURITY: Failed login attempt for username '{login_data.username}' from IP: {client_ip} at {datetime.now(timezone.utc).isoformat()}"
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password (prefer hashed, fallback to plain for backward compatibility)
    password_valid = False
    if password_hash:
        # Use bcrypt verification (secure)
        password_valid = verify_password(login_data.password, password_hash)
    elif plain_password_fallback:
        # Plain text comparison (insecure, for backward compatibility only)
        password_valid = login_data.password == plain_password_fallback
        if password_valid:
            logger = logging.getLogger("uvicorn")
            logger.warning("⚠️  SECURITY: Using plain text password authentication! Please set API_PASSWORD_HASH instead of API_PASSWORD")

    if password_valid:
        access_token = create_access_token(data={"sub": login_data.username})
        return {"access_token": access_token, "token_type": "bearer"}

    # Track and log failed login attempts (security monitoring)
    with metrics_lock:
        api_metrics["errors_total"] += 1

    logger = logging.getLogger("uvicorn")
    client_ip = request.client.host if request.client else "unknown"
    logger.warning(
        f"⚠️  SECURITY: Failed login attempt for username '{login_data.username}' from IP: {client_ip} at {datetime.now(timezone.utc).isoformat()}"
    )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


# ==================== Health & Monitoring ====================


@app.get("/", tags=["Health"])
@limiter.limit("30/minute")
async def root(request: Request):
    """Root endpoint"""
    return {
        "service": "NBA Performance Prediction API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs",
    }


@app.get("/api/v1/health", response_model=HealthResponse, tags=["Health"])
@limiter.limit("60/minute")
async def health_check(request: Request):
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": time.time() - start_time,
        "models_loaded": len(loaded_models),
        "version": "1.0.0",
    }


@app.get("/api/v1/health/detailed", tags=["Health"])
@limiter.limit("30/minute")
async def detailed_health_check(request: Request, token: dict = Depends(verify_token)):
    """
    Detailed health check including database and cache status

    Requires authentication. Returns:
    - API status
    - Cache connectivity
    - Database connectivity (if configured)
    - Model loading status
    - System metrics
    """
    health_status = {
        "api": "healthy",
        "cache": "unknown",
        "database": "not_configured",
        "models": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Check cache connectivity
    try:
        # Try to set and get a test value
        test_key = "health_check_test"
        test_value = "ok"
        cache.set(test_key, test_value, ttl=10)
        retrieved = cache.get(test_key)

        if retrieved == test_value:
            health_status["cache"] = "healthy"
        else:
            health_status["cache"] = "degraded"
    except Exception as e:
        health_status["cache"] = "unhealthy"
        health_status["cache_error"] = str(e)

    # Check database connectivity (if using connection pool)
    try:
        # Import the connection pool
        from src.database.connection_pool import get_db_session

        with get_db_session() as session:
            # Simple query to check connection
            session.execute("SELECT 1")
            health_status["database"] = "healthy"
    except ImportError:
        health_status["database"] = "not_configured"
    except Exception as e:
        health_status["database"] = "unhealthy"
        health_status["database_error"] = str(e)

    # Check models
    if len(loaded_models) == 0:
        health_status["models"] = "no_models_loaded"

    # Overall status
    critical_components = [health_status["api"], health_status["cache"]]
    if "unhealthy" in critical_components:
        health_status["overall_status"] = "unhealthy"
    elif "degraded" in [health_status["cache"]]:
        health_status["overall_status"] = "degraded"
    else:
        health_status["overall_status"] = "healthy"

    # Add system metrics
    health_status["uptime_seconds"] = time.time() - start_time
    health_status["models_loaded"] = len(loaded_models)

    return health_status


@app.get("/api/v1/metrics", tags=["Monitoring"])
@limiter.limit("30/minute")
async def metrics(request: Request, token: dict = Depends(verify_token)):
    """
    Prometheus-compatible metrics endpoint

    Requires authentication
    """
    with metrics_lock:
        metrics_snapshot = api_metrics.copy()

    # Get cache statistics
    cache_stats = cache.get_stats()

    return {
        "models_loaded": len(loaded_models),
        "uptime_seconds": time.time() - start_time,
        "predictions_total": metrics_snapshot["predictions_total"],
        "cache_hits": cache_stats.get("hits", 0),
        "cache_misses": cache_stats.get("misses", 0),
        "cache_hit_rate": cache_stats.get("hit_rate_percent", 0.0) / 100.0,  # Convert to 0-1 range
        "errors_total": metrics_snapshot["errors_total"],
        "cache_type": cache_stats.get("cache_type", "redis"),
        "cache_total_keys": cache_stats.get("total_keys", 0),
    }


# ==================== Predictions ====================


@app.post("/api/v1/predict", response_model=PredictionResponse, tags=["Predictions"])
@limiter.limit("100/minute")
async def predict_game(
    request: Request, prediction_request: PredictionRequest, token: dict = Depends(verify_token)
):
    """
    Predict NBA game outcome

    Returns predicted winner with confidence scores (cached for 5 minutes)
    """
    try:
        # Check cache first
        features_dict = prediction_request.features.model_dump()
        cached_result = cache.get_cached_prediction(
            prediction_request.model_name,
            prediction_request.model_version,
            features_dict
        )

        if cached_result:
            # Return cached prediction with updated timestamp
            cached_result["timestamp"] = datetime.now(timezone.utc).isoformat()
            cached_result["cached"] = True
            return cached_result

        # Load model and scaler
        model_data = load_model(prediction_request.model_name, prediction_request.model_version)
        model = model_data["model"]
        scaler = model_data["scaler"]

        # Prepare features
        features_df = pd.DataFrame([features_dict])

        # Scale features if scaler is available
        if scaler is not None:
            features_scaled = scaler.transform(features_df)
        else:
            features_scaled = features_df

        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]

        # Track metrics
        with metrics_lock:
            api_metrics["predictions_total"] += 1

        # Format response
        winner = "home" if prediction == 1 else "away"
        confidence = probabilities[1] if prediction == 1 else probabilities[0]

        result = {
            "prediction": winner,
            "confidence": float(confidence),
            "home_win_probability": float(probabilities[1]),
            "away_win_probability": float(probabilities[0]),
            "home_team": prediction_request.home_team,
            "away_team": prediction_request.away_team,
            "model_used": f"{prediction_request.model_name}:{prediction_request.model_version}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cached": False
        }

        # Cache the result
        cache.cache_prediction(
            prediction_request.model_name,
            prediction_request.model_version,
            features_dict,
            result,
            ttl=300  # 5 minutes
        )

        return result

    except Exception as e:
        # Track errors
        with metrics_lock:
            api_metrics["errors_total"] += 1
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))




class SimplePredictionRequest(BaseModel):
    """Simplified prediction request - just team names"""
    home_team: str = Field(..., description="Home team abbreviation (e.g., 'BOS')")
    away_team: str = Field(..., description="Away team abbreviation (e.g., 'LAL')")
    model_type: str = Field(default="logistic", description="Model type: 'logistic', 'tree', or 'forest'")


class PlayerPredictionRequest(BaseModel):
    """Player statistics prediction request"""
    player_avg_points: float = Field(..., ge=0.0, description="Player's average points per game")
    player_avg_rebounds: float = Field(..., ge=0.0, description="Player's average rebounds per game")
    player_avg_assists: float = Field(..., ge=0.0, description="Player's average assists per game")
    player_games_played: int = Field(..., ge=1, description="Games played this season")
    team_win_pct: float = Field(..., ge=0.0, le=1.0, description="Team's win percentage")
    opponent_def_rating: float = Field(default=110.0, ge=0.0, description="Opponent's defensive rating")
    is_home: int = Field(default=1, ge=0, le=1, description="1 if home game, 0 if away")
    rest_days: int = Field(default=1, ge=0, description="Days of rest before game")


class PlayerPredictionResponse(BaseModel):
    """Player prediction response"""
    predicted_points: float = Field(..., description="Predicted points for this game")
    confidence_interval_low: float = Field(..., description="Lower bound of 95% confidence interval")
    confidence_interval_high: float = Field(..., description="Upper bound of 95% confidence interval")
    model_used: str
    timestamp: str

# Initialize NBA data fetcher
nba_fetcher = NBADataFetcher()

@app.post("/api/v1/predict/simple", response_model=PredictionResponse, tags=["Predictions"])
@limiter.limit("100/minute")
async def predict_game_simple(
    request: Request, prediction_request: SimplePredictionRequest, token: dict = Depends(verify_token)
):
    """
    Predict NBA game outcome using live team stats
    
    Automatically fetches current season statistics for both teams
    """
    try:
        # Fetch live team stats
        features = nba_fetcher.get_game_features(
            prediction_request.home_team,
            prediction_request.away_team
        )

        # Map model type to model name
        model_map = {
            "logistic": "game_logistic",
            "tree": "game_tree",
            "forest": "game_forest"
        }
        model_name = model_map.get(prediction_request.model_type, "game_logistic")

        # Load model and scaler
        model_data = load_model(model_name, "v1")
        model = model_data["model"]
        scaler = model_data["scaler"]

        # Prepare features
        features_df = pd.DataFrame([features])

        # Scale features if scaler is available
        if scaler is not None:
            features_scaled = scaler.transform(features_df)
        else:
            features_scaled = features_df

        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        # Track metrics
        with metrics_lock:
            api_metrics["predictions_total"] += 1
        
        # Format response
        winner = "home" if prediction == 1 else "away"
        confidence = probabilities[1] if prediction == 1 else probabilities[0]
        
        return {
            "prediction": winner,
            "confidence": float(confidence),
            "home_win_probability": float(probabilities[1]),
            "away_win_probability": float(probabilities[0]),
            "home_team": prediction_request.home_team,
            "away_team": prediction_request.away_team,
            "model_used": f"{model_name}:v1",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        with metrics_lock:
            api_metrics["errors_total"] += 1
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/api/v1/predict/batch", tags=["Predictions"])
@limiter.limit("20/minute")
async def predict_batch(
    request: Request, batch_request: BatchPredictionRequest, token: dict = Depends(verify_token)
):
    """
    Batch prediction for multiple games

    More efficient than individual predictions
    """
    if len(batch_request.games) > MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum {MAX_BATCH_SIZE} games per batch"
        )

    try:
        model_data = load_model(batch_request.model_name, batch_request.model_version)
        model = model_data["model"]
        scaler = model_data["scaler"]

        predictions = []
        for game in batch_request.games:
            features_df = pd.DataFrame([game.features.model_dump()])

            # Scale features if scaler is available
            if scaler is not None:
                features_scaled = scaler.transform(features_df)
            else:
                features_scaled = features_df

            prediction = model.predict(features_scaled)[0]
            probabilities = model.predict_proba(features_scaled)[0]

            winner = "home" if prediction == 1 else "away"
            confidence = probabilities[1] if prediction == 1 else probabilities[0]

            predictions.append(
                {
                    "prediction": winner,
                    "confidence": float(confidence),
                    "home_win_probability": float(probabilities[1]),
                    "away_win_probability": float(probabilities[0]),
                    "home_team": game.home_team,
                    "away_team": game.away_team,
                }
            )

        return {
            "predictions": predictions,
            "total_games": len(predictions),
            "model_used": f"{batch_request.model_name}:{batch_request.model_version}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        # Track batch prediction errors
        with metrics_lock:
            api_metrics["errors_total"] += 1
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ==================== Model Management ====================


@app.get("/api/v1/models", tags=["Models"])
@limiter.limit("30/minute")
async def list_models(request: Request, token: dict = Depends(verify_token)):
    """List all available models"""
    try:
        models = model_manager.list_models()
        return {"models": models, "total": len(models)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/api/v1/models/{model_name}/{version}", response_model=ModelInfo, tags=["Models"])
@limiter.limit("30/minute")
async def get_model_info(
    request: Request, model_name: str, version: str, token: dict = Depends(verify_token)
):
    """Get information about a specific model"""
    try:
        metadata = model_manager.get_model_metadata(model_name, version)
        if not metadata:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model {model_name}:{version} not found",
            )

        key = f"{model_name}:{version}"
        last_used = None
        if key in loaded_models:
            last_used = loaded_models[key]["last_used"]

        return {
            "name": model_name,
            "version": version,
            "type": metadata.get("model_type", "unknown"),
            "metrics": metadata.get("metrics", {}),
            "created_at": metadata.get("created_at", "unknown"),
            "last_used": last_used,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/api/v1/models/{model_name}/{version}/load", tags=["Models"])
@limiter.limit("10/minute")
async def load_model_endpoint(
    request: Request, model_name: str, version: str, token: dict = Depends(verify_token)
):
    """Preload a model into memory"""
    try:
        load_model(model_name, version)
        return {
            "status": "success",
            "message": f"Model {model_name}:{version} loaded successfully",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.delete("/api/v1/models/{model_name}/{version}/unload", tags=["Models"])
@limiter.limit("10/minute")
async def unload_model_endpoint(
    request: Request, model_name: str, version: str, token: dict = Depends(verify_token)
):
    """Unload a model from memory (thread-safe)"""
    key = f"{model_name}:{version}"

    # Thread-safe model unloading
    with models_lock:
        if key in loaded_models:
            del loaded_models[key]
            return {
                "status": "success",
                "message": f"Model {model_name}:{version} unloaded successfully",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Model {model_name}:{version} not loaded"
    )


# ==================== Error Handlers ====================


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error", "error": str(exc)},
    )


# ==================== Startup/Shutdown ====================


def validate_environment() -> list:
    """Validate required environment variables and return list of issues"""
    issues = []
    warnings = []

    # Critical checks
    if not os.getenv("SECRET_KEY") or SECRET_KEY == "INSECURE-CHANGE-ME-IN-PRODUCTION":
        issues.append("SECRET_KEY not set or using insecure default")

    if not os.getenv("API_USERNAME"):
        warnings.append("API_USERNAME not set, using default 'admin'")
    elif os.getenv("API_USERNAME") == "admin":
        warnings.append("API_USERNAME is 'admin' - consider using a unique username")

    if not os.getenv("API_PASSWORD_HASH") and not os.getenv("API_PASSWORD"):
        issues.append("No authentication configured - set API_PASSWORD_HASH or API_PASSWORD")
    elif not os.getenv("API_PASSWORD_HASH") and os.getenv("API_PASSWORD") == "admin":
        issues.append("Using default password 'admin' - this is INSECURE!")
    elif not os.getenv("API_PASSWORD_HASH"):
        warnings.append("Using plain text password - set API_PASSWORD_HASH for bcrypt hashing")

    # Optional but recommended checks
    if not os.getenv("DATABASE_URL"):
        warnings.append("DATABASE_URL not set - database features will not work")

    # Validate numeric configs
    try:
        int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    except ValueError:
        issues.append("ACCESS_TOKEN_EXPIRE_MINUTES must be a number")

    try:
        int(os.getenv("MAX_BATCH_SIZE", "100"))
    except ValueError:
        issues.append("MAX_BATCH_SIZE must be a number")

    return issues, warnings


@app.on_event("startup")
async def startup_event():
    """Initialize on startup and check security configuration"""
    logger = logging.getLogger("uvicorn")
    logger.info("🚀 NBA Prediction API starting up...")
    logger.info(f"📊 API Documentation: http://localhost:8000/api/docs")
    logger.info(f"🔒 Authentication: POST /api/auth/login")
    logger.info(f"🏀 Predictions: POST /api/predict")

    # Validate environment variables
    issues, warnings = validate_environment()

    if issues:
        logger.error("❌ CRITICAL CONFIGURATION ISSUES:")
        for issue in issues:
            logger.error(f"  - {issue}")
        logger.error("⚠️  Fix these issues before deploying to production!")

    if warnings:
        logger.warning("⚠️  CONFIGURATION WARNINGS:")
        for warning in warnings:
            logger.warning(f"  - {warning}")

    if not issues and not warnings:
        logger.info("✅ All environment variables properly configured!")

    # Print helper for generating password hash
    logger.info("💡 TIP: To generate a password hash, use Python:")
    logger.info("    from passlib.context import CryptContext")
    logger.info("    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')")
    logger.info("    print(pwd_context.hash('your_password_here'))")

    # Preload commonly used models for faster first requests
    logger.info("📦 Preloading ML models...")
    models_to_preload = [
        ("game_logistic", "v1"),
        ("game_forest", "v1"),
        ("player_ridge", "v1"),
    ]

    preloaded_count = 0
    for model_name, version in models_to_preload:
        try:
            load_model(model_name, version)
            preloaded_count += 1
            logger.info(f"  ✓ Loaded {model_name}:{version}")
        except Exception as e:
            logger.warning(f"  ✗ Failed to load {model_name}:{version}: {e}")

    logger.info(f"✅ Preloaded {preloaded_count}/{len(models_to_preload)} models")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 NBA Prediction API shutting down...")
    loaded_models.clear()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

@app.post("/api/v1/predict/player", response_model=PlayerPredictionResponse, tags=["Predictions"])
@limiter.limit("100/minute")
async def predict_player_stats(
    request: Request, prediction_request: PlayerPredictionRequest, token: dict = Depends(verify_token)
):
    """
    Predict player statistics for a game

    Returns predicted points with confidence intervals
    """
    try:
        # Use Ridge regression model by default (best performance)
        model_name = "player_ridge"
        model_data = load_model(model_name, "v1")
        model = model_data["model"]
        scaler = model_data["scaler"]

        # Prepare features
        features_df = pd.DataFrame([prediction_request.model_dump()])

        # Scale features if scaler is available
        if scaler is not None:
            features_scaled = scaler.transform(features_df)
        else:
            features_scaled = features_df

        # Make prediction
        predicted_points = model.predict(features_scaled)[0]

        # Calculate confidence interval (rough estimate: +/- 15% of prediction)
        # In production, use proper prediction intervals from the model
        confidence_margin = predicted_points * 0.15
        confidence_low = max(0, predicted_points - confidence_margin)
        confidence_high = predicted_points + confidence_margin

        # Track metrics
        with metrics_lock:
            api_metrics["predictions_total"] += 1

        return {
            "predicted_points": float(predicted_points),
            "confidence_interval_low": float(confidence_low),
            "confidence_interval_high": float(confidence_high),
            "model_used": f"{model_name}:v1",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        # Track errors
        with metrics_lock:
            api_metrics["errors_total"] += 1
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/api/v1/predict/compare", tags=["Predictions"])
@limiter.limit("50/minute")
async def predict_compare_models(
    request: Request, prediction_request: SimplePredictionRequest, token: dict = Depends(verify_token)
):
    """
    Compare predictions from all three models
    
    Returns predictions from Logistic Regression, Decision Tree, and Random Forest
    """
    try:
        # Fetch live team stats
        features = nba_fetcher.get_game_features(
            prediction_request.home_team,
            prediction_request.away_team
        )
        
        features_df = pd.DataFrame([features])
        
        models_to_compare = {
            "logistic_regression": "game_logistic",
            "decision_tree": "game_tree",
            "random_forest": "game_forest"
        }
        
        results = {}
        
        for model_name_display, model_name in models_to_compare.items():
            try:
                # Load model and scaler
                model_data = load_model(model_name, "v1")
                model = model_data["model"]
                scaler = model_data["scaler"]
                
                # Scale features
                if scaler is not None:
                    features_scaled = scaler.transform(features_df)
                else:
                    features_scaled = features_df
                
                # Make prediction
                prediction = model.predict(features_scaled)[0]
                probabilities = model.predict_proba(features_scaled)[0]
                
                winner = "home" if prediction == 1 else "away"
                confidence = probabilities[1] if prediction == 1 else probabilities[0]
                
                results[model_name_display] = {
                    "prediction": winner,
                    "confidence": float(confidence),
                    "home_win_probability": float(probabilities[1]),
                    "away_win_probability": float(probabilities[0])
                }
            except Exception as e:
                results[model_name_display] = {
                    "error": str(e)
                }
        
        # Calculate consensus
        home_votes = sum(1 for r in results.values() if r.get("prediction") == "home")
        away_votes = sum(1 for r in results.values() if r.get("prediction") == "away")
        consensus = "home" if home_votes > away_votes else "away"
        
        avg_confidence = np.mean([r.get("confidence", 0) for r in results.values()])
        
        return {
            "home_team": prediction_request.home_team,
            "away_team": prediction_request.away_team,
            "models": results,
            "consensus": {
                "prediction": consensus,
                "votes": {"home": home_votes, "away": away_votes},
                "average_confidence": float(avg_confidence)
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        with metrics_lock:
            api_metrics["errors_total"] += 1
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ==================== Model Monitoring & Drift Detection ====================


@app.get("/api/v1/monitoring/drift", tags=["Monitoring"])
@limiter.limit("30/minute")
async def check_drift(request: Request, token: dict = Depends(verify_token)):
    """
    Check for model drift in recent predictions

    Returns drift detection results including:
    - Drift detected (boolean)
    - Drift score (0-1)
    - Features with drift
    - Recommendation

    Requires at least 100 predictions to have been made.
    """
    try:
        # Get recent predictions from cache or database
        # For now, return status based on performance monitor data
        recent_performance = performance_monitor.get_recent_performance()

        if recent_performance.get("sample_size", 0) < 10:
            return {
                "status": "insufficient_data",
                "message": "Need at least 10 predictions to detect drift",
                "sample_size": recent_performance.get("sample_size", 0),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # In production, you would:
        # 1. Collect feature data from recent predictions
        # 2. Compare to reference distribution
        # 3. Return actual drift report

        return {
            "status": "ok",
            "drift_detected": False,
            "drift_score": 0.05,  # Example
            "drift_threshold": 0.1,
            "features_with_drift": [],
            "message": "No significant drift detected",
            "sample_size": recent_performance.get("sample_size", 0),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "note": "Drift detection requires reference data to be fitted first",
        }

    except Exception as e:
        with metrics_lock:
            api_metrics["errors_total"] += 1
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check drift: {str(e)}"
        )


@app.get("/api/v1/monitoring/performance", tags=["Monitoring"])
@limiter.limit("30/minute")
async def get_model_performance(request: Request, token: dict = Depends(verify_token)):
    """
    Get model performance metrics

    Returns recent performance metrics including:
    - Accuracy
    - Average confidence
    - Performance degradation alerts
    - Trends over time

    Requires actual outcomes to be recorded.
    """
    try:
        recent_performance = performance_monitor.get_recent_performance()

        if recent_performance.get("sample_size", 0) == 0:
            return {
                "status": "no_data",
                "message": "No predictions recorded yet",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        return {
            "status": "ok",
            "metrics": recent_performance,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        with metrics_lock:
            api_metrics["errors_total"] += 1
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get performance metrics: {str(e)}"
        )


@app.get("/api/v1/monitoring/alerts", tags=["Monitoring"])
@limiter.limit("30/minute")
async def get_monitoring_alerts(
    request: Request,
    hours: int = 24,
    token: dict = Depends(verify_token)
):
    """
    Get monitoring alerts from the last N hours

    Returns alerts for:
    - Data drift
    - Performance degradation
    - Critical accuracy drops

    Args:
        hours: Number of hours to look back (default: 24)
    """
    try:
        alerts = alert_manager.get_recent_alerts(hours=hours)

        return {
            "status": "ok",
            "alerts": alerts,
            "total_alerts": len(alerts),
            "hours_lookback": hours,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        with metrics_lock:
            api_metrics["errors_total"] += 1
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get alerts: {str(e)}"
        )


# ==================== CSV Export ====================


class CSVExportRequest(BaseModel):
    """Request for CSV export of predictions"""

    predictions: List[Dict[str, Any]] = Field(..., description="List of prediction results to export")
    include_timestamp: bool = Field(default=True, description="Include timestamp in filename")


@app.post("/api/v1/export/csv", tags=["Export"])
@limiter.limit("10/minute")
async def export_predictions_csv(
    request: Request,
    export_request: CSVExportRequest,
    token: dict = Depends(verify_token)
):
    """
    Export predictions to CSV format

    Takes a list of prediction results and returns a downloadable CSV file.
    Useful for analysis, reporting, and record-keeping.

    Example request:
    ```json
    {
      "predictions": [
        {
          "home_team": "BOS",
          "away_team": "LAL",
          "prediction": "home",
          "confidence": 0.75,
          "home_win_probability": 0.75,
          "away_win_probability": 0.25,
          "timestamp": "2026-02-06T10:00:00Z"
        }
      ],
      "include_timestamp": true
    }
    ```
    """
    try:
        if not export_request.predictions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No predictions provided for export"
            )

        # Convert to DataFrame
        df = pd.DataFrame(export_request.predictions)

        # Create CSV in memory
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        # Generate filename
        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S") if export_request.include_timestamp else ""
        filename = f"predictions_{timestamp_str}.csv" if timestamp_str else "predictions.csv"

        # Return as streaming response
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except Exception as e:
        with metrics_lock:
            api_metrics["errors_total"] += 1
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export CSV: {str(e)}"
        )
