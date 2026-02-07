"""
Load Testing Script for NBA Prediction API

Tests API performance under load using locust
"""

from locust import HttpUser, task, between
import random
import json


class NBAAPIUser(HttpUser):
    """Simulated user for load testing"""

    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    token = None

    def on_start(self):
        """Login and get token when user starts"""
        response = self.client.post("/api/v1/auth/login", json={
            "username": "admin",
            "password": "admin"
        })
        if response.status_code == 200:
            self.token = response.json()["access_token"]

    @task(5)  # Weight: 5 (most common)
    def predict_game_simple(self):
        """Test simple game prediction"""
        teams = ["BOS", "LAL", "GSW", "MIA", "DEN", "PHX", "MIL", "PHI"]
        home = random.choice(teams)
        away = random.choice([t for t in teams if t != home])

        self.client.post(
            "/api/v1/predict/simple",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "home_team": home,
                "away_team": away,
                "model_type": random.choice(["logistic", "tree", "forest"])
            },
            name="/api/v1/predict/simple"
        )

    @task(3)  # Weight: 3
    def predict_player(self):
        """Test player prediction"""
        self.client.post(
            "/api/v1/predict/player",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "player_avg_points": random.uniform(15, 35),
                "player_avg_rebounds": random.uniform(3, 12),
                "player_avg_assists": random.uniform(2, 10),
                "player_games_played": random.randint(20, 70),
                "team_win_pct": random.uniform(0.3, 0.8),
                "opponent_def_rating": random.uniform(105, 120),
                "is_home": random.choice([0, 1]),
                "rest_days": random.randint(0, 5)
            },
            name="/api/v1/predict/player"
        )

    @task(2)  # Weight: 2
    def compare_models(self):
        """Test model comparison"""
        teams = ["BOS", "LAL", "GSW", "MIA"]
        home = random.choice(teams)
        away = random.choice([t for t in teams if t != home])

        self.client.post(
            "/api/v1/predict/compare",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "home_team": home,
                "away_team": away
            },
            name="/api/v1/predict/compare"
        )

    @task(1)  # Weight: 1 (less common)
    def list_models(self):
        """Test model listing"""
        self.client.get(
            "/api/v1/models",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/api/v1/models"
        )

    @task(10)  # Weight: 10 (very common)
    def health_check(self):
        """Test health endpoint"""
        self.client.get("/api/v1/health", name="/api/v1/health")

    @task(2)  # Weight: 2
    def get_metrics(self):
        """Test metrics endpoint"""
        self.client.get(
            "/api/v1/metrics",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/api/v1/metrics"
        )


# Run with:
# locust -f tests/load_test.py --host=http://localhost:8000

# Or for headless mode:
# locust -f tests/load_test.py --host=http://localhost:8000 \
#        --users 100 --spawn-rate 10 --run-time 60s --headless
