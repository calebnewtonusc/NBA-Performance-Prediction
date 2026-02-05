# Deploy Frontend to Vercel

Your Next.js frontend is ready to deploy to Vercel!

## Quick Deploy (5 minutes)

### Step 1: Import Project to Vercel

1. Go to https://vercel.com
2. Click "Add New..." → "Project"
3. Import your GitHub repository: `calebnewtonusc/NBA-Performance-Prediction`
4. Vercel will auto-detect Next.js

### Step 2: Configure Build Settings

Vercel should auto-configure, but verify:

- **Framework Preset:** Next.js
- **Root Directory:** `frontend`
- **Build Command:** `npm run build`
- **Output Directory:** `.next`
- **Install Command:** `npm install`

### Step 3: Set Environment Variable

Add this environment variable in Vercel:

```
NEXT_PUBLIC_API_URL=https://nba-performance-prediction-production.up.railway.app
```

### Step 4: Deploy!

Click "Deploy" and wait ~2 minutes.

Your frontend will be live at: `https://your-project.vercel.app`

## What You Get

### Live Pages:

1. **Home** (`/`) - API health dashboard with status cards
2. **Game Predictions** (`/predictions`) - Full prediction form with:
   - Team selection dropdowns (30 NBA teams)
   - Win percentage inputs
   - Real-time predictions from Railway API
   - Interactive chart showing win probabilities
3. **Player Stats** (`/players`) - Placeholder (coming soon)
4. **Model Performance** (`/performance`) - Placeholder (coming soon)
5. **Data Explorer** (`/explorer`) - Placeholder (coming soon)

### Features:

- ✅ Modern, responsive design with Tailwind CSS
- ✅ Dark theme matching your original Streamlit dashboard
- ✅ Real-time API integration with Railway backend
- ✅ Interactive charts with Recharts
- ✅ TypeScript for type safety
- ✅ Automatic deployments on git push

## Update CORS in Railway

After deployment, update your Railway API's ALLOWED_ORIGINS:

1. Go to Railway → Your API service → Variables
2. Update `ALLOWED_ORIGINS` to:
```
https://your-project.vercel.app,http://localhost:8501
```
3. Railway will auto-redeploy (~30 seconds)

## Test Your Deployment

1. Visit your Vercel URL
2. Navigate to "Game Predictions"
3. Select two teams (e.g., BOS vs LAL)
4. Enter win percentages (e.g., 0.650 and 0.600)
5. Click "Get Prediction"
6. You should see the prediction with confidence score

## Architecture

```
GitHub Repository
  └── Push to main → Vercel auto-deploys frontend

Vercel Frontend (Next.js)
  └── API calls → Railway Backend (FastAPI)
        ├── PostgreSQL
        └── Redis

```

## Cost

- **Vercel:** FREE (Hobby tier)
  - Unlimited deployments
  - Automatic HTTPS
  - Global CDN
  - 100GB bandwidth/month

- **Railway:** $10-15/month (existing backend)

**Total:** $10-15/month

## Customization

### Colors

Edit `frontend/tailwind.config.js`:

```javascript
colors: {
  primary: '#FF6B6B',      // Your primary color
  background: '#0E1117',   // Background color
  secondary: '#262730',    // Card background
  text: '#FAFAFA',         // Text color
},
```

### Add More Features

1. Player Stats page: `frontend/app/players/page.tsx`
2. Model Performance: `frontend/app/performance/page.tsx`
3. Data Explorer: `frontend/app/explorer/page.tsx`

Just edit the placeholder pages and Vercel will auto-deploy!

## Troubleshooting

### Build Fails on Vercel

Check:
- Root directory is set to `frontend`
- Node.js version is 18.x or higher

### API Calls Failing

Check:
- `NEXT_PUBLIC_API_URL` environment variable is set
- Railway API is running (check https://nba-performance-prediction-production.up.railway.app/api/health)
- CORS is configured with your Vercel URL

### Styling Issues

Clear cache and rebuild:
```bash
cd frontend
rm -rf .next node_modules
npm install
npm run dev
```

## Next Steps

1. Deploy to Vercel (5 minutes)
2. Update CORS in Railway
3. Test predictions
4. Share your URL!

Your frontend will automatically redeploy whenever you push to GitHub main branch.

---

**Live URLs:**
- Frontend: https://your-project.vercel.app (after deployment)
- API: https://nba-performance-prediction-production.up.railway.app
- API Docs: https://nba-performance-prediction-production.up.railway.app/api/docs
