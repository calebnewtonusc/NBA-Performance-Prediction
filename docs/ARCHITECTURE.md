# NBA Performance Prediction - System Architecture

## 📋 Overview

The NBA Performance Prediction system is a full-stack machine learning application that predicts NBA game outcomes and player statistics using enterprise-grade infrastructure.

---

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         END USERS                                │
│                    (Web Browsers, Mobile)                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     VERCEL CDN (Frontend)                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │            Next.js 14 Application                          │  │
│  │  • React Components (TypeScript)                           │  │
│  │  • Error Boundaries                                        │  │
│  │  • Client-side Validation                                  │  │
│  │  • Tailwind CSS Styling                                    │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ REST API (HTTPS)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RAILWAY (Backend API)                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              FastAPI Application                           │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  Authentication Layer                                 │  │  │
│  │  │  • JWT Tokens                                         │  │  │
│  │  │  • Bcrypt Password Hashing                            │  │  │
│  │  │  • Request ID Tracking                                │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  Rate Limiting                                        │  │  │
│  │  │  • SlowAPI (100 req/min)                              │  │  │
│  │  │  • IP-based throttling                                │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  Prediction Endpoints                                 │  │  │
│  │  │  • POST /api/predict (game outcomes)                  │  │  │
│  │  │  • POST /api/predict/simple (auto-fetch stats)        │  │  │
│  │  │  • POST /api/predict/player (player stats)            │  │  │
│  │  │  • POST /api/predict/compare (multi-model)            │  │  │
│  │  │  • POST /api/predict/batch (bulk predictions)         │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  Model Management                                     │  │  │
│  │  │  • GET /api/models (list all)                         │  │  │
│  │  │  • GET /api/models/{name}/{version}                   │  │  │
│  │  │  • POST /api/models/{name}/{version}/load             │  │  │
│  │  │  • DELETE /api/models/{name}/{version}/unload         │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  Monitoring & Health                                  │  │  │
│  │  │  • GET /api/health                                    │  │  │
│  │  │  • GET /api/metrics (Prometheus-compatible)           │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────┬──────────────┬───────────────┬──────────────────────┘
            │              │               │
            ▼              ▼               ▼
┌────────────────┐ ┌──────────────┐ ┌──────────────────┐
│  PostgreSQL    │ │    Redis     │ │   External APIs  │
│   Database     │ │    Cache     │ │   (nba_api)      │
│                │ │              │ │                  │
│ • Predictions  │ │ • Prediction │ │ • Live Stats     │
│ • User Data    │ │   Cache      │ │ • Team Info      │
│ • Audit Logs   │ │ • Features   │ │ • Schedule Data  │
│ • Metadata     │ │ • Rate Limit │ │                  │
└────────────────┘ └──────────────┘ └──────────────────┘
```

---

## 🧠 ML Model Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   ML MODEL LAYER                         │
│                                                          │
│  Game Prediction Models (Classification)                │
│  ┌───────────────────────────────────────────────────┐  │
│  │ 1. Logistic Regression (69.6% accuracy)          │  │
│  │ 2. Decision Tree (61.6% accuracy)                │  │
│  │ 3. Random Forest (67.3% accuracy)                │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  Player Stats Models (Regression)                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │ 1. Linear Regression (MAE ~2.49)                 │  │
│  │ 2. Ridge Regression (MAE ~2.49) ⭐ Default        │  │
│  │ 3. Lasso Regression (MAE ~2.49)                  │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  Feature Engineering Pipeline (40x Optimized)           │
│  ┌───────────────────────────────────────────────────┐  │
│  │ • Rolling averages (vectorized pandas)           │  │
│  │ • Win/loss streaks                               │  │
│  │ • Head-to-head history                           │  │
│  │ • Home/away splits                               │  │
│  │ • Rest days & back-to-back detection             │  │
│  │ • Point differential trends                      │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Model Storage Structure

```
models/
├── game_logistic/
│   └── v1/
│       ├── model.pkl          # Trained scikit-learn model
│       ├── scaler.pkl         # StandardScaler for features
│       └── metadata.json      # Training metrics, date, params
├── game_forest/
│   └── v1/
│       ├── model.pkl
│       ├── scaler.pkl
│       └── metadata.json
├── player_ridge/              # Default for player predictions
│   └── v1/
│       ├── model.pkl
│       ├── scaler.pkl
│       └── metadata.json
└── ...
```

---

## 🔄 Data Flow

### 1. Game Prediction Flow

```
User Request (BOS vs LAL)
    │
    ▼
Frontend Validation
    │
    ▼
API: POST /api/predict/simple
    │
    ├──> [Check Redis Cache] ──> Cache Hit? ──> Return Cached Result
    │                                 │
    │                                 ▼ No
    ├──> NBA Data Fetcher
    │      │
    │      ├──> Fetch BOS Stats (nba_api or fallback)
    │      └──> Fetch LAL Stats (nba_api or fallback)
    │
    ▼
Feature Engineering
    │
    ├──> Calculate rolling averages
    ├──> Compute point differentials
    ├──> Determine home court advantage
    └──> Build feature vector (18 features)
    │
    ▼
Model Manager
    │
    ├──> Load model (if not already loaded)
    ├──> Apply StandardScaler
    └──> Generate prediction
    │
    ▼
Response Formatting
    │
    ├──> Winner (home/away)
    ├──> Confidence (0-1)
    ├──> Probabilities
    └──> Metadata (model used, timestamp)
    │
    ▼
[Cache Result in Redis] (5 min TTL)
    │
    ▼
Return JSON to Frontend
```

### 2. Player Prediction Flow

```
User Request (Player Stats)
    │
    ▼
API: POST /api/predict/player
    │
    ├──> Validate input features
    │      • player_avg_points
    │      • player_avg_rebounds
    │      • player_avg_assists
    │      • team_win_pct
    │      • opponent_def_rating
    │      • is_home, rest_days, etc.
    │
    ▼
Load Player Ridge Model
    │
    ├──> Apply StandardScaler
    └──> Predict points
    │
    ▼
Calculate Confidence Interval
    │
    └──> ±15% margin (future: use prediction intervals)
    │
    ▼
Return Prediction + Intervals
```

---

## 🔐 Security Architecture

### Authentication Flow (JWT)

```
1. Login Request
   POST /api/auth/login
   {
     "username": "admin",
     "password": "secure_password"
   }
   │
   ▼
2. Password Verification
   • Bcrypt hash comparison (secure)
   • Fallback to plain text (deprecated, warns)
   │
   ▼
3. Generate JWT Token
   • Payload: {"sub": "admin", "exp": <timestamp>}
   • Algorithm: HS256
   • Secret: SECRET_KEY env var
   │
   ▼
4. Return Token
   {
     "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
     "token_type": "bearer"
   }
   │
   ▼
5. Subsequent Requests
   Headers: {
     "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
   }
   │
   ▼
6. Token Verification
   • Decode JWT
   • Verify signature
   • Check expiration
   • Extract user info
```

### Security Layers

1. **Transport Security**: HTTPS (TLS 1.2+)
2. **Authentication**: JWT tokens (HS256)
3. **Password Storage**: Bcrypt hashing (cost factor 12)
4. **Rate Limiting**: 100 requests/minute per IP
5. **Input Validation**: Pydantic schemas
6. **CORS**: Restricted to approved domains
7. **SQL Injection Prevention**: SQLAlchemy ORM
8. **Request Tracing**: Unique request IDs

---

## 💾 Database Schema

```sql
-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- Predictions Table
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    prediction_type VARCHAR(20) NOT NULL,  -- 'game' or 'player'
    model_name VARCHAR(50) NOT NULL,
    home_team VARCHAR(3),
    away_team VARCHAR(3),
    prediction VARCHAR(10),
    confidence FLOAT,
    features JSONB,                        -- Input features
    result JSONB,                          -- Prediction result
    created_at TIMESTAMP DEFAULT NOW(),
    request_id UUID
);

-- Model Metadata Table
CREATE TABLE model_metadata (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(50) NOT NULL,
    version VARCHAR(20) NOT NULL,
    model_type VARCHAR(50),
    accuracy FLOAT,
    metrics JSONB,
    trained_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(model_name, version)
);

-- Audit Logs
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(50) NOT NULL,
    resource VARCHAR(100),
    details JSONB,
    ip_address INET,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 📊 Monitoring & Observability

### Metrics Collected

```python
{
    "models_loaded": 6,
    "uptime_seconds": 123456,
    "predictions_total": 10543,
    "cache_hits": 3245,
    "cache_misses": 7298,
    "cache_hit_rate": 0.308,
    "errors_total": 12,
    "cache_type": "redis",
    "cache_total_keys": 450
}
```

### Logging Strategy

```
logs/
├── nba_api.log              # All logs (rotates at 10MB)
├── nba_api_errors.log       # Errors only (rotates at 10MB)
├── nba_api_daily.log        # Daily rotation (keeps 30 days)
└── archived/                # Old logs
    ├── nba_api.log.1
    ├── nba_api.log.2
    └── ...
```

### Alert Triggers

1. Error rate > 5% for 2 minutes
2. Response time P95 > 1000ms for 5 minutes
3. Health check fails for 1 minute
4. Database connection pool exhausted
5. Redis connection failure
6. Model loading failures

---

## 🚀 Deployment Pipeline (CI/CD)

```
Developer Push to GitHub
    │
    ▼
GitHub Actions Triggered
    │
    ├──> Run Tests (Ubuntu, macOS, Windows)
    │      ├─ pytest (90%+ coverage)
    │      ├─ flake8 (code quality)
    │      ├─ black (formatting)
    │      └─ bandit (security scan)
    │
    ├──> Build Docker Image
    │      └─ Multi-stage build (python:3.11-slim)
    │
    ▼
Tests Pass?
    │
    ├─ NO ──> ❌ Deployment Blocked
    │
    ▼ YES
    │
    ├──> Railway (Backend)
    │      ├─ Pull latest code
    │      ├─ Build image
    │      ├─ Run migrations
    │      ├─ Deploy (zero-downtime)
    │      └─ Health check
    │
    └──> Vercel (Frontend)
           ├─ Build Next.js app
           ├─ Deploy to CDN
           └─ Update DNS
    │
    ▼
Production Deployment Complete ✅
    │
    └──> Post-Deployment
           ├─ Smoke tests
           ├─ Monitor metrics
           └─ Alert on-call if issues
```

---

## 🔧 Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.9-3.12
- **ML Libraries**: scikit-learn 1.3+, pandas 2.0+, numpy 1.24+
- **Database**: PostgreSQL 15+ (SQLAlchemy ORM)
- **Cache**: Redis 5.0+ (with hiredis)
- **Auth**: python-jose (JWT), passlib (bcrypt)
- **Validation**: Pydantic 2.0+
- **Rate Limiting**: SlowAPI
- **Server**: Uvicorn (ASGI)
- **Testing**: pytest, pytest-cov

### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Charts**: Recharts
- **Icons**: Lucide React

### Infrastructure
- **Hosting**: Railway (backend), Vercel (frontend)
- **CDN**: Vercel Edge Network
- **Database**: Railway Postgres
- **Cache**: Railway Redis
- **Monitoring**: Prometheus, Grafana (planned)
- **CI/CD**: GitHub Actions

---

## 📈 Performance Characteristics

### API Response Times (P95)
- Health check: <50ms
- Cached prediction: <100ms
- Uncached prediction: <500ms
- Batch prediction (10 games): <1000ms
- Model loading (first request): <2000ms

### Throughput
- Max requests/second: ~100 (rate limited)
- Concurrent users supported: ~500
- Cache hit rate: ~30-40%

### Resource Usage
- API memory: ~512MB (idle), ~1GB (under load)
- Model memory: ~200MB total (all 6 models)
- Database connections: Pool of 10-20

---

## 🔄 Future Enhancements

### Planned Architecture Improvements

1. **Microservices Split**
   ```
   Current: Monolithic API
   Future:
     ├─ Prediction Service
     ├─ Data Ingestion Service
     ├─ Model Training Service
     └─ Analytics Service
   ```

2. **Advanced Caching**
   - Cache warming (pre-compute popular matchups)
   - Intelligent TTL (longer for stable teams)
   - Multi-tier caching (memory + Redis)

3. **Scalability**
   - Kubernetes deployment (auto-scaling)
   - Load balancer (multiple API instances)
   - Read replicas (database scaling)

4. **Observability**
   - Distributed tracing (Jaeger)
   - APM (Datadog/New Relic)
   - Real-time dashboards

5. **ML Improvements**
   - Online learning (auto-retrain)
   - Ensemble methods (combine all models)
   - Deep learning models (neural networks)
   - Real-time feature updates

---

## 📞 Support & Maintenance

- **Documentation**: `/docs` directory
- **API Docs**: https://[api-url]/api/docs
- **Health Check**: https://[api-url]/api/health
- **Metrics**: https://[api-url]/api/metrics (auth required)

**Maintained by**: Caleb Newton (https://calebnewton.me)
