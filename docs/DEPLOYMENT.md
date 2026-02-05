# Deployment Guide

Complete guide to deploying the NBA Performance Prediction system to production using GitHub → Railway (backend) + Streamlit Cloud (frontend).

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step 1: Push to GitHub](#step-1-push-to-github)
4. [Step 2: Deploy Backend to Railway](#step-2-deploy-backend-to-railway)
5. [Step 3: Deploy Frontend to Streamlit Cloud](#step-3-deploy-frontend-to-streamlit-cloud)
6. [Step 4: Verification](#step-4-verification)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)
8. [Troubleshooting](#troubleshooting)
9. [Cost Estimates](#cost-estimates)

---

## Overview

The deployment architecture consists of:

- **Frontend**: Streamlit dashboard deployed to **Streamlit Cloud** (free tier)
- **Backend**: FastAPI + PostgreSQL + Redis deployed to **Railway** ($15-20/month)
- **CI/CD**: GitHub Actions for automated testing and deployment

### Architecture Diagram

```
GitHub Repository
    │
    ├── Push to main → Railway deploys backend automatically
    │   └── FastAPI + PostgreSQL + Redis
    │       └── Health checks, auto-restart on failure
    │
    └── Connected to Streamlit Cloud → Frontend deployment
        └── Streamlit Dashboard
            └── Calls Railway API via HTTPS
```

---

## Prerequisites

### Accounts Required

1. **GitHub Account** (free)
   - Create at https://github.com/signup

2. **Railway Account** (free trial, then $5-15/month)
   - Sign up at https://railway.app
   - Link GitHub account

3. **Streamlit Cloud Account** (free tier available)
   - Sign up at https://streamlit.io/cloud
   - Link GitHub account

### Local Setup

Ensure you have the following installed:
- Git
- Python 3.9+
- Docker (optional, for local testing)

---

## Step 1: Push to GitHub

### 1.1 Generate Secure Secrets

Run the secrets generator:

```bash
python scripts/generate_secrets.py
```

Save the output securely (use a password manager). You'll need these for Railway and Streamlit Cloud.

### 1.2 Verify .gitignore

Ensure sensitive files are excluded:

```bash
# Check .gitignore includes:
.env
*.log
.streamlit/secrets.toml
__pycache__/
```

### 1.3 Create GitHub Repository

Option A: Via GitHub CLI
```bash
gh repo create nba-performance-prediction --public --source=. --remote=origin
```

Option B: Via GitHub Web UI
1. Go to https://github.com/new
2. Repository name: `nba-performance-prediction`
3. Public or Private (your choice)
4. Don't initialize with README (already exists)
5. Create repository

### 1.4 Push Code

```bash
# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: NBA Performance Prediction system

- FastAPI REST API with JWT auth
- PostgreSQL + Redis infrastructure
- Streamlit dashboard
- Docker Compose setup
- Railway + Streamlit Cloud deployment configs

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/nba-performance-prediction.git
git branch -M main
git push -u origin main
```

### 1.5 Verify GitHub Actions

After pushing, check that GitHub Actions workflows are triggered:

1. Go to your repository on GitHub
2. Click "Actions" tab
3. You should see workflows running (or waiting for first PR)

---

## Step 2: Deploy Backend to Railway

### 2.1 Create Railway Project

1. Go to https://railway.app/dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `nba-performance-prediction` repository
5. Railway will detect the `Dockerfile.api` and `railway.json`

### 2.2 Add PostgreSQL Database

1. In your Railway project, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically provision a database and set `DATABASE_URL`

### 2.3 Add Redis Cache

1. Click "+ New" again
2. Select "Database" → "Redis"
3. Railway will automatically set Redis connection variables

### 2.4 Configure Environment Variables

In your Railway project, go to your web service → Variables tab:

```bash
# Required: Generate these with scripts/generate_secrets.py
SECRET_KEY=<your-generated-secret-key>
API_USERNAME=admin
API_PASSWORD=<your-generated-password>

# API Configuration
ACCESS_TOKEN_EXPIRE_MINUTES=30
MAX_BATCH_SIZE=100
ENABLE_MONITORING=true
LOG_LEVEL=INFO

# CORS - Update after deploying Streamlit
ALLOWED_ORIGINS=https://your-streamlit-app.streamlit.app,http://localhost:8501

# Database and Redis are auto-configured by Railway
# DATABASE_URL (auto-set by PostgreSQL addon)
# REDIS_HOST (auto-set by Redis addon)
# REDIS_PORT (auto-set by Redis addon)
# REDIS_PASSWORD (auto-set by Redis addon)
```

### 2.5 Deploy

1. Railway will automatically deploy after configuration
2. Wait for build to complete (2-5 minutes)
3. Check logs for any errors
4. Note your Railway app URL (e.g., `https://nba-api-production.up.railway.app`)

### 2.6 Verify Backend Deployment

```bash
# Test health endpoint
curl https://your-app.up.railway.app/api/health

# Should return:
# {
#   "status": "healthy",
#   "timestamp": "...",
#   "models_loaded": 1,
#   "uptime_seconds": 123
# }
```

Or use the test script:

```bash
python scripts/test_api_connection.py --url https://your-app.up.railway.app --password YOUR_PASSWORD
```

---

## Step 3: Deploy Frontend to Streamlit Cloud

### 3.1 Connect to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Connect your GitHub account if not already connected
4. Select your repository: `nba-performance-prediction`

### 3.2 Configure App Settings

- **Main file path**: `src/visualization/dashboard.py`
- **Python version**: `3.11`
- **Branch**: `main`

### 3.3 Add Secrets

In Streamlit Cloud App Settings → Secrets, add:

```toml
API_BASE_URL = "https://your-railway-app.up.railway.app"
API_USERNAME = "admin"
API_PASSWORD = "your-generated-password"
```

**Important**: Use the SAME password you set in Railway!

### 3.4 Deploy

1. Click "Deploy"
2. Wait for deployment (2-3 minutes)
3. Your app will be available at: `https://your-app.streamlit.app`

### 3.5 Update CORS in Railway

Now that you have your Streamlit URL, update Railway environment variables:

1. Go to Railway project → Web service → Variables
2. Update `ALLOWED_ORIGINS`:
   ```
   ALLOWED_ORIGINS=https://your-app.streamlit.app,http://localhost:8501
   ```
3. Railway will automatically redeploy

---

## Step 4: Verification

### 4.1 Test Backend

```bash
# Health check
curl https://your-railway-app.up.railway.app/api/health

# Login
curl -X POST https://your-railway-app.up.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'

# API Documentation
open https://your-railway-app.up.railway.app/api/docs
```

### 4.2 Test Frontend

1. Open your Streamlit Cloud URL
2. Navigate to "Game Predictions" page
3. Enter prediction parameters
4. Click "Predict Winner"
5. Verify prediction appears

### 4.3 Test End-to-End Connection

The dashboard will make API calls to Railway. Check:

1. Streamlit Cloud logs for any connection errors
2. Railway logs for incoming requests
3. No CORS errors in browser console (F12)

### 4.4 Run Full Test Suite

```bash
python scripts/test_api_connection.py --url https://your-railway-app.up.railway.app --password YOUR_PASSWORD
```

All tests should pass:
- ✅ Health check
- ✅ Login
- ✅ Models endpoint
- ✅ Prediction endpoint
- ✅ Metrics endpoint

---

## Monitoring and Maintenance

### Railway Monitoring

1. **Logs**: Railway Dashboard → Your service → Logs
2. **Metrics**: View CPU, memory, and request metrics
3. **Health Checks**: Automatic via `/api/health` endpoint

### Streamlit Cloud Monitoring

1. **Logs**: Streamlit Cloud → Your app → Logs
2. **Usage**: View app access statistics
3. **Performance**: Monitor response times

### Prometheus Metrics

Access Prometheus metrics for detailed monitoring:

```bash
curl https://your-railway-app.up.railway.app/api/metrics
```

Metrics include:
- `predictions_total` - Total predictions made
- `errors_total` - Total errors
- `models_loaded` - Number of models loaded
- `uptime_seconds` - API uptime

### Database Backups

Railway automatically backs up PostgreSQL:
1. Go to Railway → PostgreSQL service → Backups
2. Download backups or restore from snapshot
3. Recommended: Enable daily backups

---

## Troubleshooting

### Backend Issues

**Problem**: Health check failing

```bash
# Check logs
railway logs

# Common causes:
# 1. Missing environment variables
# 2. Database connection failed
# 3. Model files not found
# 4. Port binding issues
```

**Problem**: Authentication errors

```bash
# Verify environment variables
echo $SECRET_KEY  # Should not be "INSECURE-CHANGE-ME-IN-PRODUCTION"
echo $API_PASSWORD  # Should not be "admin"

# Test login
curl -X POST https://your-app.up.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'
```

**Problem**: Database connection errors

```bash
# Railway sets DATABASE_URL automatically
# Verify it's set:
railway variables

# Format should be:
# postgresql://user:password@host:port/database
```

### Frontend Issues

**Problem**: CORS errors in browser console

```
Access to fetch at 'https://...' from origin 'https://...' has been blocked by CORS policy
```

**Fix**: Update `ALLOWED_ORIGINS` in Railway to include your Streamlit Cloud URL

```bash
# In Railway environment variables:
ALLOWED_ORIGINS=https://your-app.streamlit.app,http://localhost:8501
```

**Problem**: API connection failed

Check Streamlit Cloud secrets:
1. Go to App Settings → Secrets
2. Verify `API_BASE_URL` matches your Railway URL
3. Verify `API_PASSWORD` matches Railway password
4. Redeploy app after updating secrets

**Problem**: Module import errors

```bash
# Ensure requirements-streamlit.txt includes all dependencies
# Check Streamlit Cloud logs for missing packages
# Add missing packages to requirements-streamlit.txt and push to GitHub
```

### GitHub Actions Issues

**Problem**: Workflows not triggering

1. Check `.github/workflows/*.yml` files exist
2. Verify GitHub Actions is enabled in repository settings
3. Check workflow trigger conditions (branches, paths)

**Problem**: Tests failing

```bash
# Run tests locally first
python -c "from src.api.main import app; print('OK')"
python -c "from src.models.model_manager import ModelManager; print('OK')"

# Fix import errors, then push to GitHub
```

---

## Cost Estimates

### Railway (Backend)

| Component | Plan | Cost |
|-----------|------|------|
| Web Service (FastAPI) | Starter | $5/month |
| PostgreSQL | 1GB | $5/month |
| Redis | 256MB | $5/month |
| **Total** | | **$15/month** |

**Note**: Railway offers $5 free credit per month, reducing cost to $10/month.

### Streamlit Cloud (Frontend)

| Tier | Features | Cost |
|------|----------|------|
| Community | Public apps, 1GB RAM | **FREE** |
| Team | Private apps, more resources | $20/user/month |

**Recommended**: Use Community tier (FREE) for this project.

### GitHub

- **Public repos**: Free
- **GitHub Actions**: 2000 minutes/month free (sufficient)

### Total Monthly Cost

- **With free tiers**: $10-15/month
- **Without free tiers**: $15/month
- **Enterprise (Team tier)**: $35/month

---

## Next Steps

After successful deployment:

1. **Custom Domain** (optional)
   - Add custom domain in Railway settings
   - Update CORS configuration

2. **Monitoring** (optional)
   - Set up error tracking (Sentry, LogRocket)
   - Configure alerting (email, Slack)

3. **Scaling**
   - Increase Railway plan for more resources
   - Enable auto-scaling if needed

4. **Security Hardening**
   - Rotate secrets periodically
   - Enable rate limiting per user
   - Add IP whitelisting if needed

5. **Database Optimization**
   - Index frequently queried columns
   - Set up read replicas if needed
   - Configure connection pooling

---

## Support

- **Railway Docs**: https://docs.railway.app
- **Streamlit Docs**: https://docs.streamlit.io
- **Project Issues**: https://github.com/YOUR_USERNAME/nba-performance-prediction/issues

---

## Rollback Procedure

If deployment fails or issues occur:

### Backend (Railway)

1. Go to Railway → Your service → Deployments
2. Find previous successful deployment
3. Click "Redeploy" on that version
4. Or: Revert git commit and push to trigger new deployment

### Frontend (Streamlit Cloud)

1. Revert changes in GitHub repository
2. Streamlit Cloud auto-deploys from main branch
3. Or: Use "Reboot app" in Streamlit Cloud settings

### Database (Railway)

1. Go to PostgreSQL service → Backups
2. Select backup snapshot
3. Restore from snapshot
4. Note: This will lose data since backup

---

**Deployment Complete! 🎉**

Your NBA Performance Prediction system is now live:
- **Dashboard**: https://your-app.streamlit.app
- **API**: https://your-railway-app.up.railway.app
- **API Docs**: https://your-railway-app.up.railway.app/api/docs
