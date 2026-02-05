"""
Model Comparison Framework

Compare multiple models and select the best one.

Usage:
    from src.evaluation.model_comparison import ModelComparison

    comparison = ModelComparison()
    comparison.add_model('logistic', logistic_model, X_test, y_test)
    comparison.add_model('tree', tree_model, X_test, y_test)
    results = comparison.compare_all()
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import seaborn as sns
from src.evaluation.metrics import ClassificationMetrics, RegressionMetrics
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ModelComparison:
    """Compare multiple models and generate comparison reports"""

    def __init__(self, task_type: str = "classification"):
        """
        Initialize model comparison

        Args:
            task_type: 'classification' or 'regression'
        """
        self.task_type = task_type
        self.models = {}
        self.results = {}

        if task_type == "classification":
            self.metrics_calculator = ClassificationMetrics()
        else:
            self.metrics_calculator = RegressionMetrics()

    def add_model(
        self,
        name: str,
        model: Any,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ):
        """
        Add a model to the comparison

        Args:
            name: Model name
            model: Trained model object
            X_test: Test features
            y_test: Test labels/values
        """
        logger.info(f"Adding model: {name}")

        # Make predictions
        y_pred = model.predict(X_test)

        # Get probabilities for classification
        y_proba = None
        if self.task_type == "classification" and hasattr(model, 'predict_proba'):
            y_proba = model.predict_proba(X_test)[:, 1]

        # Calculate metrics
        if self.task_type == "classification":
            metrics = self.metrics_calculator.calculate_all_metrics(
                y_test.values, y_pred, y_proba
            )
        else:
            metrics = self.metrics_calculator.calculate_all_metrics(
                y_test.values, y_pred
            )

        self.models[name] = model
        self.results[name] = {
            'predictions': y_pred,
            'probabilities': y_proba,
            'metrics': metrics,
            'y_test': y_test.values
        }

        logger.info(f"Model {name} added successfully")

    def compare_all(self) -> pd.DataFrame:
        """
        Compare all models

        Returns:
            DataFrame with comparison results
        """
        if not self.results:
            raise ValueError("No models added. Use add_model() first.")

        logger.info("Comparing all models...")

        # Create comparison DataFrame
        comparison_data = []

        for name, result in self.results.items():
            metrics = result['metrics']
            row = {'model': name}
            row.update(metrics)
            comparison_data.append(row)

        comparison_df = pd.DataFrame(comparison_data)

        # Remove confusion_matrix for display
        if 'confusion_matrix' in comparison_df.columns:
            comparison_df = comparison_df.drop('confusion_matrix', axis=1)

        # Sort by best metric
        if self.task_type == "classification":
            comparison_df = comparison_df.sort_values('accuracy', ascending=False)
        else:
            comparison_df = comparison_df.sort_values('rmse', ascending=True)

        logger.info("Model comparison complete")

        return comparison_df

    def get_best_model(self, metric: str = None) -> tuple:
        """
        Get the best performing model

        Args:
            metric: Metric to use for comparison (default: accuracy for classification, rmse for regression)

        Returns:
            Tuple of (model_name, model_object)
        """
        if not self.results:
            raise ValueError("No models added. Use add_model() first.")

        if metric is None:
            metric = 'accuracy' if self.task_type == "classification" else 'rmse'

        # Find best model
        best_name = None
        best_value = None

        ascending = (metric in ['mae', 'mse', 'rmse', 'mape'])  # Lower is better for these

        for name, result in self.results.items():
            value = result['metrics'].get(metric)

            if value is None:
                continue

            if best_value is None:
                best_name = name
                best_value = value
            elif ascending and value < best_value:
                best_name = name
                best_value = value
            elif not ascending and value > best_value:
                best_name = name
                best_value = value

        logger.info(f"Best model: {best_name} ({metric}={best_value:.4f})")

        return best_name, self.models[best_name]

    def plot_comparison(
        self,
        metrics: List[str] = None,
        save_path: str = None
    ):
        """
        Plot comparison of models

        Args:
            metrics: List of metrics to plot (None = all)
            save_path: Optional path to save figure
        """
        if not self.results:
            raise ValueError("No models added. Use add_model() first.")

        comparison_df = self.compare_all()

        if metrics is None:
            # Default metrics
            if self.task_type == "classification":
                metrics = ['accuracy', 'precision', 'recall', 'f1_score']
            else:
                metrics = ['mae', 'rmse', 'r2']

        # Filter to available metrics
        metrics = [m for m in metrics if m in comparison_df.columns]

        n_metrics = len(metrics)
        fig, axes = plt.subplots(1, n_metrics, figsize=(5 * n_metrics, 5))

        if n_metrics == 1:
            axes = [axes]

        for i, metric in enumerate(metrics):
            ax = axes[i]

            values = comparison_df[metric].values
            models = comparison_df['model'].values

            bars = ax.bar(models, values, edgecolor='black', alpha=0.7)

            # Color best bar
            if metric in ['mae', 'mse', 'rmse', 'mape']:
                best_idx = values.argmin()
            else:
                best_idx = values.argmax()

            bars[best_idx].set_color('gold')
            bars[best_idx].set_edgecolor('darkgoldenrod')
            bars[best_idx].set_linewidth(2)

            ax.set_ylabel(metric.upper())
            ax.set_title(f'{metric.upper()} Comparison')
            ax.grid(axis='y', alpha=0.3)

            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            logger.info(f"Comparison plot saved to {save_path}")

        return fig

    def generate_report(self, save_path: str = None) -> str:
        """
        Generate detailed comparison report

        Args:
            save_path: Optional path to save report

        Returns:
            Report string
        """
        if not self.results:
            raise ValueError("No models added. Use add_model() first.")

        comparison_df = self.compare_all()

        report = "=" * 60 + "\n"
        report += "MODEL COMPARISON REPORT\n"
        report += "=" * 60 + "\n\n"

        report += f"Task Type: {self.task_type.upper()}\n"
        report += f"Number of Models: {len(self.results)}\n\n"

        report += "=" * 60 + "\n"
        report += "METRICS COMPARISON\n"
        report += "=" * 60 + "\n\n"

        report += comparison_df.to_string(index=False) + "\n\n"

        # Best model
        if self.task_type == "classification":
            best_name, _ = self.get_best_model('accuracy')
            report += f"Best Model (by accuracy): {best_name}\n"
        else:
            best_name, _ = self.get_best_model('rmse')
            report += f"Best Model (by RMSE): {best_name}\n"

        report += "\n" + "=" * 60 + "\n"
        report += "DETAILED RESULTS\n"
        report += "=" * 60 + "\n\n"

        for name, result in self.results.items():
            report += f"\n{name.upper()}\n"
            report += "-" * 40 + "\n"

            for metric, value in result['metrics'].items():
                if metric != 'confusion_matrix':
                    report += f"  {metric}: {value:.4f}\n" if isinstance(value, float) else f"  {metric}: {value}\n"

        if save_path:
            with open(save_path, 'w') as f:
                f.write(report)
            logger.info(f"Report saved to {save_path}")

        return report


# Example usage
if __name__ == "__main__":
    print("Model Comparison - Ready for use!")
    print("Add multiple models and compare their performance")
