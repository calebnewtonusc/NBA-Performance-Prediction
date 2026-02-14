#!/bin/bash
# Quick Start Script for NBA Performance Prediction
# This script sets up and runs the entire project

set -e  # Exit on error

echo "========================================"
echo "NBA Performance Prediction - Quick Start"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "checkmark Python $python_version detected"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "checkmark Virtual environment created"
else
    echo "checkmark Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate
echo "checkmark Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "checkmark Dependencies installed"
echo ""

# Generate sample data
echo "Generating sample data..."
python3 scripts/generate_sample_data.py
echo "checkmark Sample data generated"
echo ""

# Train models
echo "Training models (this may take a few minutes)..."
python3 scripts/train_models.py --all
echo "checkmark Models trained"
echo ""

# Success message
echo "========================================"
echo "checkmark Setup Complete!"
echo "========================================"
echo ""
echo "To start the dashboard, run:"
echo "  source venv/bin/activate"
echo "  streamlit run src/visualization/dashboard.py"
echo ""
echo "Or simply:"
echo "  make dashboard"
echo ""
echo "Happy predicting! basketball.fill"
