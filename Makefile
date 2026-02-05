.PHONY: help install test lint format clean data train dashboard docker

help:
	@echo "NBA Performance Prediction - Available Commands:"
	@echo ""
	@echo "  make install        Install dependencies"
	@echo "  make install-dev    Install with dev dependencies"
	@echo "  make sample-data    Generate sample data for testing"
	@echo "  make data           Collect real NBA data (requires API access)"
	@echo "  make train          Train all ML models"
	@echo "  make dashboard      Run the Streamlit dashboard"
	@echo "  make test           Run tests with pytest"
	@echo "  make lint           Run linting checks"
	@echo "  make format         Format code with black"
	@echo "  make clean          Clean temporary files"
	@echo "  make docker-build   Build Docker image"
	@echo "  make docker-run     Run Docker container"
	@echo ""

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 mypy jupyter

sample-data:
	@echo "Generating sample data..."
	python3 scripts/generate_sample_data.py

data:
	@echo "Collecting NBA data..."
	python3 scripts/collect_data.py --seasons 2023 2024

data-quick:
	@echo "Collecting sample NBA data (quick mode)..."
	python3 scripts/collect_data.py --quick --seasons 2023

train:
	@echo "Training all models..."
	python3 scripts/train_models.py --all

train-game:
	@echo "Training game prediction models..."
	python3 scripts/train_models.py --game-models

train-player:
	@echo "Training player statistics models..."
	python3 scripts/train_models.py --player-models

dashboard:
	@echo "Starting dashboard..."
	streamlit run src/visualization/dashboard.py

test:
	@echo "Running tests..."
	pytest tests/ -v --cov=src --cov-report=term-missing

test-quick:
	@echo "Running quick tests..."
	pytest tests/ -v -x

lint:
	@echo "Running linting..."
	flake8 src tests --max-line-length=120 --statistics
	mypy src --ignore-missing-imports || true

format:
	@echo "Formatting code..."
	black src tests scripts

format-check:
	@echo "Checking code format..."
	black --check src tests scripts

clean:
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/ dist/ build/

docker-build:
	@echo "Building Docker image..."
	docker build -t nba-prediction:latest .

docker-run:
	@echo "Running Docker container..."
	docker run -p 8501:8501 nba-prediction:latest

all: install sample-data train dashboard
