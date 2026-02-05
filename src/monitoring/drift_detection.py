"""
Model Monitoring and Drift Detection

Detects data drift and model performance degradation in production
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass, asdict


@dataclass
class DriftReport:
    """Drift detection report"""

    timestamp: str
    drift_detected: bool
    drift_score: float
    drift_threshold: float
    features_with_drift: List[str]
    drift_scores_by_feature: Dict[str, float]
    recommendation: str


class DataDriftDetector:
    """Detect data drift in features"""

    def __init__(self, threshold: float = 0.1):
        """
        Initialize drift detector

        Args:
            threshold: Drift threshold (0-1, higher = more tolerant)
        """
        self.threshold = threshold
        self.reference_stats: Optional[Dict] = None

    def fit_reference(self, X: pd.DataFrame):
        """
        Fit reference distribution from training data

        Args:
            X: Reference feature data
        """
        self.reference_stats = {
            "mean": X.mean().to_dict(),
            "std": X.std().to_dict(),
            "min": X.min().to_dict(),
            "max": X.max().to_dict(),
            "quantiles": {
                "25%": X.quantile(0.25).to_dict(),
                "50%": X.quantile(0.50).to_dict(),
                "75%": X.quantile(0.75).to_dict(),
            },
        }
        print("✅ Reference distribution fitted")

    def detect_drift(self, X: pd.DataFrame) -> DriftReport:
        """
        Detect drift in new data

        Args:
            X: New feature data

        Returns:
            Drift report
        """
        if self.reference_stats is None:
            raise ValueError("Must fit reference distribution first")

        drift_scores = {}
        features_with_drift = []

        # Calculate drift for each feature
        for feature in X.columns:
            if feature not in self.reference_stats["mean"]:
                continue

            # Calculate KS statistic (distribution difference)
            drift_score = self._calculate_ks_statistic(X[feature], feature)
            drift_scores[feature] = drift_score

            if drift_score > self.threshold:
                features_with_drift.append(feature)

        # Overall drift score (max across features)
        overall_drift_score = max(drift_scores.values()) if drift_scores else 0.0
        drift_detected = overall_drift_score > self.threshold

        # Recommendation
        if drift_detected:
            recommendation = (
                f"⚠️  Data drift detected in {len(features_with_drift)} features. "
                f"Consider retraining the model with recent data."
            )
        else:
            recommendation = "✅ No significant data drift detected. Model is stable."

        return DriftReport(
            timestamp=datetime.now(timezone.utc).isoformat(),
            drift_detected=drift_detected,
            drift_score=overall_drift_score,
            drift_threshold=self.threshold,
            features_with_drift=features_with_drift,
            drift_scores_by_feature=drift_scores,
            recommendation=recommendation,
        )

    def _calculate_ks_statistic(self, data: pd.Series, feature_name: str) -> float:
        """
        Calculate Kolmogorov-Smirnov statistic for drift detection

        Args:
            data: New data for feature
            feature_name: Feature name

        Returns:
            KS statistic (0-1)
        """
        ref_mean = self.reference_stats["mean"][feature_name]
        ref_std = self.reference_stats["std"][feature_name]

        if ref_std == 0:
            return 0.0

        # Z-score normalization
        data_normalized = (data - data.mean()) / (data.std() + 1e-10)
        ref_normalized = 0.0  # Reference is normalized to mean=0

        # Simple approximation of KS statistic
        # In production, use scipy.stats.ks_2samp for accurate calculation
        mean_diff = abs(data_normalized.mean() - ref_normalized)
        std_diff = abs((data.std() - ref_std) / (ref_std + 1e-10))

        ks_approx = (mean_diff + std_diff) / 2
        return min(ks_approx, 1.0)


class ModelPerformanceMonitor:
    """Monitor model performance in production"""

    def __init__(self, window_size: int = 100):
        """
        Initialize performance monitor

        Args:
            window_size: Number of recent predictions to monitor
        """
        self.window_size = window_size
        self.predictions_history: List[Dict] = []
        self.baseline_accuracy: Optional[float] = None

    def set_baseline(self, accuracy: float):
        """Set baseline accuracy from training"""
        self.baseline_accuracy = accuracy
        print(f"✅ Baseline accuracy set: {accuracy:.4f}")

    def record_prediction(
        self, prediction: int, actual: int, confidence: float, timestamp: Optional[str] = None
    ):
        """
        Record a prediction for monitoring

        Args:
            prediction: Predicted class
            actual: Actual class
            confidence: Prediction confidence
            timestamp: Timestamp of prediction
        """
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).isoformat()

        self.predictions_history.append(
            {
                "prediction": prediction,
                "actual": actual,
                "correct": prediction == actual,
                "confidence": confidence,
                "timestamp": timestamp,
            }
        )

        # Keep only recent predictions
        if len(self.predictions_history) > self.window_size * 2:
            self.predictions_history = self.predictions_history[-self.window_size :]

    def get_recent_performance(self, n: Optional[int] = None) -> Dict:
        """
        Get performance metrics for recent predictions

        Args:
            n: Number of recent predictions to analyze (default: window_size)

        Returns:
            Performance metrics
        """
        n = n or self.window_size

        if len(self.predictions_history) == 0:
            return {
                "error": "No predictions recorded",
                "sample_size": 0,
            }

        recent = self.predictions_history[-n:]

        correct_predictions = sum(1 for p in recent if p["correct"])
        accuracy = correct_predictions / len(recent)
        avg_confidence = np.mean([p["confidence"] for p in recent])

        # Calculate degradation if baseline exists
        degradation = None
        if self.baseline_accuracy is not None:
            degradation = self.baseline_accuracy - accuracy

        return {
            "sample_size": len(recent),
            "accuracy": accuracy,
            "average_confidence": avg_confidence,
            "baseline_accuracy": self.baseline_accuracy,
            "accuracy_degradation": degradation,
            "alerts": self._generate_alerts(accuracy, degradation),
        }

    def _generate_alerts(
        self, current_accuracy: float, degradation: Optional[float]
    ) -> List[str]:
        """Generate performance alerts"""
        alerts = []

        if degradation is not None:
            if degradation > 0.1:
                alerts.append("🚨 CRITICAL: Accuracy degraded by >10%")
            elif degradation > 0.05:
                alerts.append("⚠️  WARNING: Accuracy degraded by >5%")

        if current_accuracy < 0.5:
            alerts.append("🚨 CRITICAL: Accuracy below 50%")
        elif current_accuracy < 0.6:
            alerts.append("⚠️  WARNING: Accuracy below 60%")

        if not alerts:
            alerts.append("✅ Performance is stable")

        return alerts

    def get_performance_trends(self, bin_size: int = 10) -> Dict:
        """
        Get performance trends over time

        Args:
            bin_size: Number of predictions per bin

        Returns:
            Trend data
        """
        if len(self.predictions_history) < bin_size:
            return {"error": "Not enough data for trend analysis"}

        bins = []
        for i in range(0, len(self.predictions_history), bin_size):
            chunk = self.predictions_history[i : i + bin_size]
            if len(chunk) < bin_size // 2:
                continue

            bin_accuracy = sum(1 for p in chunk if p["correct"]) / len(chunk)
            bin_confidence = np.mean([p["confidence"] for p in chunk])

            bins.append(
                {
                    "bin_index": len(bins),
                    "start_time": chunk[0]["timestamp"],
                    "end_time": chunk[-1]["timestamp"],
                    "accuracy": bin_accuracy,
                    "confidence": bin_confidence,
                    "sample_size": len(chunk),
                }
            )

        return {
            "bins": bins,
            "total_bins": len(bins),
            "trend": self._calculate_trend([b["accuracy"] for b in bins]),
        }

    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction"""
        if len(values) < 2:
            return "stable"

        first_half = np.mean(values[: len(values) // 2])
        second_half = np.mean(values[len(values) // 2 :])

        diff = second_half - first_half

        if diff > 0.05:
            return "improving"
        elif diff < -0.05:
            return "degrading"
        else:
            return "stable"


class AlertManager:
    """Manage and send alerts for model monitoring"""

    def __init__(self):
        """Initialize alert manager"""
        self.alerts_history: List[Dict] = []

    def check_and_alert(
        self, drift_report: DriftReport, performance_metrics: Dict
    ) -> List[Dict]:
        """
        Check conditions and generate alerts

        Args:
            drift_report: Drift detection report
            performance_metrics: Performance metrics

        Returns:
            List of alerts
        """
        alerts = []
        timestamp = datetime.now(timezone.utc).isoformat()

        # Drift alerts
        if drift_report.drift_detected:
            alerts.append(
                {
                    "timestamp": timestamp,
                    "severity": "warning",
                    "type": "data_drift",
                    "message": f"Data drift detected in {len(drift_report.features_with_drift)} features",
                    "details": drift_report.recommendation,
                }
            )

        # Performance alerts
        if "alerts" in performance_metrics:
            for alert_msg in performance_metrics["alerts"]:
                if "CRITICAL" in alert_msg:
                    severity = "critical"
                elif "WARNING" in alert_msg:
                    severity = "warning"
                else:
                    severity = "info"

                alerts.append(
                    {
                        "timestamp": timestamp,
                        "severity": severity,
                        "type": "performance",
                        "message": alert_msg,
                        "details": performance_metrics,
                    }
                )

        # Store alerts
        self.alerts_history.extend(alerts)

        return alerts

    def get_recent_alerts(self, hours: int = 24) -> List[Dict]:
        """Get alerts from last N hours"""
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        cutoff_str = cutoff_time.isoformat()

        return [a for a in self.alerts_history if a["timestamp"] >= cutoff_str]

    def clear_old_alerts(self, days: int = 30):
        """Clear alerts older than N days"""
        cutoff_time = datetime.now(timezone.utc) - timedelta(days=days)
        cutoff_str = cutoff_time.isoformat()

        self.alerts_history = [a for a in self.alerts_history if a["timestamp"] >= cutoff_str]
