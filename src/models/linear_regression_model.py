"""
Linear Regression Model for Player Statistics Prediction

This module implements linear regression for predicting player performance.

Usage:
    from src.models.linear_regression_model import PlayerLinearRegression

    model = PlayerLinearRegression()
    model.train(X_train, y_train)
    predictions = model.predict(X_test)
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from typing import Dict, Any, Optional
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class PlayerLinearRegression:
    """Linear Regression model for player statistics prediction"""

    def __init__(self):
        """Initialize the linear regression model"""
        self.model = None
        self.feature_importance = None
        self.feature_names = None

    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: Optional[pd.DataFrame] = None,
        y_val: Optional[pd.Series] = None
    ) -> Dict[str, Any]:
        """
        Train the linear regression model

        Args:
            X_train: Training features
            y_train: Training target
            X_val: Validation features (optional)
            y_val: Validation target (optional)

        Returns:
            Dictionary with training metrics
        """
        logger.info("Training Linear Regression model...")

        self.feature_names = X_train.columns.tolist()

        self.model = LinearRegression()
        self.model.fit(X_train, y_train)

        # Calculate feature importance (coefficient magnitudes)
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
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train))
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
        """
        Make predictions

        Args:
            X: Features to predict

        Returns:
            Predicted values
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train() first.")

        return self.model.predict(X)

    def evaluate(
        self,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> Dict[str, float]:
        """
        Evaluate model performance

        Args:
            X_test: Test features
            y_test: Test target

        Returns:
            Dictionary with evaluation metrics
        """
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

        predictions = self.predict(X_test)

        metrics = {
            'r2': r2_score(y_test, predictions),
            'mae': mean_absolute_error(y_test, predictions),
            'mse': mean_squared_error(y_test, predictions),
            'rmse': np.sqrt(mean_squared_error(y_test, predictions))
        }

        logger.info(f"Test R²: {metrics['r2']:.4f}")
        logger.info(f"Test MAE: {metrics['mae']:.2f}")
        logger.info(f"Test RMSE: {metrics['rmse']:.2f}")

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

    def analyze_residuals(
        self,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> Dict[str, Any]:
        """
        Analyze regression residuals

        Args:
            X_test: Test features
            y_test: Test target

        Returns:
            Dictionary with residual analysis
        """
        predictions = self.predict(X_test)
        residuals = y_test.values - predictions

        analysis = {
            'mean_residual': np.mean(residuals),
            'std_residual': np.std(residuals),
            'min_residual': np.min(residuals),
            'max_residual': np.max(residuals),
            'residuals': residuals
        }

        logger.info(f"Mean residual: {analysis['mean_residual']:.2f}")
        logger.info(f"Std residual: {analysis['std_residual']:.2f}")

        return analysis

    def check_assumptions(
        self,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        save_path: Optional[str] = None
    ):
        """
        Check linear regression assumptions

        Args:
            X_test: Test features
            y_test: Test target
            save_path: Optional path to save plots

        Returns:
            Figure with diagnostic plots
        """
        predictions = self.predict(X_test)
        residuals = y_test.values - predictions

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # 1. Residuals vs Fitted
        axes[0, 0].scatter(predictions, residuals, alpha=0.5)
        axes[0, 0].axhline(y=0, color='r', linestyle='--', lw=2)
        axes[0, 0].set_xlabel('Fitted Values')
        axes[0, 0].set_ylabel('Residuals')
        axes[0, 0].set_title('Residuals vs Fitted')
        axes[0, 0].grid(alpha=0.3)

        # 2. Normal Q-Q plot
        from scipy import stats
        stats.probplot(residuals, dist="norm", plot=axes[0, 1])
        axes[0, 1].set_title('Normal Q-Q Plot')
        axes[0, 1].grid(alpha=0.3)

        # 3. Scale-Location
        standardized_residuals = residuals / np.std(residuals)
        axes[1, 0].scatter(predictions, np.sqrt(np.abs(standardized_residuals)), alpha=0.5)
        axes[1, 0].set_xlabel('Fitted Values')
        axes[1, 0].set_ylabel('√|Standardized Residuals|')
        axes[1, 0].set_title('Scale-Location')
        axes[1, 0].grid(alpha=0.3)

        # 4. Residuals Histogram
        axes[1, 1].hist(residuals, bins=30, edgecolor='black', alpha=0.7)
        axes[1, 1].axvline(x=0, color='r', linestyle='--', lw=2)
        axes[1, 1].set_xlabel('Residuals')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].set_title('Residual Distribution')
        axes[1, 1].grid(alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            logger.info(f"Diagnostic plots saved to {save_path}")

        return fig

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
            y: Target
            cv: Number of folds

        Returns:
            Dictionary with cross-validation results
        """
        if self.model is None:
            self.model = LinearRegression()

        scores = cross_val_score(self.model, X, y, cv=cv, scoring='r2')

        results = {
            'mean_r2': scores.mean(),
            'std_r2': scores.std(),
            'all_scores': scores
        }

        logger.info(f"Cross-validation R²: {results['mean_r2']:.4f} (+/- {results['std_r2']:.4f})")

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
            'feature_importance': self.feature_importance
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

        logger.info(f"Model loaded from {filepath}")


# Example usage
if __name__ == "__main__":
    print("Linear Regression Model - Ready for training!")
    print("Load your dataset and call train() to build the model")
