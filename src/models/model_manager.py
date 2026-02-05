"""
Model Management and Retraining Pipeline

This module handles model versioning, retraining, and deployment.

Usage:
    from src.models.model_manager import ModelManager

    manager = ModelManager()
    manager.train_and_save_model(model, X_train, y_train, 'game_predictor', 'v1')
    model = manager.load_model('game_predictor', 'v1')
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import pickle
import pandas as pd
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ModelManager:
    """Manage model lifecycle: training, versioning, deployment"""

    def __init__(self, models_dir: str = "models"):
        """
        Initialize model manager

        Args:
            models_dir: Directory to store models
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def save_model(
        self,
        model: Any,
        name: str,
        version: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Save a model with metadata

        Args:
            model: Trained model object
            name: Model name
            version: Version string
            metadata: Additional metadata
        """
        model_path = self.models_dir / name / version
        model_path.mkdir(parents=True, exist_ok=True)

        # Save model
        model_file = model_path / "model.pkl"
        with open(model_file, 'wb') as f:
            pickle.dump(model, f)

        # Save metadata
        if metadata is None:
            metadata = {}

        metadata.update({
            'name': name,
            'version': version,
            'saved_at': datetime.now().isoformat(),
            'model_file': str(model_file)
        })

        metadata_file = model_path / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Model saved: {name} v{version} at {model_path}")

    def load_model(self, name: str, version: str) -> Any:
        """
        Load a model

        Args:
            name: Model name
            version: Version string

        Returns:
            Loaded model object
        """
        model_path = self.models_dir / name / version / "model.pkl"

        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")

        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        logger.info(f"Model loaded: {name} v{version}")

        return model

    def get_model_metadata(self, name: str, version: str) -> Dict[str, Any]:
        """
        Get model metadata

        Args:
            name: Model name
            version: Version string

        Returns:
            Metadata dictionary
        """
        metadata_path = self.models_dir / name / version / "metadata.json"

        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata not found: {metadata_path}")

        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        return metadata

    def list_models(self) -> Dict[str, list]:
        """
        List all available models

        Returns:
            Dictionary mapping model names to versions
        """
        models = {}

        for model_dir in self.models_dir.iterdir():
            if model_dir.is_dir():
                versions = [v.name for v in model_dir.iterdir() if v.is_dir()]
                if versions:
                    models[model_dir.name] = sorted(versions)

        return models

    def compare_versions(
        self,
        name: str,
        version1: str,
        version2: str
    ) -> Dict[str, Any]:
        """
        Compare two model versions

        Args:
            name: Model name
            version1: First version
            version2: Second version

        Returns:
            Comparison dictionary
        """
        meta1 = self.get_model_metadata(name, version1)
        meta2 = self.get_model_metadata(name, version2)

        comparison = {
            'model_name': name,
            'version1': version1,
            'version2': version2,
            'metadata1': meta1,
            'metadata2': meta2
        }

        return comparison

    def set_production_model(self, name: str, version: str):
        """
        Set a model version as production

        Args:
            name: Model name
            version: Version to promote to production
        """
        # Create symlink or marker file for production model
        prod_path = self.models_dir / name / "production"

        if prod_path.is_symlink() or prod_path.exists():
            prod_path.unlink()

        version_path = self.models_dir / name / version

        # Create symlink to production version
        try:
            prod_path.symlink_to(version_path, target_is_directory=True)
            logger.info(f"Set {name} v{version} as production model")
        except OSError:
            # Symlinks might not work on Windows, use marker file instead
            with open(self.models_dir / name / "production.txt", 'w') as f:
                f.write(version)
            logger.info(f"Set {name} v{version} as production model (marker file)")

    def get_production_model(self, name: str) -> Any:
        """
        Load the production model

        Args:
            name: Model name

        Returns:
            Production model object
        """
        prod_link = self.models_dir / name / "production"
        prod_marker = self.models_dir / name / "production.txt"

        if prod_link.exists():
            # Load from symlink
            model_file = prod_link / "model.pkl"
            with open(model_file, 'rb') as f:
                model = pickle.load(f)
            logger.info(f"Loaded production model: {name}")
            return model
        elif prod_marker.exists():
            # Load from marker file
            with open(prod_marker, 'r') as f:
                version = f.read().strip()
            return self.load_model(name, version)
        else:
            raise FileNotFoundError(f"No production model set for {name}")


class ModelRetrainer:
    """Automated model retraining pipeline"""

    def __init__(self, model_manager: ModelManager):
        """
        Initialize retrainer

        Args:
            model_manager: ModelManager instance
        """
        self.model_manager = model_manager

    def retrain_model(
        self,
        model_class: Any,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: pd.DataFrame,
        y_val: pd.Series,
        model_name: str,
        base_version: str
    ) -> tuple:
        """
        Retrain a model and create new version

        Args:
            model_class: Model class to instantiate
            X_train: Training features
            y_train: Training target
            X_val: Validation features
            y_val: Validation target
            model_name: Name of the model
            base_version: Base version string

        Returns:
            Tuple of (new_model, new_version, metrics)
        """
        logger.info(f"Retraining model: {model_name}")

        # Create new model instance
        new_model = model_class()

        # Train
        train_metrics = new_model.train(X_train, y_train, X_val, y_val)

        # Evaluate
        eval_metrics = new_model.evaluate(X_val, y_val)

        # Generate new version
        new_version = f"{base_version}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Save
        metadata = {
            'train_metrics': train_metrics,
            'eval_metrics': eval_metrics,
            'retrained_at': datetime.now().isoformat(),
            'base_version': base_version
        }

        self.model_manager.save_model(new_model, model_name, new_version, metadata)

        logger.info(f"Retrained model saved as {model_name} v{new_version}")

        return new_model, new_version, eval_metrics

    def compare_with_production(
        self,
        new_model: Any,
        model_name: str,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        metric: str = 'accuracy'
    ) -> Dict[str, Any]:
        """
        Compare new model with production model

        Args:
            new_model: Newly trained model
            model_name: Model name
            X_test: Test features
            y_test: Test target
            metric: Metric to compare

        Returns:
            Comparison results
        """
        try:
            prod_model = self.model_manager.get_production_model(model_name)

            # Evaluate both models
            new_metrics = new_model.evaluate(X_test, y_test)
            prod_metrics = prod_model.evaluate(X_test, y_test)

            comparison = {
                'production_metrics': prod_metrics,
                'new_model_metrics': new_metrics,
                'improvement': new_metrics[metric] - prod_metrics[metric],
                'better': new_metrics[metric] > prod_metrics[metric]
            }

            logger.info(f"Comparison - Production {metric}: {prod_metrics[metric]:.4f}, "
                       f"New {metric}: {new_metrics[metric]:.4f}")

            return comparison

        except FileNotFoundError:
            logger.warning("No production model found for comparison")
            return {'production_metrics': None, 'new_model_metrics': new_model.evaluate(X_test, y_test)}


# Example usage
if __name__ == "__main__":
    print("Model Manager - Ready for managing model lifecycle!")
