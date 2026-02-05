# Vercel Frontend Deployment Guide

## Option 1: Deploy via Vercel Dashboard (Recommended)

1. Go to https://vercel.com/dashboard
2. Click "Add New Project"
3. Import from GitHub: `calebnewtonusc/NBA-Performance-Prediction`
4. **Configure Project:**
   - **Root Directory:** `frontend`
   - **Framework Preset:** Next.js (auto-detected)
   - **Build Command:** `npm run build` (default)
   - **Output Directory:** `.next` (default)
   - **Install Command:** `npm install` (default)

5. **Add Environment Variable:**
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: `https://nba-performance-prediction-production.up.railway.app`

6. Click "Deploy"

## Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI globally
npm install -g vercel

# Navigate to project root
cd /Users/joelnewton/Desktop/2026-Code/projects/NBA-Performance-Prediction

# Deploy from frontend directory
vercel --cwd frontend

# When prompted:
# - Link to existing project or create new one
# - Set NEXT_PUBLIC_API_URL=https://nba-performance-prediction-production.up.railway.app
```

## Vercel Project Settings

Root Directory: `frontend`
Environment Variables: `NEXT_PUBLIC_API_URL=https://nba-performance-prediction-production.up.railway.app`
