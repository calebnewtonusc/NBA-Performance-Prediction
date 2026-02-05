"""
Multi-Output Regression for Player Statistics Prediction

Predict multiple statistics simultaneously (e.g., points, rebounds, assists).

Usage:
    from src.models.multi_output_regression import PlayerMultiOutputRegression

    model = PlayerMultiOutputRegression()
    model.train(X_train, y_train_multi)  # y_train_multi has multiple columns
    predictions = model.predict(X_test)
"""

import numpy as np
import pandas as pd
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from typing import Dict, Any, Optional, List
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class PlayerMultiOutputRegression:
    """Multi-output regression for predicting multiple player statistics"""

    def __init__(self, base_estimator: str = "ridge", random_state: int = 42):
        """
        Initialize multi-output regression model

        Args:
            base_estimator: Base estimator to use ('ridge' or 'random_forest')
            random_state: Random seed for reproducibility
        """
        self.base_estimator_name = base_estimator
        self.random_state = random_state
        self.model = None
        self.feature_names = None
        self.target_names = None

    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.DataFrame,  # Multi-output target
        X_val: Optional[pd.DataFrame] = None,
        y_val: Optional[pd.DataFrame] = None
    ) -> Dict[str, Any]:
        """
        Train multi-output regression model

        Args:
            X_train: Training features
            y_train: Training targets (DataFrame with multiple columns)
            X_val: Validation features (optional)
            y_val: Validation targets (optional)

        Returns:
            Dictionary with training metrics
        """
        logger.info("Training Multi-Output Regression model...")

        self.feature_names = X_train.columns.tolist()
        self.target_names = y_train.columns.tolist()

        logger.info(f"Predicting {len(self.target_names)} outputs: {self.target_names}")

        # Create base estimator
        if self.base_estimator_name == "ridge":
            base_estimator = Ridge(alpha=1.0, random_state=self.random_state)
        elif self.base_estimator_name == "random_forest":
            base_estimator = RandomForestRegressor(
                n_estimators=100,
                random_state=self.random_state,
                n_jobs=-1
            )
        else:
            raise ValueError(f"Unknown base estimator: {self.base_estimator_name}")

        # Create multi-output model
        self.model = MultiOutputRegressor(base_estimator)
        self.model.fit(X_train, y_train)

        # Calculate metrics for each output
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

        y_pred_train = self.model.predict(X_train)

        metrics = {
            'base_estimator': self.base_estimator_name,
            'outputs': {}
        }

        # Calculate metrics for each target variable
        for i, target_name in enumerate(self.target_names):
            y_true_col = y_train.iloc[:, i]
            y_pred_col = y_pred_train[:, i]

            metrics['outputs'][target_name] = {
                'train_r2': r2_score(y_true_col, y_pred_col),
                'train_mae': mean_absolute_error(y_true_col, y_pred_col),
                'train_rmse': np.sqrt(mean_squared_error(y_true_col, y_pred_col))
            }

            logger.info(f"{target_name} - Train R²: {metrics['outputs'][target_name]['train_r2']:.4f}, "
                       f"MAE: {metrics['outputs'][target_name]['train_mae']:.2f}")

        # Validation metrics
        if X_val is not None and y_val is not None:
            y_pred_val = self.model.predict(X_val)

            for i, target_name in enumerate(self.target_names):
                y_true_col = y_val.iloc[:, i]
                y_pred_col = y_pred_val[:, i]

                metrics['outputs'][target_name]['val_r2'] = r2_score(y_true_col, y_pred_col)
                metrics['outputs'][target_name]['val_mae'] = mean_absolute_error(y_true_col, y_pred_col)
                metrics['outputs'][target_name]['val_rmse'] = np.sqrt(mean_squared_error(y_true_col, y_pred_col))

                logger.info(f"{target_name} - Val R²: {metrics['outputs'][target_name]['val_r2']:.4f}, "
                           f"MAE: {metrics['outputs'][target_name]['val_mae']:.2f}")

        logger.info("Training complete!")

        return metrics

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions

        Args:
            X: Features to predict

        Returns:
            Predictions array with shape (n_samples, n_outputs)
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train() first.")

        return self.model.predict(X)

    def predict_single_output(self, X: pd.DataFrame, output_name: str) -> np.ndarray:
        """
        Predict a single output

        Args:
            X: Features to predict
            output_name: Name of the output to predict

        Returns:
            Predictions for the specified output
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train() first.")

        if output_name not in self.target_names:
            raise ValueError(f"Output {output_name} not found. Available: {self.target_names}")

        predictions = self.model.predict(X)
        output_idx = self.target_names.index(output_name)

        return predictions[:, output_idx]

    def evaluate(
        self,
        X_test: pd.DataFrame,
        y_test: pd.DataFrame
    ) -> Dict[str, Dict[str, float]]:
        """
        Evaluate model performance for all outputs

        Args:
            X_test: Test features
            y_test: Test targets

        Returns:
            Dictionary with metrics for each output
        """
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

        predictions = self.predict(X_test)

        metrics = {}

        for i, target_name in enumerate(self.target_names):
            y_true_col = y_test.iloc[:, i]
            y_pred_col = predictions[:, i]

            metrics[target_name] = {
                'r2': r2_score(y_true_col, y_pred_col),
                'mae': mean_absolute_error(y_true_col, y_pred_col),
                'mse': mean_squared_error(y_true_col, y_pred_col),
                'rmse': np.sqrt(mean_squared_error(y_true_col, y_pred_col))
            }

            logger.info(f"{target_name} - Test R²: {metrics[target_name]['r2']:.4f}, "
                       f"MAE: {metrics[target_name]['mae']:.2f}")

        return metrics

    def analyze_output_correlation(
        self,
        X_test: pd.DataFrame,
        y_test: pd.DataFrame,
        save_path: Optional[str] = None
    ):
        """
        Analyze correlation between predicted outputs

        Args:
            X_test: Test features
            y_test: Test targets
            save_path: Optional path to save figure

        Returns:
            Figure with correlation heatmap
        """
        predictions = self.predict(X_test)
        pred_df = pd.DataFrame(predictions, columns=self.target_names)

        # Calculate correlation matrix
        corr = pred_df.corr()

        # Plot
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Predicted outputs correlation
        import seaborn as sns
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                   square=True, ax=axes[0], cbar_kws={'label': 'Correlation'})
        axes[0].set_title('Correlation: Predicted Outputs')

        # Actual outputs correlation
        corr_actual = y_test.corr()
        sns.heatmap(corr_actual, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                   square=True, ax=axes[1], cbar_kws={'label': 'Correlation'})
        axes[1].set_title('Correlation: Actual Outputs')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            logger.info(f"Correlation plot saved to {save_path}")

        return fig

    def plot_predictions_comparison(
        self,
        X_test: pd.DataFrame,
        y_test: pd.DataFrame,
        save_path: Optional[str] = None
    ):
        """
        Plot predictions vs actuals for all outputs

        Args:
            X_test: Test features
            y_test: Test targets
            save_path: Optional path to save figure

        Returns:
            Figure with comparison plots
        """
        predictions = self.predict(X_test)

        n_outputs = len(self.target_names)
        cols = min(3, n_outputs)
        rows = (n_outputs + cols - 1) // cols

        fig, axes = plt.subplots(rows, cols, figsize=(6 * cols, 5 * rows))

        if n_outputs == 1:
            axes = np.array([axes])

        axes = axes.flatten()

        for i, target_name in enumerate(self.target_names):
            ax = axes[i]

            y_true = y_test.iloc[:, i]
            y_pred = predictions[:, i]

            ax.scatter(y_true, y_pred, alpha=0.5, edgecolors='k')

            # Perfect prediction line
            min_val = min(y_true.min(), y_pred.min())
            max_val = max(y_true.max(), y_pred.max())
            ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)

            ax.set_xlabel('Actual')
            ax.set_ylabel('Predicted')
            ax.set_title(f'{target_name} Predictions')
            ax.grid(alpha=0.3)

            # Add R² to plot
            from sklearn.metrics import r2_score
            r2 = r2_score(y_true, y_pred)
            ax.text(0.05, 0.95, f'R² = {r2:.3f}', transform=ax.transAxes,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        # Hide extra subplots
        for i in range(n_outputs, len(axes)):
            axes[i].set_visible(False)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            logger.info(f"Comparison plot saved to {save_path}")

        return fig

    def save(self, filepath: str):
        """Save model to disk"""
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")

        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'target_names': self.target_names,
            'base_estimator_name': self.base_estimator_name
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
        self.target_names = model_data['target_names']
        self.base_estimator_name = model_data['base_estimator_name']

        logger.info(f"Model loaded from {filepath}")


# Example usage
if __name__ == "__main__":
    print("Multi-Output Regression Model - Ready for training!")
    print("Load your dataset and call train() with multiple target columns")
