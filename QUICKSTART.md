# 🚀 Quick Start Guide

Get up and running with NBA Performance Prediction in 5 minutes!

## Option 1: Automated Setup (Recommended)

Run the automated quickstart script:

```bash
cd NBA-Performance-Prediction
./scripts/quickstart.sh
```

This will:
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Generate sample data
- ✅ Train all models
- ✅ Set up the project

Then start the dashboard:
```bash
make dashboard
# or
streamlit run src/visualization/dashboard.py
```

## Option 2: Manual Setup

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Generate Sample Data

```bash
# Generate synthetic data for testing
python scripts/generate_sample_data.py
```

**OR** collect real NBA data:

```bash
# Collect real data (requires API access)
python scripts/collect_data.py --quick --seasons 2023
```

### 3. Train Models

```bash
# Train all models
python scripts/train_models.py --all

# Or train specific models
python scripts/train_models.py --game-models
python scripts/train_models.py --player-models
```

### 4. Run Dashboard

```bash
streamlit run src/visualization/dashboard.py
```

Visit `http://localhost:8501` in your browser!

## Option 3: Using Make

```bash
# Install and set up everything
make install
make sample-data
make train

# Run dashboard
make dashboard
```

## Option 4: Using Docker

```bash
# Build image
docker build -t nba-prediction .

# Run container
docker run -p 8501:8501 nba-prediction

# Visit http://localhost:8501
```

## Using the Project

### Predict a Game

```python
from src.models.model_manager import ModelManager

# Load production model
manager = ModelManager()
model = manager.get_production_model('game_logistic')

# Make prediction
prediction = model.predict(game_features)
probability = model.predict_proba(game_features)
```

### Predict Player Stats

```python
from src.models.model_manager import ModelManager

# Load model
manager = ModelManager()
model = manager.load_model('player_ridge', 'v1')

# Predict
predicted_points = model.predict(player_features)
```

### Explore Data

```bash
# Open Jupyter notebook
jupyter notebook notebooks/01_data_collection_demo.ipynb
```

## Common Commands

```bash
# Run tests
make test

# Format code
make format

# Check code quality
make lint

# Clean temporary files
make clean

# See all commands
make help
```

## Troubleshooting

### Import Errors

If you get import errors, make sure you're in the project root and virtual environment is activated:

```bash
cd NBA-Performance-Prediction
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### API Rate Limits

If collecting real data fails due to rate limits:

```bash
# Use sample data instead
python scripts/generate_sample_data.py

# Or use quick mode
python scripts/collect_data.py --quick
```

### Streamlit Port Already in Use

```bash
# Run on different port
streamlit run src/visualization/dashboard.py --server.port 8502
```

## What's Next?

1. **Explore the notebooks** in `notebooks/` directory
2. **Read the full documentation** in `docs/`
3. **Check the project plan** in `docs/PROJECT_PLAN.md`
4. **Customize models** in `src/models/`
5. **Add new features** in `src/data_processing/`

## Team Collaboration

1. **Claim a task** in `docs/PROJECT_PLAN.md`
2. **Create a branch**: `git checkout -b feature/your-feature`
3. **Make changes** and commit
4. **Push**: `git push origin feature/your-feature`
5. **Create Pull Request** on GitHub

## Need Help?

- Check `README.md` for full documentation
- Browse example notebooks in `notebooks/`
- Read API guide in `docs/API_GUIDE.md`
- Review project plan in `docs/PROJECT_PLAN.md`

Happy predicting! 🏀
