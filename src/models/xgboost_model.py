"""
XGBoost Model for NBA Game Predictions

Gradient boosting implementation with advanced features:
- Hyperparameter tuning
- Feature importance analysis
- Early stopping
- Cross-validation
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import numpy as np
import pandas as pd
from typing import Dict, Optional, Tuple

try:
    import xgboost as xgb
    from xgboost import XGBClassifier

    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("[exclamationmark.triangle]  XGBoost not installed. Install with: pip install xgboost")

from src.models.base_model import BaseModel


class GameXGBoost(BaseModel):
    """XGBoost classifier for NBA game predictions"""

    def __init__(self, **kwargs):
        """
        Initialize XGBoost model

        Args:
            **kwargs: XGBoost hyperparameters
        """
        if not XGBOOST_AVAILABLE:
            raise ImportError("XGBoost package not installed")

        super().__init__()

        # Default hyperparameters (can be overridden)
        default_params = {
            "objective": "binary:logistic",
            "eval_metric": "logloss",
            "max_depth": 6,
            "learning_rate": 0.1,
            "n_estimators": 200,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "min_child_weight": 1,
            "gamma": 0,
            "reg_alpha": 0,
            "reg_lambda": 1,
            "random_state": 42,
            "tree_method": "hist",  # Faster training
            "predictor": "cpu_predictor",
        }

        # Update with provided kwargs
        default_params.update(kwargs)

        self.model = XGBClassifier(**default_params)
        self.feature_names = None
        self.is_trained = False

    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: Optional[pd.DataFrame] = None,
        y_val: Optional[pd.Series] = None,
        tune_hyperparameters: bool = False,
        early_stopping_rounds: int = 10,
    ) -> Dict:
        """
        Train XGBoost model

        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features
            y_val: Validation labels
            tune_hyperparameters: Whether to tune hyperparameters
            early_stopping_rounds: Early stopping patience

        Returns:
            Training history
        """
        self.feature_names = list(X_train.columns)

        if tune_hyperparameters:
            print("[wrench.fill] Tuning hyperparameters...")
            self._tune_hyperparameters(X_train, y_train)

        # Training with validation set for early stopping
        if X_val is not None and y_val is not None:
            eval_set = [(X_train, y_train), (X_val, y_val)]
            self.model.fit(
                X_train,
                y_train,
                eval_set=eval_set,
                early_stopping_rounds=early_stopping_rounds,
                verbose=False,
            )

            # Get training history
            results = self.model.evals_result()
            history = {
                "train_logloss": results["validation_0"]["logloss"],
                "val_logloss": results["validation_1"]["logloss"],
                "best_iteration": self.model.best_iteration,
            }
        else:
            self.model.fit(X_train, y_train)
            history = {}

        self.is_trained = True
        print(f"[checkmark.circle] XGBoost training complete (best iteration: {self.model.best_iteration})")

        return history

    def _tune_hyperparameters(self, X_train: pd.DataFrame, y_train: pd.Series):
        """
        Tune hyperparameters using grid search

        Args:
            X_train: Training features
            y_train: Training labels
        """
        from sklearn.model_selection import GridSearchCV

        param_grid = {
            "max_depth": [3, 5, 7],
            "learning_rate": [0.01, 0.1, 0.3],
            "n_estimators": [100, 200, 300],
            "subsample": [0.8, 0.9, 1.0],
            "colsample_bytree": [0.8, 0.9, 1.0],
        }

        grid_search = GridSearchCV(
            self.model, param_grid, cv=3, scoring="accuracy", n_jobs=-1, verbose=0
        )

        grid_search.fit(X_train, y_train)

        print(f"   Best hyperparameters: {grid_search.best_params_}")
        print(f"   Best CV score: {grid_search.best_score_:.4f}")

        self.model = grid_search.best_estimator_

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        return self.model.predict(X)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Predict class probabilities"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        return self.model.predict_proba(X)

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict:
        """
        Evaluate model performance

        Returns:
            Dictionary of metrics
        """
        from sklearn.metrics import (
            accuracy_score,
            precision_score,
            recall_score,
            f1_score,
            roc_auc_score,
            log_loss,
        )

        y_pred = self.predict(X_test)
        y_proba = self.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1_score": f1_score(y_test, y_pred, zero_division=0),
            "roc_auc": roc_auc_score(y_test, y_proba),
            "log_loss": log_loss(y_test, y_proba),
        }

        print("\n[chart.bar.fill] XGBoost Model Performance:")
        for metric, value in metrics.items():
            print(f"   {metric}: {value:.4f}")

        return metrics

    def get_feature_importance(self, feature_names: Optional[list] = None) -> pd.DataFrame:
        """
        Get feature importance

        Args:
            feature_names: List of feature names

        Returns:
            DataFrame with feature importance
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")

        if feature_names is None:
            feature_names = self.feature_names

        # Get importance using different metrics
        importance_gain = self.model.get_booster().get_score(importance_type="gain")
        importance_weight = self.model.get_booster().get_score(importance_type="weight")
        importance_cover = self.model.get_booster().get_score(importance_type="cover")

        # Create DataFrame
        importance_df = pd.DataFrame(
            {
                "feature": feature_names,
                "gain": [importance_gain.get(f"f{i}", 0) for i in range(len(feature_names))],
                "weight": [
                    importance_weight.get(f"f{i}", 0) for i in range(len(feature_names))
                ],
                "cover": [importance_cover.get(f"f{i}", 0) for i in range(len(feature_names))],
            }
        )

        # Normalize to sum to 1
        if importance_df["gain"].sum() > 0:
            importance_df["gain_normalized"] = (
                importance_df["gain"] / importance_df["gain"].sum()
            )
        else:
            importance_df["gain_normalized"] = 0

        return importance_df.sort_values("gain", ascending=False)

    def save(self, filepath: str):
        """Save model to file"""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")

        self.model.save_model(filepath)
        print(f"[checkmark.circle] Model saved to {filepath}")

    def load(self, filepath: str):
        """Load model from file"""
        self.model.load_model(filepath)
        self.is_trained = True
        print(f"[checkmark.circle] Model loaded from {filepath}")

    def get_model_info(self) -> Dict:
        """Get model information"""
        return {
            "model_type": "XGBoost",
            "n_features": len(self.feature_names) if self.feature_names else 0,
            "n_estimators": self.model.n_estimators,
            "max_depth": self.model.max_depth,
            "learning_rate": self.model.learning_rate,
            "best_iteration": self.model.best_iteration if hasattr(self.model, "best_iteration") else None,
            "is_trained": self.is_trained,
        }

    def plot_feature_importance(self, top_n: int = 15, figsize: Tuple[int, int] = (10, 8)):
        """
        Plot feature importance

        Args:
            top_n: Number of top features to show
            figsize: Figure size
        """
        try:
            import matplotlib.pyplot as plt

            importance_df = self.get_feature_importance()
            top_features = importance_df.head(top_n)

            plt.figure(figsize=figsize)
            plt.barh(top_features["feature"], top_features["gain"])
            plt.xlabel("Importance (Gain)")
            plt.ylabel("Feature")
            plt.title(f"Top {top_n} Feature Importance (XGBoost)")
            plt.tight_layout()
            plt.show()

        except ImportError:
            print("[exclamationmark.triangle]  Matplotlib not installed for plotting")

    def plot_training_history(self):
        """Plot training history"""
        try:
            import matplotlib.pyplot as plt

            results = self.model.evals_result()

            epochs = range(len(results["validation_0"]["logloss"]))

            plt.figure(figsize=(10, 6))
            plt.plot(epochs, results["validation_0"]["logloss"], label="Train Loss")
            if "validation_1" in results:
                plt.plot(epochs, results["validation_1"]["logloss"], label="Validation Loss")

            if hasattr(self.model, "best_iteration"):
                plt.axvline(
                    self.model.best_iteration,
                    color="r",
                    linestyle="--",
                    label=f"Best Iteration ({self.model.best_iteration})",
                )

            plt.xlabel("Iteration")
            plt.ylabel("Log Loss")
            plt.title("XGBoost Training History")
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()

        except ImportError:
            print("[exclamationmark.triangle]  Matplotlib not installed for plotting")
