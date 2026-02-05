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

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator
import jwt
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.models.model_manager import ModelManager
from src.data_processing.game_features import GameFeatureEngineer

# Configuration
SECRET_KEY = "your-secret-key-change-in-production"  # TODO: Move to env variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize FastAPI app
app = FastAPI(
    title="NBA Performance Prediction API",
    description="Enterprise-grade ML API for NBA game outcome predictions",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Global state
model_manager = ModelManager()
feature_engineer = GameFeatureEngineer()
loaded_models: Dict[str, any] = {}


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

    class Config:
        schema_extra = {
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


def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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
    """Load model if not already loaded"""
    key = f"{model_name}:{model_version}"
    if key not in loaded_models:
        try:
            model = model_manager.load_model(model_name, model_version)
            loaded_models[key] = {
                "model": model,
                "loaded_at": datetime.utcnow().isoformat(),
                "last_used": datetime.utcnow().isoformat(),
            }
        except FileNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model {model_name}:{model_version} not found",
            )
    else:
        loaded_models[key]["last_used"] = datetime.utcnow().isoformat()

    return loaded_models[key]["model"]


# ==================== Authentication ====================


@app.post("/api/auth/login", response_model=Token, tags=["Authentication"])
async def login(request: LoginRequest):
    """
    Login endpoint to get JWT token

    In production, validate against database with hashed passwords
    """
    # TODO: Replace with real authentication
    if request.username == "admin" and request.password == "admin":
        access_token = create_access_token(data={"sub": request.username})
        return {"access_token": access_token, "token_type": "bearer"}

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


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
@limiter.limit("60/minute")
async def health_check(request: Request):
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": time.time() - start_time,
        "models_loaded": len(loaded_models),
        "version": "1.0.0",
    }


@app.get("/api/metrics", tags=["Monitoring"])
@limiter.limit("30/minute")
async def metrics(request: Request, token: dict = Depends(verify_token)):
    """
    Prometheus-compatible metrics endpoint

    Requires authentication
    """
    return {
        "models_loaded": len(loaded_models),
        "uptime_seconds": time.time() - start_time,
        "predictions_total": 0,  # TODO: Track in database
        "cache_hits": 0,  # TODO: Track in Redis
        "cache_misses": 0,  # TODO: Track in Redis
    }


# ==================== Predictions ====================


@app.post("/api/predict", response_model=PredictionResponse, tags=["Predictions"])
@limiter.limit("100/minute")
async def predict_game(
    request: Request, prediction_request: PredictionRequest, token: dict = Depends(verify_token)
):
    """
    Predict NBA game outcome

    Returns predicted winner with confidence scores
    """
    try:
        # Load model
        model = load_model(prediction_request.model_name, prediction_request.model_version)

        # Prepare features
        features_df = pd.DataFrame([prediction_request.features.dict()])

        # Make prediction
        prediction = model.predict(features_df)[0]
        probabilities = model.predict_proba(features_df)[0]

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
            "model_used": f"{prediction_request.model_name}:{prediction_request.model_version}",
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/api/predict/batch", tags=["Predictions"])
@limiter.limit("20/minute")
async def predict_batch(
    request: Request, batch_request: BatchPredictionRequest, token: dict = Depends(verify_token)
):
    """
    Batch prediction for multiple games

    More efficient than individual predictions
    """
    if len(batch_request.games) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Maximum 100 games per batch"
        )

    try:
        model = load_model(batch_request.model_name, batch_request.model_version)

        predictions = []
        for game in batch_request.games:
            features_df = pd.DataFrame([game.features.dict()])
            prediction = model.predict(features_df)[0]
            probabilities = model.predict_proba(features_df)[0]

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
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ==================== Model Management ====================


@app.get("/api/models", tags=["Models"])
@limiter.limit("30/minute")
async def list_models(request: Request, token: dict = Depends(verify_token)):
    """List all available models"""
    try:
        models = model_manager.list_models()
        return {"models": models, "total": len(models)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/api/models/{model_name}/{version}", response_model=ModelInfo, tags=["Models"])
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


@app.post("/api/models/{model_name}/{version}/load", tags=["Models"])
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
            "timestamp": datetime.utcnow().isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.delete("/api/models/{model_name}/{version}/unload", tags=["Models"])
@limiter.limit("10/minute")
async def unload_model_endpoint(
    request: Request, model_name: str, version: str, token: dict = Depends(verify_token)
):
    """Unload a model from memory"""
    key = f"{model_name}:{version}"
    if key in loaded_models:
        del loaded_models[key]
        return {
            "status": "success",
            "message": f"Model {model_name}:{version} unloaded successfully",
            "timestamp": datetime.utcnow().isoformat(),
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


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("🚀 NBA Prediction API starting up...")
    print(f"📊 API Documentation: http://localhost:8000/api/docs")
    print(f"🔒 Authentication: POST /api/auth/login")
    print(f"🏀 Predictions: POST /api/predict")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 NBA Prediction API shutting down...")
    loaded_models.clear()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
