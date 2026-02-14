# wrench.fill NBA Prediction API - Troubleshooting Guide

## Quick Diagnosis

```bash
# Check API health
curl https://your-api-url.com/api/health

# Check if models are loaded
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://your-api-url.com/api/models

# Check metrics
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://your-api-url.com/api/metrics
```

---

## Common Issues & Solutions

### 1. Cannot Login / 401 Unauthorized

#### Symptoms
```json
{
  "detail": "Incorrect username or password"
}
```

#### Causes & Solutions

**Cause 1: Wrong credentials**
```bash
# Check your .env file
cat .env | grep API_

# Expected:
API_USERNAME=your_username
API_PASSWORD_HASH=$2b$12$...
```

**Cause 2: Using plain password instead of hash**
```bash
# Generate proper hash
python3 -c "from passlib.context import CryptContext; pwd_context = CryptContext(schemes=['bcrypt']); print(pwd_context.hash('your_password'))"

# Add to .env:
API_PASSWORD_HASH=$2b$12$... (copy hash from above)
```

**Cause 3: Token expired**
```bash
# Default expiry is 30 minutes
# Request a new token:
curl -X POST https://your-api-url.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'
```

---

### 2. Prediction Request Fails / 500 Internal Server Error

#### Symptoms
```json
{
  "detail": "Internal server error",
  "error": "..."
}
```

#### Diagnosis Steps

1. **Check API logs**:
   ```bash
   # Railway
   railway logs

   # Docker
   docker logs nba-api --tail 100

   # Local
   tail -f logs/nba_api_errors.log
   ```

2. **Verify model is loaded**:
   ```bash
   curl -H "Authorization: Bearer TOKEN" \
     https://your-api-url.com/api/models/game_logistic/v1
   ```

3. **Check request payload**:
   ```bash
   # Invalid team name?
   curl -X POST https://your-api-url.com/api/predict/simple \
     -H "Authorization: Bearer TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"home_team":"INVALID","away_team":"LAL"}'

   # Error: "Invalid team abbreviation 'INVALID'. Valid teams: ATL, BOS, ..."
   ```

#### Common Causes

**Cause 1: Model not found**
```bash
# List available models
ls models/

# Expected:
game_logistic/
game_forest/
game_tree/
player_ridge/
player_linear/
player_lasso/

# Fix: Train missing model or use available one
```

**Cause 2: Invalid input features**
```json
{
  "detail": [
    {
      "loc": ["body", "features", "home_win_pct"],
      "msg": "ensure this value is less than or equal to 1.0",
      "type": "value_error.number.not_le"
    }
  ]
}
```
Fix: Ensure `home_win_pct` is between 0.0 and 1.0

**Cause 3: Missing numpy import** (Fixed in latest version)
```bash
# Update to latest code
git pull origin main
```

---

### 3. Redis Cache Not Working

#### Symptoms
- `cache_hits` always 0 in `/api/metrics`
- Warnings: "Redis not available, falling back to in-memory cache"

#### Diagnosis
```bash
# Check if Redis is running
redis-cli ping
# Expected: PONG

# Check connection
redis-cli -h your-redis-host -p 6379 ping
```

#### Solutions

**Solution 1: Start Redis**
```bash
# Local (macOS)
brew services start redis

# Local (Linux)
sudo systemctl start redis

# Docker
docker run -d --name redis -p 6379:6379 redis:latest
```

**Solution 2: Update environment variables**
```bash
# .env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=  # leave empty if no password
```

**Solution 3: Check Railway/production Redis**
```bash
# Railway: Check Redis addon in dashboard
# Ensure DATABASE_URL is set correctly
```

---

### 4. Database Connection Errors

#### Symptoms
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server
```

#### Diagnosis
```bash
# Test database connection
psql "postgresql://user:pass@host:5432/dbname"

# Check environment variable
echo $DATABASE_URL
```

#### Solutions

**Solution 1: Database not running**
```bash
# Local PostgreSQL
brew services start postgresql
# or
sudo systemctl start postgresql
```

**Solution 2: Wrong connection string**
```bash
# .env
DATABASE_URL=postgresql://user:password@localhost:5432/nba_predictions

# Railway: Copy from dashboard
```

**Solution 3: Connection pool exhausted**
```python
# Check pool status in logs
# Increase pool size in .env:
DB_POOL_SIZE=20
DB_POOL_MAX_OVERFLOW=30
```

---

### 5. HTTPS Redirect Loop

#### Symptoms
- Browser shows "ERR_TOO_MANY_REDIRECTS"
- Infinite redirect between HTTP/HTTPS

#### Cause
HTTPS enforcement middleware conflicting with reverse proxy

#### Solution
```python
# Check if Railway/Vercel sets X-Forwarded-Proto correctly
# Middleware checks this header

# Disable HTTPS enforcement in development:
# Remove or comment out RAILWAY_ENVIRONMENT check
```

---

### 6. Slow Prediction Response (>2 seconds)

#### Diagnosis
```bash
# Check model loading time
curl -w "@curl-format.txt" -o /dev/null -s \
  -X POST https://your-api-url.com/api/predict/simple \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"home_team":"BOS","away_team":"LAL"}'

# curl-format.txt:
time_namelookup:  %{time_namelookup}\n
time_connect:  %{time_connect}\n
time_starttransfer:  %{time_starttransfer}\n
time_total:  %{time_total}\n
```

#### Solutions

**Solution 1: Models not preloaded**
```python
# Check startup logs:
shippingbox.fill Preloading ML models...
  checkmark Loaded game_logistic:v1
  checkmark Loaded game_forest:v1
  checkmark Loaded player_ridge:v1
checkmark.circle.fill Preloaded 3/3 models

# If not loading, check startup_event() function
```

**Solution 2: NBA API timeout**
```python
# Increase timeout in nba_data_fetcher.py
timeout = 10  # seconds
```

**Solution 3: Database slow**
```bash
# Check database performance
EXPLAIN ANALYZE SELECT * FROM predictions WHERE user_id = 1 LIMIT 10;

# Add indexes if missing
CREATE INDEX idx_predictions_user_id ON predictions(user_id);
```

---

### 7. Frontend Shows "Failed to connect to API"

#### Symptoms
- Red error message on homepage
- Console error: "Network Error" or "CORS policy"

#### Diagnosis
```bash
# Check CORS configuration in backend
# Check if frontend URL is allowed

# Browser console (F12):
fetch('https://your-api-url.com/api/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

#### Solutions

**Solution 1: CORS not configured**
```python
# src/api/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"(https://your-frontend-url\.vercel\.app|http://localhost:[0-9]+)",
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

**Solution 2: API URL wrong**
```typescript
// frontend/lib/api-client.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://your-api-url.com'
```

**Solution 3: API down**
```bash
# Check API health
curl https://your-api-url.com/api/health

# Check Railway deployment
railway status
```

---

### 8. Rate Limit Exceeded (429 Error)

#### Symptoms
```json
{
  "error": "Rate limit exceeded: 100 per 1 minute"
}
```

#### Solutions

**Solution 1: Wait 1 minute**
```bash
# Rate limit resets after time window
# Default: 100 requests per minute
```

**Solution 2: Increase rate limit**
```python
# src/api/main.py
@app.post("/api/predict")
@limiter.limit("200/minute")  # Increase from 100
async def predict_game(...):
```

**Solution 3: Use batch endpoint**
```bash
# Instead of 10 individual requests, use batch:
curl -X POST https://your-api-url.com/api/predict/batch \
  -H "Authorization: Bearer TOKEN" \
  -d '{"games":[...]}'
```

---

### 9. Model Not Found / 404 Error

#### Symptoms
```json
{
  "detail": "Model game_logistic:v1 not found"
}
```

#### Solutions

**Solution 1: Check model files exist**
```bash
ls -la models/game_logistic/v1/
# Expected:
model.pkl
scaler.pkl
metadata.json
```

**Solution 2: Retrain model**
```bash
python scripts/train_models.py
```

**Solution 3: Use correct model name**
```bash
# List available models
curl -H "Authorization: Bearer TOKEN" \
  https://your-api-url.com/api/models

# Use exact name from response
```

---

### 10. Memory Error / Out of Memory

#### Symptoms
```
MemoryError: Unable to allocate array
```
or
```
Killed (OOM)
```

#### Solutions

**Solution 1: Reduce batch size**
```python
# .env
MAX_BATCH_SIZE=50  # Reduce from 100
```

**Solution 2: Increase Railway memory**
```bash
# Railway dashboard:
# Settings > Resources > Increase memory limit
```

**Solution 3: Clear cache**
```bash
# Clear Redis cache
redis-cli FLUSHDB

# Or restart API
railway up --detach
```

---

## Debugging Tools

### Enable Debug Logging
```bash
# .env
LOG_LEVEL=DEBUG
SQL_ECHO=true  # Show all SQL queries
```

### Check Request ID
```bash
# Every request has unique ID
curl -v https://your-api-url.com/api/health 2>&1 | grep X-Request-ID

# Use ID to find logs:
grep "abc-123-def" logs/nba_api.log
```

### Inspect Database
```sql
-- Recent predictions
SELECT * FROM predictions ORDER BY created_at DESC LIMIT 10;

-- Failed predictions
SELECT * FROM audit_logs WHERE success = false ORDER BY created_at DESC;

-- Most used models
SELECT model_name, COUNT(*) as usage_count
FROM predictions
GROUP BY model_name
ORDER BY usage_count DESC;
```

### Monitor Performance
```python
# Add timing decorator
import time
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end-start:.2f}s")
        return result
    return wrapper
```

---

## Getting Help

If you can't solve your issue:

1. **Check logs first**:
   ```bash
   # API logs
   tail -100 logs/nba_api_errors.log

   # Railway logs
   railway logs --tail 100
   ```

2. **Create GitHub issue** with:
   - Error message (full stack trace)
   - Steps to reproduce
   - Environment (Railway/local, Python version, etc.)
   - Request ID (from X-Request-ID header)

3. **Include diagnostics**:
   ```bash
   # System info
   python --version
   pip list | grep -E "(fastapi|sklearn|pandas)"

   # API health
   curl https://your-api-url.com/api/health | jq

   # Model status
   curl -H "Authorization: Bearer TOKEN" \
     https://your-api-url.com/api/models | jq
   ```

---

## Preventive Maintenance

### Weekly Checks
- [ ] Check disk space: `df -h`
- [ ] Check log sizes: `du -sh logs/`
- [ ] Review error logs: `tail -100 logs/nba_api_errors.log`
- [ ] Test critical endpoints
- [ ] Review metrics dashboard

### Monthly Checks
- [ ] Update dependencies: `pip list --outdated`
- [ ] Backup database: `pg_dump $DATABASE_URL > backup.sql`
- [ ] Review and archive old logs
- [ ] Load test API
- [ ] Check model accuracy (drift detection)

### Alerts to Set Up
- Error rate > 5%
- Response time P95 > 1000ms
- Database connection failures
- Redis connection failures
- Disk space < 10%

---

**Last Updated**: February 6, 2026
**Maintained by**: Caleb Newton
