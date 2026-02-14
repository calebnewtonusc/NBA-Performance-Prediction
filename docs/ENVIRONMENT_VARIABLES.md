# Environment Variables Reference

Complete reference for all environment variables used in the NBA Performance Prediction system.

---

## Table of Contents

1. [Overview](#overview)
2. [Backend (Railway)](#backend-railway)
3. [Frontend (Streamlit Cloud)](#frontend-streamlit-cloud)
4. [Local Development](#local-development)
5. [Generating Secrets](#generating-secrets)
6. [Security Best Practices](#security-best-practices)

---

## Overview

Environment variables are used to configure the application across different environments (development, staging, production) without changing code.

### Variable Precedence

1. Environment variables (highest priority)
2. `.env` file (local development)
3. Default values in code (lowest priority)

---

## Backend (Railway)

### Required Variables

| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| `SECRET_KEY` | string | `xK7vP9m...` | JWT token signing key. Generate with `scripts/generate_secrets.py` |
| `API_USERNAME` | string | `admin` | Username for API authentication |
| `API_PASSWORD` | string | `secure_pass_123` | Password for API authentication |

### Database Variables (Auto-configured by Railway)

| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| `DATABASE_URL` | string | `postgresql://user:pass@host:5432/db` | PostgreSQL connection string (auto-set by Railway) |
| `REDIS_HOST` | string | `redis.railway.internal` | Redis host (auto-set by Railway) |
| `REDIS_PORT` | integer | `6379` | Redis port (auto-set by Railway) |
| `REDIS_PASSWORD` | string | `redis_pass_123` | Redis password (auto-set by Railway) |

### API Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ACCESS_TOKEN_EXPIRE_MINUTES` | integer | `30` | JWT token expiration time in minutes |
| `MAX_BATCH_SIZE` | integer | `100` | Maximum number of predictions per batch request |
| `ALLOWED_ORIGINS` | string | `http://localhost:8501` | Comma-separated list of allowed CORS origins |

### Monitoring & Logging

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ENABLE_MONITORING` | boolean | `true` | Enable Prometheus metrics endpoint |
| `LOG_LEVEL` | string | `INFO` | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |

### Server Configuration (Local Dev Only)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `API_HOST` | string | `0.0.0.0` | API host binding (Railway overrides this) |
| `API_PORT` | integer | `8000` | API port (Railway overrides this) |

---

## Frontend (Streamlit Cloud)

Configure in Streamlit Cloud → App Settings → Secrets as TOML format:

```toml
# Required: Backend API URL
API_BASE_URL = "https://your-railway-app.up.railway.app"

# Required: API Authentication
API_USERNAME = "admin"
API_PASSWORD = "your-secure-password"
```

### Variable Descriptions

| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| `API_BASE_URL` | string | `https://api.railway.app` | Base URL of the Railway backend API |
| `API_USERNAME` | string | `admin` | Username for API authentication (must match backend) |
| `API_PASSWORD` | string | `secure_pass_123` | Password for API authentication (must match backend) |

---

## Local Development

### Create `.env` File

Copy `.env.example` and customize:

```bash
cp .env.example .env
```

Edit `.env`:

```bash
# ==================== Security ====================
SECRET_KEY=local-dev-secret-key-change-in-production
API_USERNAME=admin
API_PASSWORD=admin

# ==================== Database ====================
DATABASE_URL=postgresql://nba_user:nba_password@localhost:5432/nba_predictions

# ==================== Redis ====================
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=redis_password

# ==================== API Configuration ====================
API_HOST=0.0.0.0
API_PORT=8000
ACCESS_TOKEN_EXPIRE_MINUTES=30
MAX_BATCH_SIZE=100

# ==================== CORS ====================
ALLOWED_ORIGINS=http://localhost:8501,http://localhost:3000,http://localhost:8000

# ==================== Monitoring ====================
ENABLE_MONITORING=true
LOG_LEVEL=DEBUG
```

### Docker Compose Environment

When using `docker-compose up`, edit `docker-compose.yml` directly or use `.env`:

```bash
# docker-compose.yml uses these patterns:
POSTGRES_USER: nba_user
POSTGRES_PASSWORD: nba_password_change_in_production
REDIS_PASSWORD: redis_password_change_in_production
```

---

## Generating Secrets

### Use Built-in Script

```bash
python scripts/generate_secrets.py
```

Output example:
```
======================================================================
🔐 NBA Performance Prediction - Production Secrets Generator
======================================================================

Copy these values to your environment variables:

----------------------------------------------------------------------
# Railway Backend Environment Variables
----------------------------------------------------------------------

SECRET_KEY=xK7vP9mQ2tL5nW8eR4yU6iO0aS3dF7gH9jK1lZ2xC5vB8nM4qW6eR0tY3uI
API_PASSWORD=vL8kJ2mN5pQ3rT6wY9zA1sD4fG7hK0lX

# PostgreSQL (Railway will auto-generate DATABASE_URL)
POSTGRES_PASSWORD=nE4mR7pS0tV3wY6zB9cD2fG5hJ8k

# Redis (Railway will auto-configure connection)
REDIS_PASSWORD=aS3dF6gH9jK2lZ5xC8vB1nM4qW7e

----------------------------------------------------------------------
# Streamlit Cloud Secrets
----------------------------------------------------------------------

# Add to Streamlit Cloud > App Settings > Secrets
API_BASE_URL = "https://your-railway-app.up.railway.app"
API_USERNAME = "admin"
API_PASSWORD = "vL8kJ2mN5pQ3rT6wY9zA1sD4fG7hK0lX"
```

### Manual Generation

Using Python:
```python
import secrets

# SECRET_KEY (32 bytes)
print(secrets.token_urlsafe(32))

# Passwords (24 characters)
alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
print(''.join(secrets.choice(alphabet) for _ in range(24)))
```

Using OpenSSL:
```bash
# SECRET_KEY
openssl rand -base64 32

# Password
openssl rand -base64 18
```

---

## Security Best Practices

### 1. Never Commit Secrets

Ensure `.gitignore` includes:
```
.env
.env.local
.env.production
.streamlit/secrets.toml
```

### 2. Use Different Secrets Per Environment

| Environment | SECRET_KEY | Passwords | Database |
|-------------|------------|-----------|----------|
| Development | Simple key | Simple passwords | Local |
| Staging | Strong key | Strong passwords | Separate DB |
| Production | Strong key | Strong passwords | Separate DB |

### 3. Rotate Secrets Regularly

Recommended rotation schedule:
- **SECRET_KEY**: Every 90 days
- **API_PASSWORD**: Every 90 days
- **Database passwords**: Every 180 days

### 4. Secure Storage

Store secrets in:
- **Development**: `.env` file (git-ignored)
- **Production**: Railway/Streamlit Cloud secrets (encrypted)
- **Backup**: Password manager (1Password, Bitwarden, etc.)

Never store secrets in:
- Git commits
- Slack/Discord/Email
- Code comments
- README files

### 5. Minimal Permissions

Grant only necessary permissions:
- **API_USERNAME**: Read-only if possible
- **Database user**: Only required tables
- **Redis**: Restrict to specific keys

### 6. Monitor Access

Enable logging for:
- Failed login attempts
- Authentication errors
- Database connection failures
- Unusual API usage patterns

---

## Railway Environment Setup

### Setting Variables in Railway

1. **Via Dashboard**:
   - Go to your Railway project
   - Click on your web service
   - Click "Variables" tab
   - Click "+ New Variable"
   - Add each variable

2. **Via Railway CLI**:
   ```bash
   railway variables set SECRET_KEY=your-secret-key
   railway variables set API_PASSWORD=your-password
   ```

### Viewing Current Variables

```bash
# List all variables
railway variables

# Get specific variable (will show value)
railway variables get SECRET_KEY
```

### Deleting Variables

```bash
railway variables delete VARIABLE_NAME
```

---

## Streamlit Cloud Environment Setup

### Setting Secrets in Streamlit Cloud

1. Go to https://share.streamlit.io
2. Select your app
3. Click "⋮" menu → "Settings"
4. Click "Secrets" section
5. Add secrets in TOML format:

```toml
API_BASE_URL = "https://your-railway-app.up.railway.app"
API_USERNAME = "admin"
API_PASSWORD = "your-secure-password"
```

6. Click "Save"
7. App will automatically restart

### Accessing Secrets in Code

```python
import streamlit as st

# Access secrets
api_url = st.secrets["API_BASE_URL"]
username = st.secrets["API_USERNAME"]
password = st.secrets["API_PASSWORD"]
```

**Note**: For local development, secrets are read from `.streamlit/secrets.toml` (git-ignored).

---

## Validation Checklist

Before deployment, verify:

- [ ] All required variables are set
- [ ] No default/insecure values in production
  - [ ] `SECRET_KEY` is not "INSECURE-CHANGE-ME-IN-PRODUCTION"
  - [ ] `API_PASSWORD` is not "admin"
  - [ ] Database passwords are not defaults
- [ ] `ALLOWED_ORIGINS` includes only trusted domains
- [ ] `API_BASE_URL` points to correct backend
- [ ] Credentials match between frontend and backend
- [ ] All secrets are stored securely (not in git)

---

## Troubleshooting

### "Invalid credentials" error

**Cause**: Password mismatch between frontend and backend

**Fix**:
```bash
# Verify passwords match
# Railway:
railway variables get API_PASSWORD

# Streamlit Cloud:
# Check secrets in app settings
```

### "CORS error" in browser

**Cause**: Frontend URL not in `ALLOWED_ORIGINS`

**Fix**:
```bash
# Railway:
railway variables set ALLOWED_ORIGINS=https://your-app.streamlit.app,http://localhost:8501
```

### "Database connection failed"

**Cause**: `DATABASE_URL` not set or incorrect

**Fix**:
```bash
# Railway auto-sets this when PostgreSQL addon is added
# If missing, add PostgreSQL database to your project
```

### "SECRET_KEY" warning on startup

**Cause**: Using default insecure key

**Fix**:
```bash
# Generate new key
python scripts/generate_secrets.py

# Set in Railway
railway variables set SECRET_KEY=your-new-key
```

---

## Reference

### Complete Variable List

| Variable | Railway | Streamlit | Local | Required |
|----------|---------|-----------|-------|----------|
| `SECRET_KEY` | ✓ | ✗ | ✓ | Yes |
| `API_USERNAME` | ✓ | ✓ | ✓ | Yes |
| `API_PASSWORD` | ✓ | ✓ | ✓ | Yes |
| `API_BASE_URL` | ✗ | ✓ | ✓ | Yes (frontend) |
| `DATABASE_URL` | Auto | ✗ | ✓ | Yes (backend) |
| `REDIS_HOST` | Auto | ✗ | ✓ | Yes (backend) |
| `REDIS_PORT` | Auto | ✗ | ✓ | Yes (backend) |
| `REDIS_PASSWORD` | Auto | ✗ | ✓ | Yes (backend) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | ✓ | ✗ | ✓ | No |
| `MAX_BATCH_SIZE` | ✓ | ✗ | ✓ | No |
| `ALLOWED_ORIGINS` | ✓ | ✗ | ✓ | Yes (backend) |
| `ENABLE_MONITORING` | ✓ | ✗ | ✓ | No |
| `LOG_LEVEL` | ✓ | ✗ | ✓ | No |
| `API_HOST` | ✗ | ✗ | ✓ | No |
| `API_PORT` | ✗ | ✗ | ✓ | No |

---

**Remember**: Never commit secrets to version control! Use `scripts/generate_secrets.py` to create secure values for production.
