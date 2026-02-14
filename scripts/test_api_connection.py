#!/usr/bin/env python3
"""
Test API Connection

Usage:
    python scripts/test_api_connection.py
    python scripts/test_api_connection.py --url https://your-api.railway.app

Tests connectivity to the NBA Prediction API and verifies endpoints.
"""

import argparse
import sys
import requests
from typing import Dict, Any


def test_health_endpoint(base_url: str) -> bool:
    """Test the health check endpoint"""
    print(f"\n🔍 Testing health endpoint: {base_url}/api/health")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"[checkmark.circle] Health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Models loaded: {data.get('models_loaded')}")
            print(f"   Uptime: {data.get('uptime_seconds')}s")
            return True
        else:
            print(f"[xmark.circle] Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[xmark.circle] Health check failed: {e}")
        return False


def test_login(base_url: str, username: str, password: str) -> str:
    """Test login and return access token"""
    print(f"\n[lock.shield.fill] Testing login endpoint: {base_url}/api/auth/login")
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json={"username": username, "password": password},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"[checkmark.circle] Login successful")
            print(f"   Token type: {data.get('token_type')}")
            print(f"   Token (first 20 chars): {token[:20]}...")
            return token
        else:
            print(f"[xmark.circle] Login failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return ""
    except requests.exceptions.RequestException as e:
        print(f"[xmark.circle] Login failed: {e}")
        return ""


def test_models_endpoint(base_url: str, token: str) -> bool:
    """Test the models endpoint"""
    print(f"\n[chart.bar.fill] Testing models endpoint: {base_url}/api/models")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{base_url}/api/models", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"[checkmark.circle] Models endpoint accessible")
            print(f"   Available models: {data.get('models', [])}")
            print(f"   Models loaded: {len(data.get('loaded_models', []))}")
            return True
        else:
            print(f"[xmark.circle] Models endpoint failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[xmark.circle] Models endpoint failed: {e}")
        return False


def test_prediction(base_url: str, token: str) -> bool:
    """Test the prediction endpoint with sample data"""
    print(f"\n[target] Testing prediction endpoint: {base_url}/api/predict")

    # Sample prediction data
    prediction_data = {
        "home_team": "Lakers",
        "away_team": "Warriors",
        "features": {
            "home_win_pct": 0.650,
            "away_win_pct": 0.550,
            "home_avg_points": 112.5,
            "away_avg_points": 108.3,
            "home_avg_allowed": 105.2,
            "away_avg_allowed": 107.8,
            "home_point_diff": 7.3,
            "away_point_diff": 0.5,
            "h2h_games": 3,
            "home_h2h_win_pct": 0.667,
            "home_rest_days": 2,
            "away_rest_days": 1,
            "home_b2b": 0,
            "away_b2b": 1,
            "home_streak": 3,
            "away_streak": -1,
            "home_home_win_pct": 0.720,
            "away_away_win_pct": 0.480
        }
    }

    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{base_url}/api/predict",
            headers=headers,
            json=prediction_data,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"[checkmark.circle] Prediction successful")
            print(f"   Matchup: {data.get('home_team')} vs {data.get('away_team')}")
            print(f"   Prediction: {data.get('prediction')}")
            print(f"   Confidence: {data.get('confidence', 0)*100:.1f}%")
            print(f"   Model: {data.get('model_used')}")
            return True
        else:
            print(f"[xmark.circle] Prediction failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[xmark.circle] Prediction failed: {e}")
        return False


def test_metrics_endpoint(base_url: str) -> bool:
    """Test the metrics endpoint"""
    print(f"\n📈 Testing metrics endpoint: {base_url}/api/metrics")
    try:
        response = requests.get(f"{base_url}/api/metrics", timeout=10)
        if response.status_code == 200:
            print(f"[checkmark.circle] Metrics endpoint accessible")
            # Prometheus metrics are plain text
            lines = response.text.split('\n')[:5]
            print(f"   First few metrics:")
            for line in lines:
                if line and not line.startswith('#'):
                    print(f"     {line}")
            return True
        else:
            print(f"[xmark.circle] Metrics endpoint failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[xmark.circle] Metrics endpoint failed: {e}")
        return False


def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description="Test NBA Prediction API connection")
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="API base URL (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--username",
        default="admin",
        help="API username (default: admin)"
    )
    parser.add_argument(
        "--password",
        default="admin",
        help="API password (default: admin)"
    )
    args = parser.parse_args()

    print("=" * 70)
    print("🧪 NBA Prediction API Connection Test")
    print("=" * 70)
    print(f"   Base URL: {args.url}")
    print(f"   Username: {args.username}")
    print("=" * 70)

    # Run tests
    results = {}
    results["health"] = test_health_endpoint(args.url)

    token = test_login(args.url, args.username, args.password)
    results["login"] = bool(token)

    if token:
        results["models"] = test_models_endpoint(args.url, token)
        results["prediction"] = test_prediction(args.url, token)
    else:
        results["models"] = False
        results["prediction"] = False
        print("\n[exclamationmark.triangle]  Skipping authenticated endpoints (login failed)")

    results["metrics"] = test_metrics_endpoint(args.url)

    # Summary
    print("\n" + "=" * 70)
    print("[chart.bar.fill] Test Summary")
    print("=" * 70)
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    print(f"   Passed: {passed}/{total}")
    print()
    for test_name, result in results.items():
        status = "[checkmark.circle] PASS" if result else "[xmark.circle] FAIL"
        print(f"   {status} - {test_name}")
    print("=" * 70)

    # Exit code
    if passed == total:
        print("\n[party.popper] All tests passed!")
        sys.exit(0)
    else:
        print(f"\n[exclamationmark.triangle]  {total - passed} test(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
