"""Prediction Service - Business Logic Layer"""

from typing import Dict, Any, List
from datetime import datetime, timezone
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class PredictionService:
    """Service for handling prediction business logic"""

    def __init__(self, model_manager, cache, nba_fetcher):
        self.model_manager = model_manager
        self.cache = cache
        self.nba_fetcher = nba_fetcher
        self.loaded_models = {}
        self.predictions_count = 0

    def load_model(self, model_name: str, version: str) -> Dict[str, Any]:
        """Load model if not cached"""
        key = f"{model_name}:{version}"

        if key not in self.loaded_models:
            model_data = self.model_manager.load_model(model_name, version)

            if isinstance(model_data, dict) and 'model' in model_data:
                self.loaded_models[key] = {
                    "model": model_data['model'],
                    "scaler": model_data.get('scaler'),
                    "loaded_at": datetime.now(timezone.utc).isoformat(),
                }
            else:
                self.loaded_models[key] = {
                    "model": model_data,
                    "scaler": None,
                    "loaded_at": datetime.now(timezone.utc).isoformat(),
                }

        self.loaded_models[key]["last_used"] = datetime.now(timezone.utc).isoformat()
        return self.loaded_models[key]

    def predict_game(
        self,
        features: Dict,
        model_name: str = "game_logistic",
        version: str = "v1",
        home_team: str = None,
        away_team: str = None
    ) -> Dict:
        """
        Predict game outcome

        Args:
            features: Game features dict
            model_name: Model to use
            version: Model version
            home_team: Home team name
            away_team: Away team name

        Returns:
            Prediction result dict
        """
        # Check cache
        cache_key = f"{model_name}:{version}:{str(features)}"
        cached = self.cache.get_cached_prediction(model_name, version, features)
        if cached:
            cached["cached"] = True
            cached["timestamp"] = datetime.now(timezone.utc).isoformat()
            return cached

        # Load model
        model_data = self.load_model(model_name, version)
        model = model_data["model"]
        scaler = model_data["scaler"]

        # Prepare features
        features_df = pd.DataFrame([features])

        # Scale if needed
        if scaler is not None:
            features_scaled = scaler.transform(features_df)
        else:
            features_scaled = features_df

        # Predict
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]

        # Format result
        winner = "home" if prediction == 1 else "away"
        confidence = probabilities[1] if prediction == 1 else probabilities[0]

        result = {
            "prediction": winner,
            "confidence": float(confidence),
            "home_win_probability": float(probabilities[1]),
            "away_win_probability": float(probabilities[0]),
            "home_team": home_team or "Unknown",
            "away_team": away_team or "Unknown",
            "model_used": f"{model_name}:{version}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cached": False
        }

        # Cache result
        self.cache.cache_prediction(model_name, version, features, result, ttl=300)

        self.predictions_count += 1
        return result

    def predict_player(self, features: Dict, model_name: str = "player_ridge", version: str = "v1") -> Dict:
        """
        Predict player stats

        Args:
            features: Player features dict
            model_name: Model to use
            version: Model version

        Returns:
            Player prediction result
        """
        # Load model
        model_data = self.load_model(model_name, version)
        model = model_data["model"]
        scaler = model_data["scaler"]

        # Prepare features
        features_df = pd.DataFrame([features])

        # Scale
        if scaler is not None:
            features_scaled = scaler.transform(features_df)
        else:
            features_scaled = features_df

        # Predict
        predicted_points = model.predict(features_scaled)[0]

        # Confidence interval (±15%)
        confidence_margin = predicted_points * 0.15
        confidence_low = max(0, predicted_points - confidence_margin)
        confidence_high = predicted_points + confidence_margin

        self.predictions_count += 1

        return {
            "predicted_points": float(predicted_points),
            "confidence_interval_low": float(confidence_low),
            "confidence_interval_high": float(confidence_high),
            "model_used": f"{model_name}:{version}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def predict_game_simple(self, home_team: str, away_team: str, model_type: str = "logistic") -> Dict:
        """
        Predict game with auto-fetched stats

        Args:
            home_team: Home team abbreviation
            away_team: Away team abbreviation
            model_type: Model type (logistic, tree, forest)

        Returns:
            Prediction result
        """
        # Fetch features
        features = self.nba_fetcher.get_game_features(home_team, away_team)

        # Map model type
        model_map = {
            "logistic": "game_logistic",
            "tree": "game_tree",
            "forest": "game_forest"
        }
        model_name = model_map.get(model_type, "game_logistic")

        return self.predict_game(features, model_name, "v1", home_team, away_team)

    def compare_models(self, home_team: str, away_team: str) -> Dict:
        """
        Compare predictions from multiple models

        Args:
            home_team: Home team abbreviation
            away_team: Away team abbreviation

        Returns:
            Comparison result with consensus
        """
        features = self.nba_fetcher.get_game_features(home_team, away_team)
        features_df = pd.DataFrame([features])

        models_to_compare = {
            "logistic_regression": "game_logistic",
            "decision_tree": "game_tree",
            "random_forest": "game_forest"
        }

        results = {}

        for model_name_display, model_name in models_to_compare.items():
            try:
                model_data = self.load_model(model_name, "v1")
                model = model_data["model"]
                scaler = model_data["scaler"]

                # Scale features
                if scaler is not None:
                    features_scaled = scaler.transform(features_df)
                else:
                    features_scaled = features_df

                # Predict
                prediction = model.predict(features_scaled)[0]
                probabilities = model.predict_proba(features_scaled)[0]

                winner = "home" if prediction == 1 else "away"
                confidence = probabilities[1] if prediction == 1 else probabilities[0]

                results[model_name_display] = {
                    "prediction": winner,
                    "confidence": float(confidence),
                    "home_win_probability": float(probabilities[1]),
                    "away_win_probability": float(probabilities[0])
                }
            except Exception as e:
                logger.error(f"Error with model {model_name}: {e}")
                results[model_name_display] = {"error": str(e)}

        # Calculate consensus
        home_votes = sum(1 for r in results.values() if r.get("prediction") == "home")
        away_votes = sum(1 for r in results.values() if r.get("prediction") == "away")
        consensus = "home" if home_votes > away_votes else "away"

        avg_confidence = np.mean([r.get("confidence", 0) for r in results.values()])

        return {
            "home_team": home_team,
            "away_team": away_team,
            "models": results,
            "consensus": {
                "prediction": consensus,
                "votes": {"home": home_votes, "away": away_votes},
                "average_confidence": float(avg_confidence)
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def batch_predict(self, games: List[Dict], model_name: str = "game_logistic", version: str = "v1") -> Dict:
        """
        Batch predict multiple games

        Args:
            games: List of game dicts with features
            model_name: Model to use
            version: Model version

        Returns:
            Batch prediction result
        """
        model_data = self.load_model(model_name, version)
        model = model_data["model"]
        scaler = model_data["scaler"]

        predictions = []
        for game in games:
            features_df = pd.DataFrame([game['features']])

            if scaler is not None:
                features_scaled = scaler.transform(features_df)
            else:
                features_scaled = features_df

            prediction = model.predict(features_scaled)[0]
            probabilities = model.predict_proba(features_scaled)[0]

            winner = "home" if prediction == 1 else "away"
            confidence = probabilities[1] if prediction == 1 else probabilities[0]

            predictions.append({
                "prediction": winner,
                "confidence": float(confidence),
                "home_win_probability": float(probabilities[1]),
                "away_win_probability": float(probabilities[0]),
                "home_team": game.get('home_team', 'Unknown'),
                "away_team": game.get('away_team', 'Unknown'),
            })

        self.predictions_count += len(predictions)

        return {
            "predictions": predictions,
            "total_games": len(predictions),
            "model_used": f"{model_name}:{version}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def get_stats(self) -> Dict:
        """Get service statistics"""
        return {
            "predictions_total": self.predictions_count,
            "models_loaded": len(self.loaded_models),
            "cache_stats": self.cache.get_stats() if self.cache else {}
        }
