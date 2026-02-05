# Fix CORS Error - Railway Configuration

## Problem
```
Access to XMLHttpRequest blocked by CORS policy
```

## Solution - Update Railway Environment Variable

### Step-by-Step:

1. Go to: https://railway.app/dashboard
2. Click "NBA-Performance-Prediction" project
3. Click the API service
4. Go to "Variables" tab
5. Add/Update `ALLOWED_ORIGINS` variable:

**Value:**
```
https://nba-performance-prediction.vercel.app,https://nba-performance-prediction-ps7k31hw0-calebs-projects-a6310ab2.vercel.app,http://localhost:3000,http://localhost:8000
```

6. Click "Add" - Railway will auto-redeploy (~2-3 min)
7. Test at: https://nba-performance-prediction.vercel.app

Done! ✅
