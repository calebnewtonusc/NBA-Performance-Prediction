# NBA Performance Prediction - Production Deployment

## 🚀 LIVE PRODUCTION SYSTEM

**Frontend:** https://nba-performance-prediction.vercel.app
**Backend API:** https://nba-performance-prediction-production.up.railway.app  
**API Documentation:** https://nba-performance-prediction-production.up.railway.app/api/docs

## ✅ System Status

- **Backend:** Healthy and running on Railway
- **Frontend:** Deployed on Vercel
- **Model:** Trained on 2,788 real NBA games
- **Predictions:** Realistic (10-91% confidence range)

## 🎯 Quick Start

1. **Visit the web app:** https://nba-performance-prediction.vercel.app
2. Click "Predictions" in the navigation
3. Select home and away teams (e.g., BOS vs LAL)
4. Click "Predict Game"
5. View realistic NBA game predictions!

## 📊 Model Performance

**Real NBA Data:**
- 2,788 games from 2023-24 and 2024-25 seasons
- Training accuracy: 64.9%
- Test accuracy: 69.6%
- Home team win rate: 54.7%

**Prediction Examples:**
- BOS vs LAL → 69.8% confidence (home win)
- MIA vs PHX → 54.5% confidence (close game)
- No more unrealistic 99.999% predictions!

## 🔐 API Authentication

Username: `admin`
Password: `G9.zs8FGHP1W_lx^5eP,}mU2`

## 🧪 Test API Directly

```bash
# Login and get JWT token
TOKEN=$(curl -s -X POST "https://nba-performance-prediction-production.up.railway.app/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"G9.zs8FGHP1W_lx^5eP,}mU2"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

# Get prediction
curl -s -X POST "https://nba-performance-prediction-production.up.railway.app/api/predict/simple" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"home_team":"BOS","away_team":"LAL"}' | python3 -m json.tool
```

## 📚 What You Learned

✅ **Real API Integration** - nba_api for live NBA data
✅ **Data Engineering** - Fetched and processed 2,788 games
✅ **Machine Learning** - Logistic Regression with StandardScaler
✅ **Feature Engineering** - 18 features (win %, points, home/away splits)
✅ **REST API** - FastAPI with authentication and rate limiting
✅ **Frontend** - Next.js with React and Tailwind CSS
✅ **DevOps** - Railway + Vercel deployment pipeline
✅ **Version Control** - Git workflow with meaningful commits

## 🔄 Update Model Weekly

```bash
# Fetch latest NBA games
cd /Users/joelnewton/Desktop/2026-Code/projects/NBA-Performance-Prediction
python scripts/fetch_real_nba_data.py

# Retrain model with new data
python scripts/train_with_real_data.py

# Deploy updated model
git add models/
git commit -m "Update model with latest NBA data"
git push  # Auto-deploys to Railway
```

## 📁 Key Files

- `models/game_logistic/v1/model.pkl` - Trained model + scaler
- `src/api/main.py` - FastAPI backend with endpoints
- `src/api/nba_data_fetcher.py` - Live NBA stats fetcher
- `frontend/app/predictions/page.tsx` - Prediction interface
- `scripts/fetch_real_nba_data.py` - Fetch real NBA data
- `scripts/train_with_real_data.py` - Train on real data

## 🎓 Next Steps for Your Project

**Additional Models:**
1. Decision Trees (interpretability)
2. Random Forest (ensemble learning)
3. Ridge/Lasso Regression (player stats)
4. Model comparison dashboard

**Advanced Features:**
1. Head-to-head win history
2. Rest days tracking
3. Back-to-back game detection
4. Win/loss streaks
5. Injury data integration

## 🎉 Summary

Your NBA prediction system is **production-ready** with:
- ✅ Real data from 2,788 NBA games
- ✅ Realistic predictions (69.6% accuracy)
- ✅ Live deployments on Railway + Vercel
- ✅ Auto-fetching team statistics
- ✅ Clean production URLs
- ✅ Ready for semester learning!

**Start using it now:** https://nba-performance-prediction.vercel.app 🏀
