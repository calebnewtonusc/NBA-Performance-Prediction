"""
Ridge and Lasso Regression Models for Player Statistics Prediction

This module implements regularized regression models (Ridge and Lasso).

Usage:
    from src.models.ridge_lasso_regression import PlayerRidgeRegression, PlayerLassoRegression

    ridge = PlayerRidgeRegression()
    ridge.train(X_train, y_train)

    lasso = PlayerLassoRegression()
    lasso.train(X_train, y_train)
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge, Lasso, RidgeCV, LassoCV
from sklearn.model_selection import cross_val_score
from typing import Dict, Any, Optional
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class PlayerRidgeRegression:
    """Ridge Regression (L2 regularization) for player statistics prediction"""

    def __init__(self, random_state: int = 42):
        """
        Initialize Ridge regression model

        Args:
            random_state: Random seed for reproducibility
        """
        self.random_state = random_state
        self.model = None
        self.best_alpha = None
        self.feature_importance = None
        self.feature_names = None

    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: Optional[pd.DataFrame] = None,
        y_val: Optional[pd.Series] = None,
        tune_alpha: bool = True
    ) -> Dict[str, Any]:
        """
        Train Ridge regression model

        Args:
            X_train: Training features
            y_train: Training target
            X_val: Validation features (optional)
            y_val: Validation target (optional)
            tune_alpha: Whether to tune alpha parameter

        Returns:
            Dictionary with training metrics
        """
        logger.info("Training Ridge Regression model...")

        self.feature_names = X_train.columns.tolist()

        if tune_alpha:
            logger.info("Tuning alpha parameter...")
            alphas = np.logspace(-3, 3, 50)
            self.model = RidgeCV(alphas=alphas, cv=5)
            self.model.fit(X_train, y_train)
            self.best_alpha = self.model.alpha_
            logger.info(f"Best alpha: {self.best_alpha:.4f}")
        else:
            self.model = Ridge(alpha=1.0, random_state=self.random_state)
            self.model.fit(X_train, y_train)
            self.best_alpha = 1.0

        # Calculate feature importance
        self.feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'coefficient': self.model.coef_,
            'abs_coefficient': np.abs(self.model.coef_)
        }).sort_values('abs_coefficient', ascending=False)

        # Training metrics
        train_score = self.model.score(X_train, y_train)
        y_pred_train = self.model.predict(X_train)

        from sklearn.metrics import mean_absolute_error, mean_squared_error

        metrics = {
            'train_r2': train_score,
            'train_mae': mean_absolute_error(y_train, y_pred_train),
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
            'best_alpha': self.best_alpha
        }

        if X_val is not None and y_val is not None:
            val_score = self.model.score(X_val, y_val)
            y_pred_val = self.model.predict(X_val)

            metrics['val_r2'] = val_score
            metrics['val_mae'] = mean_absolute_error(y_val, y_pred_val)
            metrics['val_rmse'] = np.sqrt(mean_squared_error(y_val, y_pred_val))

            logger.info(f"Validation R²: {val_score:.4f}, MAE: {metrics['val_mae']:.2f}")

        logger.info(f"Training complete. Train R²: {train_score:.4f}, MAE: {metrics['train_mae']:.2f}")

        return metrics

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not trained yet. Call train() first.")
        return self.model.predict(X)

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """Evaluate model performance"""
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

        predictions = self.predict(X_test)

        metrics = {
            'r2': r2_score(y_test, predictions),
            'mae': mean_absolute_error(y_test, predictions),
            'mse': mean_squared_error(y_test, predictions),
            'rmse': np.sqrt(mean_squared_error(y_test, predictions))
        }

        logger.info(f"Test R²: {metrics['r2']:.4f}, MAE: {metrics['mae']:.2f}")

        return metrics

    def get_feature_importance(self, top_n: int = 10) -> pd.DataFrame:
        """Get top N most important features"""
        if self.feature_importance is None:
            raise ValueError("Model not trained yet. Call train() first.")
        return self.feature_importance.head(top_n)

    def plot_regularization_path(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        save_path: Optional[str] = None
    ):
        """
        Plot regularization path showing coefficient shrinkage

        Args:
            X: Features
            y: Target
            save_path: Optional path to save figure
        """
        alphas = np.logspace(-3, 3, 100)
        coefs = []

        for alpha in alphas:
            ridge = Ridge(alpha=alpha)
            ridge.fit(X, y)
            coefs.append(ridge.coef_)

        plt.figure(figsize=(12, 6))
        plt.plot(alphas, coefs)
        plt.xscale('log')
        plt.xlabel('Alpha (regularization strength)')
        plt.ylabel('Coefficients')
        plt.title('Ridge Regression: Regularization Path')
        plt.axvline(x=self.best_alpha, color='r', linestyle='--', label=f'Best Alpha: {self.best_alpha:.4f}')
        plt.legend()
        plt.grid(alpha=0.3)

        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            logger.info(f"Regularization path saved to {save_path}")

        plt.tight_layout()
        return plt.gcf()

    def save(self, filepath: str):
        """Save model to disk"""
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")

        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'feature_importance': self.feature_importance,
            'best_alpha': self.best_alpha
        }

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

        logger.info(f"Model saved to {filepath}")

    def load(self, filepath: str):
        """Load model from disk"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)

        self.model = model_data['model']
        self.feature_names = model_data['feature_names']
        self.feature_importance = model_data['feature_importance']
        self.best_alpha = model_data.get('best_alpha')

        logger.info(f"Model loaded from {filepath}")


class PlayerLassoRegression:
    """Lasso Regression (L1 regularization) for player statistics prediction"""

    def __init__(self, random_state: int = 42):
        """
        Initialize Lasso regression model

        Args:
            random_state: Random seed for reproducibility
        """
        self.random_state = random_state
        self.model = None
        self.best_alpha = None
        self.feature_importance = None
        self.feature_names = None
        self.selected_features = None

    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: Optional[pd.DataFrame] = None,
        y_val: Optional[pd.Series] = None,
        tune_alpha: bool = True
    ) -> Dict[str, Any]:
        """
        Train Lasso regression model

        Args:
            X_train: Training features
            y_train: Training target
            X_val: Validation features (optional)
            y_val: Validation target (optional)
            tune_alpha: Whether to tune alpha parameter

        Returns:
            Dictionary with training metrics
        """
        logger.info("Training Lasso Regression model...")

        self.feature_names = X_train.columns.tolist()

        if tune_alpha:
            logger.info("Tuning alpha parameter...")
            alphas = np.logspace(-3, 1, 50)
            self.model = LassoCV(alphas=alphas, cv=5, random_state=self.random_state, max_iter=10000)
            self.model.fit(X_train, y_train)
            self.best_alpha = self.model.alpha_
            logger.info(f"Best alpha: {self.best_alpha:.4f}")
        else:
            self.model = Lasso(alpha=1.0, random_state=self.random_state, max_iter=10000)
            self.model.fit(X_train, y_train)
            self.best_alpha = 1.0

        # Calculate feature importance
        self.feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'coefficient': self.model.coef_,
            'abs_coefficient': np.abs(self.model.coef_)
        }).sort_values('abs_coefficient', ascending=False)

        # Selected features (non-zero coefficients)
        self.selected_features = [
            f for f, c in zip(self.feature_names, self.model.coef_) if c != 0
        ]

        # Training metrics
        train_score = self.model.score(X_train, y_train)
        y_pred_train = self.model.predict(X_train)

        from sklearn.metrics import mean_absolute_error, mean_squared_error

        metrics = {
            'train_r2': train_score,
            'train_mae': mean_absolute_error(y_train, y_pred_train),
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
            'best_alpha': self.best_alpha,
            'n_selected_features': len(self.selected_features),
            'n_total_features': len(self.feature_names)
        }

        if X_val is not None and y_val is not None:
            val_score = self.model.score(X_val, y_val)
            y_pred_val = self.model.predict(X_val)

            metrics['val_r2'] = val_score
            metrics['val_mae'] = mean_absolute_error(y_val, y_pred_val)
            metrics['val_rmse'] = np.sqrt(mean_squared_error(y_val, y_pred_val))

            logger.info(f"Validation R²: {val_score:.4f}, MAE: {metrics['val_mae']:.2f}")

        logger.info(f"Training complete. Train R²: {train_score:.4f}, MAE: {metrics['train_mae']:.2f}")
        logger.info(f"Selected {len(self.selected_features)}/{len(self.feature_names)} features")

        return metrics

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not trained yet. Call train() first.")
        return self.model.predict(X)

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """Evaluate model performance"""
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

        predictions = self.predict(X_test)

        metrics = {
            'r2': r2_score(y_test, predictions),
            'mae': mean_absolute_error(y_test, predictions),
            'mse': mean_squared_error(y_test, predictions),
            'rmse': np.sqrt(mean_squared_error(y_test, predictions))
        }

        logger.info(f"Test R²: {metrics['r2']:.4f}, MAE: {metrics['mae']:.2f}")

        return metrics

    def get_selected_features(self) -> list:
        """Get list of selected features (non-zero coefficients)"""
        if self.selected_features is None:
            raise ValueError("Model not trained yet. Call train() first.")
        return self.selected_features

    def get_feature_importance(self, top_n: int = 10) -> pd.DataFrame:
        """Get top N most important features"""
        if self.feature_importance is None:
            raise ValueError("Model not trained yet. Call train() first.")
        # Only show non-zero coefficients
        return self.feature_importance[self.feature_importance['abs_coefficient'] > 0].head(top_n)

    def save(self, filepath: str):
        """Save model to disk"""
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")

        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'feature_importance': self.feature_importance,
            'best_alpha': self.best_alpha,
            'selected_features': self.selected_features
        }

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

        logger.info(f"Model saved to {filepath}")

    def load(self, filepath: str):
        """Load model from disk"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)

        self.model = model_data['model']
        self.feature_names = model_data['feature_names']
        self.feature_importance = model_data['feature_importance']
        self.best_alpha = model_data.get('best_alpha')
        self.selected_features = model_data.get('selected_features')

        logger.info(f"Model loaded from {filepath}")


# Example usage
if __name__ == "__main__":
    print("Ridge and Lasso Regression Models - Ready for training!")
    print("Load your dataset and call train() to build the models")
