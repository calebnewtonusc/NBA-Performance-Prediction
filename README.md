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

### Prerequisites

- Python 3.8+
- pip
- Git

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd NBA-Performance-Prediction
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Quick Start

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

Project is in initial setup phase. See [PROJECT_PLAN.md](docs/PROJECT_PLAN.md) for the roadmap.

## License

This is an educational project. Feel free to use and modify as needed.

## Team Members

Add your names here as you join the project!

- Joel Newton
- [Add your name]
- [Add your name]
- [Add your name]
