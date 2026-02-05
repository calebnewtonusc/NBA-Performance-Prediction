"""
Decision Tree Model for Game Outcome Prediction

This module implements decision tree classifier for predicting NBA game winners.

Usage:
    from src.models.decision_tree_model import GameDecisionTree

    model = GameDecisionTree()
    model.train(X_train, y_train)
    predictions = model.predict(X_test)
"""

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.model_selection import GridSearchCV, cross_val_score
from typing import Dict, Any, Optional
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class GameDecisionTree:
    """Decision Tree model for game outcome prediction"""

    def __init__(self, random_state: int = 42):
        """
        Initialize the decision tree model

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
        Train the decision tree model

        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features (optional)
            y_val: Validation labels (optional)
            tune_hyperparameters: Whether to perform hyperparameter tuning

        Returns:
            Dictionary with training metrics
        """
        logger.info("Training Decision Tree model...")

        self.feature_names = X_train.columns.tolist()

        if tune_hyperparameters:
            logger.info("Performing hyperparameter tuning...")
            self.model = self._tune_hyperparameters(X_train, y_train)
        else:
            self.model = DecisionTreeClassifier(
                random_state=self.random_state,
                max_depth=10
            )
            self.model.fit(X_train, y_train)

        # Calculate feature importance
        self.feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

        # Training metrics
        train_score = self.model.score(X_train, y_train)
        metrics = {
            'train_accuracy': train_score,
            'best_params': self.best_params,
            'tree_depth': self.model.get_depth(),
            'n_leaves': self.model.get_n_leaves()
        }

        if X_val is not None and y_val is not None:
            val_score = self.model.score(X_val, y_val)
            metrics['val_accuracy'] = val_score
            logger.info(f"Validation accuracy: {val_score:.4f}")

        logger.info(f"Training complete. Train accuracy: {train_score:.4f}")
        logger.info(f"Tree depth: {metrics['tree_depth']}, Number of leaves: {metrics['n_leaves']}")

        return metrics

    def _tune_hyperparameters(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series
    ) -> DecisionTreeClassifier:
        """
        Tune hyperparameters using GridSearchCV

        Args:
            X_train: Training features
            y_train: Training labels

        Returns:
            Best model from grid search
        """
        param_grid = {
            'max_depth': [3, 5, 7, 10, 15, 20, None],
            'min_samples_split': [2, 5, 10, 20],
            'min_samples_leaf': [1, 2, 4, 8],
            'criterion': ['gini', 'entropy']
        }

        grid_search = GridSearchCV(
            DecisionTreeClassifier(random_state=self.random_state),
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

    def visualize_tree(
        self,
        max_depth: int = 3,
        figsize: tuple = (20, 10),
        save_path: Optional[str] = None
    ):
        """
        Visualize the decision tree

        Args:
            max_depth: Maximum depth to visualize (for readability)
            figsize: Figure size
            save_path: Optional path to save the figure
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train() first.")

        plt.figure(figsize=figsize)
        plot_tree(
            self.model,
            max_depth=max_depth,
            feature_names=self.feature_names,
            class_names=['Away Win', 'Home Win'],
            filled=True,
            rounded=True,
            fontsize=10
        )
        plt.title(f"Decision Tree (showing depth up to {max_depth})")

        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            logger.info(f"Tree visualization saved to {save_path}")

        plt.tight_layout()
        return plt.gcf()

    def get_tree_rules(self, max_depth: int = 5) -> str:
        """
        Get text representation of tree rules

        Args:
            max_depth: Maximum depth to display

        Returns:
            String with tree rules
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train() first.")

        tree_rules = export_text(
            self.model,
            feature_names=self.feature_names,
            max_depth=max_depth
        )

        return tree_rules

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
    print("Decision Tree Model - Ready for training!")
    print("Load your dataset and call train() to build the model")
