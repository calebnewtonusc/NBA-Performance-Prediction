# Railway Deployment Checklist ✅

## Pre-Deployment Verification

### ✅ Files Confirmed in Repository
- [x] `Dockerfile.api` - Multi-stage Docker build
- [x] `railway.json` - Railway configuration
- [x] `requirements-api.txt` - API dependencies
- [x] `requirements-lock.txt` - Locked versions (scikit-learn==1.8.0)
- [x] All 6 model files (game_logistic, game_tree, game_forest, player_linear, player_ridge, player_lasso)
- [x] `data/raw/nba_games_real.csv` - NBA training data (276KB)

### 🔧 Railway Configuration Steps

#### 1. Create New Railway Service
1. Go to: https://railway.app/dashboard
2. Click: **"New Project"**
3. Select: **"Deploy from GitHub repo"**
4. Choose: `calebnewtonusc/NBA-Performance-Prediction`
5. Railway will auto-detect `railway.json` and use `Dockerfile.api`

#### 2. Configure Environment Variables

**CRITICAL:** Add these BEFORE clicking Deploy:

```bash
SECRET_KEY=zgPBku-uBe0BAGZQiX-TuI6hHIDbqOb6sBrtYNK3o6o
API_USERNAME=admin
API_PASSWORD=3vmPHdnH8RSfvqc-UCdy5A
ACCESS_TOKEN_EXPIRE_MINUTES=30
MAX_BATCH_SIZE=100
ALLOWED_ORIGINS=https://nba-performance-prediction.vercel.app,http://localhost:3000
LOG_LEVEL=INFO
```

**How to add:**
- Click **"Variables"** tab in Railway
- Click **"+ New Variable"** for each
- Copy/paste name and value
- Click **"Add"** for each

#### 3. Verify Build Settings (Auto-detected from railway.json)

These should be automatic:
- ✅ Builder: `DOCKERFILE`
- ✅ Dockerfile Path: `Dockerfile.api`
- ✅ Health Check: `/api/health`
- ✅ Port: Auto-assigned by Railway (uses `$PORT` env var)

**DO NOT CHANGE** these unless Railway fails to detect them.

#### 4. Deploy!

1. Click **"Deploy"**
2. Watch the build logs (should take 3-5 minutes)
3. Look for these success indicators:
   - ✅ `Building Dockerfile.api`
   - ✅ `COPY --chown=nbaapi:nbaapi models/ /app/models/`
   - ✅ `Successfully built`
   - ✅ `Health check passed`

---

## Common Deployment Errors & Fixes

### Error: "Trial plan limitation"
**Solution:** Upgrade to Railway Starter plan ($5/month)

### Error: "Build failed - requirements not found"
**Cause:** Wrong root directory
**Solution:** Root directory should be blank (project root), not `/src` or `/api`

### Error: "Model files not found"
**Cause:** `.gitignore` blocking models
**Solution:** Already fixed! Models are now in git (see commit 9beb330)

### Error: "Port binding failed"
**Cause:** App not listening on Railway's $PORT
**Solution:** Already fixed! Dockerfile uses `${PORT:-8000}`

### Error: "Health check failed"
**Cause:** App not responding at `/api/health`
**Solution:** Wait 30 seconds for startup, check logs for Python errors

---

## Post-Deployment Verification

### Step 1: Get Your Railway URL

After deployment completes, copy your Railway URL:
```
https://nba-performance-prediction-production.up.railway.app
```

(Replace with your actual URL from Railway dashboard)

### Step 2: Test Health Endpoint

```bash
curl https://YOUR-RAILWAY-URL.up.railway.app/api/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-05T...",
  "uptime_seconds": 45.2,
  "models_loaded": 0,
  "version": "1.0.0"
}
```

**Note:** `models_loaded: 0` is NORMAL! Models load on-demand.

### Step 3: Test API Documentation

Visit in browser:
```
https://YOUR-RAILWAY-URL.up.railway.app/api/docs
```

You should see the Swagger UI with all endpoints.

### Step 4: Test Authentication

```bash
curl -X POST "https://YOUR-RAILWAY-URL.up.railway.app/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=3vmPHdnH8RSfvqc-UCdy5A"
```

**Expected response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Step 5: Test Prediction (loads model on-demand)

Use the token from Step 4:

```bash
curl -X POST "https://YOUR-RAILWAY-URL.up.railway.app/api/predict/simple" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"home_team": "BOS", "away_team": "LAL", "model_type": "logistic"}'
```

**Expected response:**
```json
{
  "prediction": "home_win",
  "confidence": 0.698,
  "home_team": "BOS",
  "away_team": "LAL",
  "model_used": "game_logistic:v1"
}
```

After this, check `/api/health` again - `models_loaded` should now be `1`!

---

## Update Vercel After Railway Deploys

### Step 1: Update Vercel Environment Variable

1. Go to: https://vercel.com/dashboard
2. Select: `nba-performance-prediction` project
3. Click: **Settings** → **Environment Variables**
4. Find: `NEXT_PUBLIC_API_URL`
5. Update to: `https://YOUR-RAILWAY-URL.up.railway.app` (no trailing slash!)
6. Click: **Save**

### Step 2: Redeploy Vercel

1. Go to: **Deployments** tab
2. Click: **...** menu on latest deployment
3. Click: **Redeploy**
4. Wait ~2 minutes

### Step 3: Test Frontend

1. Visit: https://nba-performance-prediction.vercel.app
2. Navigate to "Game Predictions" page
3. Test: BOS vs LAL
4. Should see: ~69.8% confidence prediction!

---

## Troubleshooting Commands

### View Railway Logs
In Railway dashboard: **Deployments** → Click latest → **View Logs**

### Check Model Files in Container
```bash
# Railway CLI (install: npm i -g @railway/cli)
railway run ls -la /app/models/
```

### Check Python Version
```bash
railway run python --version
# Should show: Python 3.11.x
```

### Check scikit-learn Version
```bash
railway run python -c "import sklearn; print(sklearn.__version__)"
# Should show: 1.8.0
```

---

## Success Indicators ✅

- ✅ Health endpoint returns `{"status": "healthy"}`
- ✅ API docs accessible at `/api/docs`
- ✅ Authentication returns JWT token
- ✅ Prediction returns realistic confidence (~70%, not 99%)
- ✅ Models load on-demand (check logs for "Loading model")
- ✅ Frontend connects and shows predictions

---

## Need Help?

If deployment still fails:
1. **Check Railway logs** for specific error messages
2. **Verify environment variables** are set correctly
3. **Confirm GitHub integration** has proper permissions
4. **Try manual redeploy** from Railway dashboard
5. **Contact Railway Support** if trial plan limitation

---

## Credentials for Reference

**API Authentication:**
- Username: `admin`
- Password: `3vmPHdnH8RSfvqc-UCdy5A`

**Important:** Change these in production by updating Railway environment variables!

---

## Expected Deployment Timeline

- ⏱️ **Build:** 2-3 minutes (compiling dependencies)
- ⏱️ **Deploy:** 30-60 seconds (container startup)
- ⏱️ **Health Check:** 10-30 seconds (Railway verifies endpoint)
- ⏱️ **Total:** 3-5 minutes from "Deploy" click to live

---

## Post-Deployment Monitoring

Railway provides:
- **Metrics:** CPU, Memory, Network usage
- **Logs:** Real-time application logs
- **Health Checks:** Automatic monitoring of `/api/health`
- **Alerts:** Email notifications for failures

Check these in Railway dashboard → **Observability** tab

---

Good luck with deployment! 🚀
