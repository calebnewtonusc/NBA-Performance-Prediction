"""Authentication Routes"""

import os
import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, status, Request, Depends
from pydantic import BaseModel
from jose import jwt
from passlib.context import CryptContext

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "INSECURE-CHANGE-ME-IN-PRODUCTION")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Metrics
from threading import Lock
metrics_lock = Lock()
auth_metrics = {
    "login_attempts": 0,
    "login_successes": 0,
    "login_failures": 0,
}


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, request: Request):
    """
    Login endpoint to get JWT token

    Production: Set API_USERNAME and API_PASSWORD_HASH environment variables
    """
    logger = logging.getLogger("uvicorn")

    with metrics_lock:
        auth_metrics["login_attempts"] += 1

    # Get credentials from environment
    valid_username = os.getenv("API_USERNAME", "admin")
    password_hash = os.getenv("API_PASSWORD_HASH", None)
    plain_password_fallback = os.getenv("API_PASSWORD", None)

    # Check username
    if login_data.username != valid_username:
        with metrics_lock:
            auth_metrics["login_failures"] += 1

        client_ip = request.client.host if request.client else "unknown"
        logger.warning(
            f"⚠️  SECURITY: Failed login for '{login_data.username}' from {client_ip}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    password_valid = False
    if password_hash:
        password_valid = verify_password(login_data.password, password_hash)
    elif plain_password_fallback:
        password_valid = login_data.password == plain_password_fallback
        if password_valid:
            logger.warning("⚠️  SECURITY: Using plain text password! Set API_PASSWORD_HASH")

    if password_valid:
        with metrics_lock:
            auth_metrics["login_successes"] += 1

        access_token = create_access_token(data={"sub": login_data.username})
        return {"access_token": access_token, "token_type": "bearer"}

    # Failed login
    with metrics_lock:
        auth_metrics["login_failures"] += 1

    client_ip = request.client.host if request.client else "unknown"
    logger.warning(
        f"⚠️  SECURITY: Failed login for '{login_data.username}' from {client_ip}"
    )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_auth_metrics():
    """Get authentication metrics"""
    with metrics_lock:
        return auth_metrics.copy()
