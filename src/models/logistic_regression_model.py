"""
Logistic Regression Model for Game Outcome Prediction

This module implements logistic regression for predicting NBA game winners.

Usage:
    from src.models.logistic_regression_model import GameLogisticRegression

    model = GameLogisticRegression()
    model.train(X_train, y_train)
    predictions = model.predict(X_test)
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, cross_val_score
from typing import Dict, Any, Optional, Tuple
import pickle
from pathlib import Path
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class GameLogisticRegression:
    """Logistic Regression model for game outcome prediction"""

    def __init__(self, random_state: int = 42):
        """
        Initialize the logistic regression model

        Args:
            random_state: Random seed for reproducibility
        """
        self.random_state = random_state
        self.model = None
        self.best_params = None
        self.feature_importance = None
        self.feature_names = None

    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: Optional[pd.DataFrame] = None,
        y_val: Optional[pd.Series] = None,
        tune_hyperparameters: bool = True
    ) -> Dict[str, Any]:
        """
        Train the logistic regression model

        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features (optional)
            y_val: Validation labels (optional)
            tune_hyperparameters: Whether to perform hyperparameter tuning

        Returns:
            Dictionary with training metrics
        """
        logger.info("Training Logistic Regression model...")

        self.feature_names = X_train.columns.tolist()

        if tune_hyperparameters:
            logger.info("Performing hyperparameter tuning...")
            self.model = self._tune_hyperparameters(X_train, y_train)
        else:
            self.model = LogisticRegression(
                random_state=self.random_state,
                max_iter=1000
            )
            self.model.fit(X_train, y_train)

        # Calculate feature importance (coefficient magnitudes)
        self.feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'coefficient': self.model.coef_[0],
            'abs_coefficient': np.abs(self.model.coef_[0])
        }).sort_values('abs_coefficient', ascending=False)

        # Training metrics
        train_score = self.model.score(X_train, y_train)
        metrics = {
            'train_accuracy': train_score,
            'best_params': self.best_params
        }

        if X_val is not None and y_val is not None:
            val_score = self.model.score(X_val, y_val)
            metrics['val_accuracy'] = val_score
            logger.info(f"Validation accuracy: {val_score:.4f}")

        logger.info(f"Training complete. Train accuracy: {train_score:.4f}")

        return metrics

    def _tune_hyperparameters(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series
    ) -> LogisticRegression:
        """
        Tune hyperparameters using GridSearchCV

        Args:
            X_train: Training features
            y_train: Training labels

        Returns:
            Best model from grid search
        """
        param_grid = {
            'C': [0.001, 0.01, 0.1, 1, 10, 100],
            'penalty': ['l1', 'l2'],
            'solver': ['liblinear', 'saga']
        }

        grid_search = GridSearchCV(
            LogisticRegression(random_state=self.random_state, max_iter=1000),
            param_grid,
            cv=5,
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )

        grid_search.fit(X_train, y_train)

        self.best_params = grid_search.best_params_
        logger.info(f"Best parameters: {self.best_params}")
        logger.info(f"Best CV score: {grid_search.best_score_:.4f}")

        return grid_search.best_estimator_

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions

        Args:
            X: Features to predict

        Returns:
            Predicted labels (0 or 1)
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train() first.")

        return self.model.predict(X)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict class probabilities

        Args:
            X: Features to predict

        Returns:
            Probability estimates for each class
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train() first.")

        return self.model.predict_proba(X)

    def evaluate(
        self,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> Dict[str, float]:
        """
        Evaluate model performance

        Args:
            X_test: Test features
            y_test: Test labels

        Returns:
            Dictionary with evaluation metrics
        """
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

        predictions = self.predict(X_test)
        probabilities = self.predict_proba(X_test)[:, 1]

        metrics = {
            'accuracy': accuracy_score(y_test, predictions),
            'precision': precision_score(y_test, predictions),
            'recall': recall_score(y_test, predictions),
            'f1_score': f1_score(y_test, predictions),
            'roc_auc': roc_auc_score(y_test, probabilities)
        }

        logger.info(f"Test accuracy: {metrics['accuracy']:.4f}")
        logger.info(f"Test F1 score: {metrics['f1_score']:.4f}")
        logger.info(f"Test ROC AUC: {metrics['roc_auc']:.4f}")

        return metrics

    def get_feature_importance(self, top_n: int = 10) -> pd.DataFrame:
        """
        Get top N most important features

        Args:
            top_n: Number of top features to return

        Returns:
            DataFrame with top features and their importance
        """
        if self.feature_importance is None:
            raise ValueError("Model not trained yet. Call train() first.")

        return self.feature_importance.head(top_n)

    def cross_validate(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        cv: int = 5
    ) -> Dict[str, Any]:
        """
        Perform cross-validation

        Args:
            X: Features
            y: Labels
            cv: Number of folds

        Returns:
            Dictionary with cross-validation results
        """
        if self.model is None:
            self.model = LogisticRegression(random_state=self.random_state, max_iter=1000)

        scores = cross_val_score(self.model, X, y, cv=cv, scoring='accuracy')

        results = {
            'mean_score': scores.mean(),
            'std_score': scores.std(),
            'all_scores': scores
        }

        logger.info(f"Cross-validation accuracy: {results['mean_score']:.4f} (+/- {results['std_score']:.4f})")

        return results

    def save(self, filepath: str):
        """
        Save model to disk

        Args:
            filepath: Path to save the model
        """
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")

        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'feature_importance': self.feature_importance,
            'best_params': self.best_params
        }

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

        logger.info(f"Model saved to {filepath}")

    def load(self, filepath: str):
        """
        Load model from disk

        Args:
            filepath: Path to load the model from
        """
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)

        self.model = model_data['model']
        self.feature_names = model_data['feature_names']
        self.feature_importance = model_data['feature_importance']
        self.best_params = model_data.get('best_params')

        logger.info(f"Model loaded from {filepath}")


# Example usage
if __name__ == "__main__":
    # This would normally use real data
    print("Logistic Regression Model - Ready for training!")
    print("Load your dataset and call train() to build the model")
