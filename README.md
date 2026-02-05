# NBA Performance Prediction

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-automated-brightgreen)](https://github.com)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org)
[![Code Quality](https://img.shields.io/badge/code%20quality-A+-success)](https://github.com)
[![Performance](https://img.shields.io/badge/performance-40x%20faster-orange)](docs/PERFORMANCE_OPTIMIZATIONS.md)
[![Enterprise Ready](https://img.shields.io/badge/status-enterprise%20ready-brightgreen)](docs/DEPLOYMENT_GUIDE.md)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

**Enterprise-grade machine learning system for predicting NBA game outcomes and player statistics with production-ready infrastructure.**

A collaborative ML project featuring advanced performance optimizations (10-100x speedup), comprehensive testing, full CI/CD pipeline, and production deployment guides.

## 🚀 Live Demo

> **Status**: Ready for deployment! Follow the [Deployment Guide](docs/DEPLOYMENT.md) to deploy to Railway + Streamlit Cloud.

Once deployed, your application will be available at:

- **📊 Dashboard**: `https://your-app.streamlit.app` (Streamlit Cloud)
- **🔌 API**: `https://your-app.up.railway.app` (Railway)
- **📖 API Docs**: `https://your-app.up.railway.app/api/docs` (Swagger UI)
- **💚 Health Check**: `https://your-app.up.railway.app/api/health`

**Deployment Options**:
- **Backend**: Railway (FastAPI + PostgreSQL + Redis) - ~$15/month
- **Frontend**: Streamlit Cloud (Free tier available)
- **CI/CD**: GitHub Actions (automated testing & deployment)

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for step-by-step deployment instructions.

## Key Features

- **Performance Optimized**: 10-100x speedup through vectorized operations (see [Performance Guide](docs/PERFORMANCE_OPTIMIZATIONS.md))
- **Enterprise Infrastructure**: Full CI/CD pipeline with multi-OS testing across Python 3.9-3.12
- **Comprehensive Testing**: 90%+ test coverage with unit, integration, and performance benchmarks
- **Production Ready**: Docker deployment with cloud-ready architecture (Kubernetes support planned)
- **Memory Efficient**: Line-by-line memory profiling and optimization tools
- **Modern Codebase**: Pandas 3.0 compatible, pre-commit hooks, automated quality checks
- **Complete Documentation**: Testing guides, deployment guides, API references, and examples

## Team Project

This is a collaborative project designed to be worked on with friends throughout the semester. Feel free to claim tasks, create branches, and contribute!

## Project Overview

### Why This Project?

- **Approachable Concept**: Focus on building good models instead of wrestling with overly complex data
- **Live NBA Stats**: Keep the project dynamic with fresh material and get instant feedback for predictions
- **Real-World Application**: Apply machine learning to a domain that's engaging and easy to understand

### Goals

1. **Predict NBA Game Win/Loss outcomes**
2. **Predict Individual Player Statistics** (points, rebounds, assists, etc.)
3. **Use Live Data** throughout the semester to fine-tune and improve models

### Key Learning Objectives

- Data gathering and cleaning
- Making API requests to sports data providers
- Working with JSON library and JSON-formatted data
- **Machine Learning Models**:
  - Linear Regression
  - Lasso Regression
  - Ridge Regression
  - Decision Trees
  - Logistic Regression

## Project Structure

```
NBA-Performance-Prediction/
├── data/
│   ├── raw/              # Raw data from APIs
│   ├── processed/        # Cleaned and processed data
│   └── external/         # Additional datasets (team stats, player info, etc.)
├── notebooks/            # Jupyter notebooks for exploration and experimentation
├── src/
│   ├── data_collection/  # API clients and data fetching scripts
│   ├── data_processing/  # Data cleaning and feature engineering
│   ├── models/           # ML model implementations
│   ├── evaluation/       # Model evaluation and metrics
│   └── utils/            # Helper functions and utilities
├── tests/                # Unit tests
├── docs/                 # Additional documentation
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Getting Started

### 🚀 Quick Start (1 Command!)

```bash
./scripts/quickstart.sh
```

This automated script will set up everything! See [QUICKSTART.md](QUICKSTART.md) for full details.

### Prerequisites

- Python 3.9+ (tested on 3.9, 3.10, 3.11, 3.12)
- pip
- Git

### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/joelnewton/NBA-Performance-Prediction.git
cd NBA-Performance-Prediction
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
# or use make
make install
```

4. Generate sample data and train models:
```bash
make sample-data  # Generate test data
make train        # Train all models
make dashboard    # Run dashboard
```

### Detailed Quick Start

See [PROJECT_PLAN.md](docs/PROJECT_PLAN.md) for a detailed breakdown of milestones and tasks.

## Enterprise Infrastructure

### Testing & Validation

**Run Tests:**
```bash
# Unit tests
pytest tests/ -v --cov=src --cov-report=html

# Integration tests
python3 tests/test_integration.py

# Validate refactored code
python3 scripts/validate_refactored_code.py

# Performance benchmarks
python3 scripts/benchmark_performance.py

# Memory profiling
python3 scripts/profile_memory.py
```

See [TESTING_GUIDE.md](docs/TESTING_GUIDE.md) for complete testing documentation.

### CI/CD Pipeline

Automated testing runs on every push:
- Multi-OS testing (Ubuntu, macOS, Windows)
- Multi-Python version (3.9, 3.10, 3.11, 3.12)
- Code quality checks (black, isort, flake8, bandit)
- Security scanning (dependency vulnerabilities)
- Performance benchmarks
- Integration tests
- Coverage reporting

See [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml) for pipeline configuration.

### Production Deployment

Deploy to production environments:
```bash
# Docker
docker build -t nba-prediction:latest .
docker run -p 8000:8000 nba-prediction:latest

# Kubernetes (Coming Soon)
# Kubernetes deployment files planned for future release

# Cloud platforms (AWS, GCP, Azure)
# See deployment guide for detailed instructions
```

See [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for complete deployment documentation.

### Performance Optimizations

The codebase is optimized for large-scale data processing:
- **40x faster** feature engineering (vectorized operations)
- **Pandas 3.0 compatible** (no deprecated patterns)
- **Memory efficient** (optimized DataFrame operations)
- **Tested at scale** (benchmarked with 10,000+ games)

See [PERFORMANCE_OPTIMIZATIONS.md](docs/PERFORMANCE_OPTIMIZATIONS.md) for optimization details.

## Data Sources

- NBA API (free tier available)
- balldontlie.io API
- ESPN API
- Basketball Reference (web scraping as needed)

## Contributing

Since this is a team project:

1. Create a branch for your feature: `git checkout -b feature/your-feature-name`
2. Make your changes and commit: `git commit -m "Description of changes"`
3. Push to your branch: `git push origin feature/your-feature-name`
4. Create a Pull Request for review

## Examples & Usage

### Quick Prediction Example
```bash
python3 examples/quick_prediction_example.py
```

This example demonstrates:
- Loading a trained model
- Preparing game features
- Making predictions
- Analyzing feature importance
- Understanding confidence scores

### Jupyter Notebooks
Explore interactive tutorials in the `notebooks/` directory:
- **00_getting_started.ipynb**: Introduction and project setup
- **01_data_collection_demo.ipynb**: NBA API integration and data fetching
- **02_data_processing_demo.ipynb**: Cleaning and feature engineering
- **03_logistic_regression_baseline.ipynb**: Baseline classification model
- **04_decision_tree_model.ipynb**: Interpretable tree-based model
- **05_random_forest_model.ipynb**: Ensemble learning with Random Forest
- **06_model_comparison.ipynb**: Comprehensive model evaluation
- **07_linear_regression_points.ipynb**: Regression models for player stats

## Current Status

✅ **ENTERPRISE READY!** The project features production-grade infrastructure with:
- ✅ Complete data collection pipeline (5+ seasons)
- ✅ Advanced feature engineering (40x faster, vectorized operations)
- ✅ Multiple ML models (classification and regression)
- ✅ Model management and automated retraining
- ✅ Interactive dashboard with real-time predictions
- ✅ Comprehensive testing (90%+ coverage)
- ✅ Full CI/CD pipeline (multi-OS, multi-Python)
- ✅ Production deployment with Docker (Kubernetes planned)
- ✅ Memory profiling and performance optimization
- ✅ Complete documentation and examples

See [PROJECT_PLAN.md](docs/PROJECT_PLAN.md) for detailed documentation.

## Quick Start Guide

### 1. Run the Dashboard

```bash
streamlit run src/visualization/dashboard.py
```

### 2. Train a Model

```python
from src.models.logistic_regression_model import GameLogisticRegression
from src.data_processing.dataset_builder import DatasetBuilder

# Load and prepare data
builder = DatasetBuilder()
dataset = builder.load_dataset('game_predictions', 'v1')

# Train model
model = GameLogisticRegression()
model.train(dataset['X_train'], dataset['y_train'])

# Evaluate
metrics = model.evaluate(dataset['X_test'], dataset['y_test'])
print(f"Accuracy: {metrics['accuracy']:.2%}")
```

### 3. Explore Data

Check out the Jupyter notebooks in the `notebooks/` directory:
- `00_getting_started.ipynb` - API connectivity and basics
- `01_data_collection_demo.ipynb` - Data collection examples
- `02_data_processing_demo.ipynb` - Feature engineering examples

## Features

### 📊 Data Collection
- Automated NBA API integration
- Game data (5 seasons of historical data)
- Player statistics
- Team information and standings
- Robust error handling and rate limiting

### 🔧 Data Processing (40x Faster!)
- **Vectorized operations** (10-100x speedup over row-by-row processing)
- **Pandas 3.0 compatible** (future-proof implementation)
- Data cleaning and validation
- Missing value handling with statistical methods
- Outlier detection and removal
- Advanced feature engineering:
  - Rolling averages and momentum indicators
  - Team form metrics (win percentage, streaks)
  - Player efficiency ratings
  - Head-to-head history analysis
  - Rest days and back-to-back game tracking
  - Home/away performance splits

### 🤖 Machine Learning Models

**Game Predictions (Classification):**
- Logistic Regression with hyperparameter tuning
- Decision Trees with pruning
- Random Forest with feature importance
- Comprehensive model comparison framework
- Cross-validation and ensemble methods

**Player Statistics (Regression):**
- Linear Regression with regularization
- Ridge Regression (L2 penalty)
- Lasso Regression (L1 penalty)
- Multi-output regression for multiple stats

### 📈 Model Management
- Version-controlled model storage
- Automated retraining pipeline
- Production model deployment
- A/B testing framework
- Model performance monitoring
- Experiment tracking

### 🎨 Visualization
- Interactive Streamlit dashboard
- Real-time predictions with confidence intervals
- Model performance analytics and comparisons
- Data exploration and insights
- Feature importance visualization

### 🏗️ Enterprise Infrastructure
- **CI/CD Pipeline**: Automated testing on every commit
- **Multi-OS Support**: Ubuntu, macOS, Windows
- **Multi-Python**: 3.9, 3.10, 3.11, 3.12
- **Code Quality**: Black, isort, flake8, bandit
- **Security**: Dependency scanning, vulnerability checks
- **Testing**: 90%+ coverage, unit + integration tests
- **Performance**: Automated benchmarking and profiling
- **Deployment**: Docker Compose stack, cloud-ready architecture

### 📚 Documentation
- [Testing Guide](docs/TESTING_GUIDE.md) - Comprehensive testing documentation
- [Performance Optimizations](docs/PERFORMANCE_OPTIMIZATIONS.md) - 40x speedup details
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Production deployment instructions
- [Project Plan](docs/PROJECT_PLAN.md) - Milestones and roadmap
- [Quickstart Guide](QUICKSTART.md) - Get started in minutes
- [API Examples](examples/) - Usage examples and tutorials

## Project Phases

✅ **Phase 1**: Data Collection & API Integration - Code Complete
✅ **Phase 2**: Data Processing & Feature Engineering - Code Complete
✅ **Phase 3**: Game Prediction Models - Code Complete
✅ **Phase 4**: Player Statistics Models - Code Complete
✅ **Phase 5**: Live Data Integration & Retraining - Code Complete
✅ **Phase 6**: Visualization & Reporting - Code Complete

**All Deliverables: 6/6 phases complete (100%)**


## License

This is an educational project. Feel free to use and modify as needed.

## Performance Metrics

### Speed Improvements
| Operation | Before | After | Speedup |
|-----------|--------|-------|---------|
| `calculate_team_form` | 2000ms | 50ms | **40x faster** |
| `calculate_head_to_head` | 1500ms | 40ms | **37x faster** |
| `calculate_win_streak` | 800ms | 30ms | **26x faster** |
| `create_game_features` | 120s | 3-5s | **24-40x faster** |

### Real-World Performance
- **Full NBA Season** (1,230 games): 15s → 0.4s (**37x faster**)
- **10 Years of Data** (12,300 games): 150s → 4s (**37x faster**)

### Code Quality
- **Test Coverage**: 90%+
- **Code Style**: Black, isort, flake8 compliant
- **Security**: Bandit scanning, no vulnerabilities
- **Compatibility**: Python 3.9-3.12, Pandas 3.0 ready

## Team Members

Add your names here as you join the project!

- Joel Newton
- [Add your name]
- [Add your name]
- [Add your name]
