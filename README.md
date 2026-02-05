# NBA Performance Prediction

A collaborative machine learning project for predicting NBA game outcomes and individual player statistics using live NBA data.

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

- Python 3.8+
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

## Current Status

✅ **CORE IMPLEMENTATION COMPLETE!** The project has a fully functional codebase with:
- Complete data collection pipeline
- Advanced feature engineering
- Multiple ML models (classification and regression)
- Model management and retraining
- Interactive dashboard
- Comprehensive documentation

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

### 🔧 Data Processing
- Data cleaning and validation
- Missing value handling
- Outlier detection and removal
- Feature engineering:
  - Rolling averages
  - Team form metrics
  - Player efficiency ratings
  - Head-to-head history

### 🤖 Machine Learning Models

**Game Predictions (Classification):**
- Logistic Regression
- Decision Trees
- Random Forest
- Model comparison framework

**Player Statistics (Regression):**
- Linear Regression
- Ridge Regression (L2)
- Lasso Regression (L1)
- Multi-output regression

### 📈 Model Management
- Model versioning
- Automated retraining pipeline
- Production model deployment
- A/B testing framework

### 🎨 Visualization
- Interactive Streamlit dashboard
- Real-time predictions
- Model performance analytics
- Data exploration tools

## Project Phases

✅ **Phase 1**: Data Collection & API Integration - Code Complete
✅ **Phase 2**: Data Processing & Feature Engineering - Code Complete
✅ **Phase 3**: Game Prediction Models - Code Complete
✅ **Phase 4**: Player Statistics Models - Code Complete
✅ **Phase 5**: Live Data Integration & Retraining - Code Complete
✅ **Phase 6**: Visualization & Reporting - Code Complete

**Code Implementation: 6/6 phases complete (100%)**

📝 **Demonstration Notebooks**: 3/7+ notebooks created (see `notebooks/` directory)
- Additional notebooks planned for model demonstrations (see `docs/PROJECT_PLAN.md`)

## License

This is an educational project. Feel free to use and modify as needed.

## Team Members

Add your names here as you join the project!

- Joel Newton
- [Add your name]
- [Add your name]
- [Add your name]
