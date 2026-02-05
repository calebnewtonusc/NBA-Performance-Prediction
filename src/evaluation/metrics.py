"""
Model Evaluation Metrics

This module provides comprehensive evaluation metrics for classification and regression models.

Usage:
    from src.evaluation.metrics import ClassificationMetrics, RegressionMetrics

    clf_metrics = ClassificationMetrics()
    results = clf_metrics.calculate_all_metrics(y_true, y_pred, y_proba)
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    mean_absolute_error, mean_squared_error, r2_score
)
from typing import Dict, Any, Optional
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ClassificationMetrics:
    """Calculate and visualize classification metrics"""

    def calculate_all_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_proba: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive classification metrics

        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_proba: Predicted probabilities (optional)

        Returns:
            Dictionary with all metrics
        """
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='binary'),
            'recall': recall_score(y_true, y_pred, average='binary'),
            'f1_score': f1_score(y_true, y_pred, average='binary'),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
        }

        if y_proba is not None:
            metrics['roc_auc'] = roc_auc_score(y_true, y_proba)

        return metrics

    def plot_confusion_matrix(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        labels: list = ['Away Win', 'Home Win'],
        save_path: Optional[str] = None
    ):
        """
        Plot confusion matrix

        Args:
            y_true: True labels
            y_pred: Predicted labels
            labels: Class labels
            save_path: Optional path to save figure
        """
        cm = confusion_matrix(y_true, y_pred)

        plt.figure(figsize=(8, 6))
        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=labels,
            yticklabels=labels
        )
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')

        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            logger.info(f"Confusion matrix saved to {save_path}")

        plt.tight_layout()
        return plt.gcf()

    def plot_roc_curve(
        self,
        y_true: np.ndarray,
        y_proba: np.ndarray,
        save_path: Optional[str] = None
    ):
        """
        Plot ROC curve

        Args:
            y_true: True labels
            y_proba: Predicted probabilities
            save_path: Optional path to save figure
        """
        from sklearn.metrics import roc_curve, auc

        fpr, tpr, thresholds = roc_curve(y_true, y_proba)
        roc_auc = auc(fpr, tpr)

        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)

        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            logger.info(f"ROC curve saved to {save_path}")

        plt.tight_layout()
        return plt.gcf()

    def print_classification_report(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        labels: list = ['Away Win', 'Home Win']
    ):
        """
        Print detailed classification report

        Args:
            y_true: True labels
            y_pred: Predicted labels
            labels: Class labels
        """
        report = classification_report(y_true, y_pred, target_names=labels)
        print("\nClassification Report:")
        print(report)


class RegressionMetrics:
    """Calculate and visualize regression metrics"""

    def calculate_all_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> Dict[str, float]:
        """
        Calculate comprehensive regression metrics

        Args:
            y_true: True values
            y_pred: Predicted values

        Returns:
            Dictionary with all metrics
        """
        metrics = {
            'mae': mean_absolute_error(y_true, y_pred),
            'mse': mean_squared_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'r2': r2_score(y_true, y_pred),
            'mape': self._calculate_mape(y_true, y_pred)
        }

        return metrics

    def _calculate_mape(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> float:
        """
        Calculate Mean Absolute Percentage Error

        Args:
            y_true: True values
            y_pred: Predicted values

        Returns:
            MAPE value
        """
        # Avoid division by zero
        mask = y_true != 0
        return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

    def plot_predictions_vs_actual(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        title: str = "Predictions vs Actual",
        save_path: Optional[str] = None
    ):
        """
        Plot predictions vs actual values

        Args:
            y_true: True values
            y_pred: Predicted values
            title: Plot title
            save_path: Optional path to save figure
        """
        plt.figure(figsize=(10, 6))

        # Scatter plot
        plt.scatter(y_true, y_pred, alpha=0.5, edgecolors='k')

        # Perfect prediction line
        min_val = min(y_true.min(), y_pred.min())
        max_val = max(y_true.max(), y_pred.max())
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')

        plt.xlabel('Actual Values')
        plt.ylabel('Predicted Values')
        plt.title(title)
        plt.legend()
        plt.grid(alpha=0.3)

        # Add metrics text
        metrics = self.calculate_all_metrics(y_true, y_pred)
        textstr = f"MAE: {metrics['mae']:.2f}\nRMSE: {metrics['rmse']:.2f}\nR²: {metrics['r2']:.3f}"
        plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            logger.info(f"Predictions plot saved to {save_path}")

        plt.tight_layout()
        return plt.gcf()

    def plot_residuals(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        save_path: Optional[str] = None
    ):
        """
        Plot residuals

        Args:
            y_true: True values
            y_pred: Predicted values
            save_path: Optional path to save figure
        """
        residuals = y_true - y_pred

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Residual plot
        axes[0].scatter(y_pred, residuals, alpha=0.5, edgecolors='k')
        axes[0].axhline(y=0, color='r', linestyle='--', lw=2)
        axes[0].set_xlabel('Predicted Values')
        axes[0].set_ylabel('Residuals')
        axes[0].set_title('Residual Plot')
        axes[0].grid(alpha=0.3)

        # Residual histogram
        axes[1].hist(residuals, bins=30, edgecolor='black', alpha=0.7)
        axes[1].axvline(x=0, color='r', linestyle='--', lw=2)
        axes[1].set_xlabel('Residuals')
        axes[1].set_ylabel('Frequency')
        axes[1].set_title('Residual Distribution')
        axes[1].grid(alpha=0.3)

        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            logger.info(f"Residual plots saved to {save_path}")

        plt.tight_layout()
        return fig


# Example usage
if __name__ == "__main__":
    print("Evaluation Metrics - Ready for use!")
    print("Import ClassificationMetrics or RegressionMetrics to evaluate your models")
