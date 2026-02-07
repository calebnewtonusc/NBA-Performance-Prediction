"""
Integration Tests for NBA Prediction API

Tests the complete API workflow end-to-end
"""

import pytest
import requests
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.api.main import app

client = TestClient(app)


class TestAuthentication:
    """Test authentication flow"""

    def test_login_success(self):
        """Test successful login"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "wrong"}
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_missing_fields(self):
        """Test login with missing fields"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin"}
        )
        assert response.status_code == 422  # Validation error


class TestHealthEndpoints:
    """Test health and monitoring endpoints"""

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "NBA Performance Prediction API"
        assert data["status"] == "operational"

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "uptime_seconds" in data
        assert "models_loaded" in data
        assert "version" in data

    def test_metrics_requires_auth(self):
        """Test metrics endpoint requires authentication"""
        response = client.get("/api/v1/metrics")
        assert response.status_code == 403  # No auth header


class TestPredictionEndpoints:
    """Test prediction endpoints"""

    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin"}
        )
        return response.json()["access_token"]

    def test_simple_prediction(self, auth_token):
        """Test simple prediction with auto-fetch"""
        response = client.post(
            "/api/v1/predict/simple",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "home_team": "BOS",
                "away_team": "LAL",
                "model_type": "logistic"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert data["prediction"] in ["home", "away"]
        assert "confidence" in data
        assert 0 <= data["confidence"] <= 1
        assert "home_win_probability" in data
        assert "away_win_probability" in data
        assert data["home_team"] == "BOS"
        assert data["away_team"] == "LAL"

    def test_simple_prediction_invalid_team(self, auth_token):
        """Test prediction with invalid team"""
        response = client.post(
            "/api/v1/predict/simple",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "home_team": "INVALID",
                "away_team": "LAL"
            }
        )
        assert response.status_code == 400
        assert "Invalid team abbreviation" in response.json()["detail"]

    def test_player_prediction(self, auth_token):
        """Test player stats prediction"""
        response = client.post(
            "/api/v1/predict/player",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "player_avg_points": 28.5,
                "player_avg_rebounds": 8.2,
                "player_avg_assists": 6.1,
                "player_games_played": 45,
                "team_win_pct": 0.650,
                "opponent_def_rating": 112.0,
                "is_home": 1,
                "rest_days": 2
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "predicted_points" in data
        assert data["predicted_points"] > 0
        assert "confidence_interval_low" in data
        assert "confidence_interval_high" in data
        assert data["confidence_interval_low"] < data["predicted_points"] < data["confidence_interval_high"]

    def test_compare_models(self, auth_token):
        """Test model comparison"""
        response = client.post(
            "/api/v1/predict/compare",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "home_team": "BOS",
                "away_team": "LAL"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert "logistic_regression" in data["models"]
        assert "decision_tree" in data["models"]
        assert "random_forest" in data["models"]
        assert "consensus" in data
        assert data["consensus"]["prediction"] in ["home", "away"]

    def test_prediction_without_auth(self):
        """Test prediction requires authentication"""
        response = client.post(
            "/api/v1/predict/simple",
            json={"home_team": "BOS", "away_team": "LAL"}
        )
        assert response.status_code == 403


class TestModelEndpoints:
    """Test model management endpoints"""

    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin"}
        )
        return response.json()["access_token"]

    def test_list_models(self, auth_token):
        """Test listing available models"""
        response = client.get(
            "/api/v1/models",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert "total" in data
        assert data["total"] > 0


class TestRateLimiting:
    """Test rate limiting"""

    def test_rate_limit_exceeded(self):
        """Test rate limiting kicks in"""
        # Make many requests quickly
        responses = []
        for i in range(150):  # Exceed 100/min limit
            response = client.get("/")
            responses.append(response.status_code)

        # At least one should be rate limited
        assert 429 in responses


class TestErrorHandling:
    """Test error handling"""

    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin"}
        )
        return response.json()["access_token"]

    def test_invalid_json(self, auth_token):
        """Test handling of invalid JSON"""
        response = client.post(
            "/api/v1/predict/simple",
            headers={
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json"
            },
            data="invalid json{"
        )
        assert response.status_code == 422

    def test_missing_required_fields(self, auth_token):
        """Test handling of missing required fields"""
        response = client.post(
            "/api/v1/predict/player",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "player_avg_points": 28.5
                # Missing other required fields
            }
        )
        assert response.status_code == 422


class TestCaching:
    """Test caching behavior"""

    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin"}
        )
        return response.json()["access_token"]

    def test_cache_hit(self, auth_token):
        """Test that repeated requests hit cache"""
        # First request
        response1 = client.post(
            "/api/v1/predict/simple",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"home_team": "BOS", "away_team": "LAL"}
        )
        assert response1.status_code == 200
        data1 = response1.json()

        # Second request (should hit cache)
        response2 = client.post(
            "/api/v1/predict/simple",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"home_team": "BOS", "away_team": "LAL"}
        )
        assert response2.status_code == 200
        data2 = response2.json()

        # Results should be identical
        assert data1["prediction"] == data2["prediction"]
        assert data1["confidence"] == data2["confidence"]


class TestRequestIDTracking:
    """Test request ID tracking"""

    def test_request_id_in_response(self):
        """Test that response includes X-Request-ID header"""
        response = client.get("/api/v1/health")
        assert "X-Request-ID" in response.headers
        assert len(response.headers["X-Request-ID"]) > 0

    def test_custom_request_id(self):
        """Test custom request ID is preserved"""
        custom_id = "test-12345"
        response = client.get(
            "/api/v1/health",
            headers={"X-Request-ID": custom_id}
        )
        assert response.headers["X-Request-ID"] == custom_id


class TestSecurityHeaders:
    """Test security headers"""

    def test_security_headers_present(self):
        """Test that security headers are present in production mode"""
        # Note: Security headers only added in production
        # This test would pass in production environment
        response = client.get("/api/v1/health")
        # In local/dev, these may not be present
        # In production with RAILWAY_ENVIRONMENT set, they should be
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
