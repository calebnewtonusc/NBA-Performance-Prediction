"""Tests for Logistic Regression model"""

import pytest
import numpy as np
from sklearn.datasets import make_classification
from src.models.logistic_regression_model import GameLogisticRegression


class TestGameLogisticRegression:
    """Test GameLogisticRegression model"""

    @pytest.fixture
    def sample_data(self):
        """Create sample classification data"""
        X, y = make_classification(
            n_samples=200, n_features=10, n_informative=8, n_redundant=2, random_state=42
        )
        # Split data
        split_idx_train = int(0.7 * len(X))
        split_idx_val = int(0.85 * len(X))

        X_train, y_train = X[:split_idx_train], y[:split_idx_train]
        X_val, y_val = X[split_idx_train:split_idx_val], y[split_idx_train:split_idx_val]
        X_test, y_test = X[split_idx_val:], y[split_idx_val:]

        return X_train, y_train, X_val, y_val, X_test, y_test

    def test_model_initialization(self):
        """Test model can be initialized"""
        model = GameLogisticRegression()
        assert model is not None
        assert model.model is None  # Should be None before training

    def test_model_training(self, sample_data):
        """Test model can be trained"""
        X_train, y_train, X_val, y_val, X_test, y_test = sample_data

        model = GameLogisticRegression()
        metrics = model.train(
            X_train, y_train, X_val, y_val, tune_hyperparameters=False
        )

        assert model.model is not None
        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert 0 <= metrics["accuracy"] <= 1

    def test_model_prediction(self, sample_data):
        """Test model can make predictions"""
        X_train, y_train, X_val, y_val, X_test, y_test = sample_data

        model = GameLogisticRegression()
        model.train(X_train, y_train, X_val, y_val, tune_hyperparameters=False)

        predictions = model.predict(X_test)

        assert len(predictions) == len(y_test)
        assert all(pred in [0, 1] for pred in predictions)

    def test_model_predict_proba(self, sample_data):
        """Test model can predict probabilities"""
        X_train, y_train, X_val, y_val, X_test, y_test = sample_data

        model = GameLogisticRegression()
        model.train(X_train, y_train, X_val, y_val, tune_hyperparameters=False)

        probabilities = model.predict_proba(X_test)

        assert probabilities.shape[0] == len(y_test)
        assert probabilities.shape[1] == 2
        assert all(0 <= prob <= 1 for prob in probabilities.flatten())

    def test_model_evaluation(self, sample_data):
        """Test model evaluation returns correct metrics"""
        X_train, y_train, X_val, y_val, X_test, y_test = sample_data

        model = GameLogisticRegression()
        model.train(X_train, y_train, X_val, y_val, tune_hyperparameters=False)

        metrics = model.evaluate(X_test, y_test)

        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1" in metrics
        assert all(0 <= metrics[key] <= 1 for key in ["accuracy", "precision", "recall", "f1"])
