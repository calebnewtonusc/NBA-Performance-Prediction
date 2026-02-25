# NBA Performance Prediction

![Next.js](https://img.shields.io/badge/Next.js-14-000000?logo=nextdotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178C6?logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-models-F7931E?logo=scikitlearn&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Railway-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-yellow)

NBA game outcome and player statistics prediction dashboard. Six trained ML models, a Next.js frontend with an Apple TV dark aesthetic, and a FastAPI backend deployed on Railway.

**Live app:** [nba-performance-prediction.vercel.app](https://nba-performance-prediction.vercel.app) &nbsp;|&nbsp; **API:** [Railway](https://nba-performance-prediction-production.up.railway.app/api/docs)

> Screenshot

## Features

- **Game outcome predictions**: compare win probabilities from Logistic Regression (69.6%), Decision Tree (61.6%), and Random Forest (67.3%) side-by-side
- **Player statistics forecasts**: points, rebounds, and assists regression using Linear, Ridge, and Lasso models trained on 2,788 real NBA games
- **Data Explorer**: browse and filter historical game data with paginated tables and advanced search
- **Player search**: fuzzy-matched autocomplete across 200+ NBA players with recent search history persisted in localStorage
- **Model performance monitor**: live accuracy, precision, recall, and F1 metrics with data freshness indicators
- **40x faster feature engineering**: vectorized Pandas 3.0-compatible operations for team form, streaks, and head-to-head stats

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14, TypeScript, Tailwind CSS, Recharts, Framer Motion |
| Backend | FastAPI, SQLAlchemy, Pydantic, JWT auth (bcrypt) |
| ML Models | scikit-learn: Logistic Regression, Decision Tree, Random Forest, Linear/Ridge/Lasso |
| Data | nba_api (2,788 games), balldontlie.io live stats |
| Caching | 5-minute in-memory cache with automatic invalidation |
| Deployment | Vercel (frontend), Railway Docker (backend) |

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- Free API key from [balldontlie.io](https://app.balldontlie.io)

### Setup

```bash
git clone https://github.com/calebnewtonusc/NBA-Performance-Prediction.git
cd NBA-Performance-Prediction

# Configure API key
cp .env.example .env
# Add: BALLDONTLIE_API_KEY=your_key_here

# Install Python dependencies
pip install -r requirements.txt

# Generate data and train models
make sample-data
make train

# Start FastAPI backend
uvicorn src.api.main:app --reload

# Start Next.js frontend (new terminal)
cd frontend
npm install
npm run dev
# App: http://localhost:3000
```

Or use the quickstart script:

```bash
./scripts/quickstart.sh
```

## Project Structure

```
NBA-Performance-Prediction/
├── src/
│   ├── data_collection/   # NBA API clients, rate limiting, data fetching
│   ├── data_processing/   # Feature engineering (40x vectorized speedup)
│   ├── models/            # Logistic regression, decision tree, random forest, regression
│   ├── evaluation/        # Metrics, cross-validation, model comparison
│   └── api/               # FastAPI server with JWT auth
├── frontend/              # Next.js 14 app (predictions, players, explorer, performance)
├── notebooks/             # Jupyter exploration (data collection → model comparison)
├── data/                  # Raw, processed, and external datasets
└── tests/                 # 90%+ coverage (unit, integration, benchmarks)
```

## Model Results

| Model | Task | Metric |
|---|---|---|
| Logistic Regression | Game outcome | 69.6% accuracy |
| Random Forest | Game outcome | 67.3% accuracy |
| Decision Tree | Game outcome | 61.6% accuracy |
| Linear Regression | Player points | 2.49 MAE |
| Ridge Regression | Player points | 2.49 MAE |
| Lasso Regression | Player points | 2.50 MAE |

## Author

**Caleb Newton** | [calebnewton.me](https://calebnewton.me) | [GitHub](https://github.com/calebnewtonusc)
