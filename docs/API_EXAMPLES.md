# NBA Prediction API - Usage Examples

Complete code examples for all API endpoints in multiple languages.

---

## Table of Contents
1. [Authentication](#authentication)
2. [Game Predictions](#game-predictions)
3. [Player Predictions](#player-predictions)
4. [Model Management](#model-management)
5. [Health & Monitoring](#health--monitoring)
6. [Error Handling](#error-handling)

---

## Authentication

### Get Access Token

#### Python
```python
import requests

API_URL = "https://nba-performance-prediction-production.up.railway.app"

# Login
response = requests.post(
    f"{API_URL}/api/auth/login",
    json={
        "username": "admin",
        "password": "your_secure_password"
    }
)

token_data = response.json()
access_token = token_data["access_token"]

# Use token in subsequent requests
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
```

#### JavaScript/TypeScript
```typescript
const API_URL = "https://nba-performance-prediction-production.up.railway.app";

async function login(username: string, password: string): Promise<string> {
    const response = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
        throw new Error(`Login failed: ${response.statusText}`);
    }

    const data = await response.json();
    return data.access_token;
}

// Usage
const token = await login("admin", "your_password");
```

#### cURL
```bash
curl -X POST https://nba-performance-prediction-production.up.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your_secure_password"
  }'

# Response:
# {
#   "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
#   "token_type": "bearer"
# }

# Save token for later
export TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

---

## Game Predictions

### Simple Prediction (Auto-fetch Stats)

#### Python
```python
import requests

def predict_game(home_team: str, away_team: str, token: str, model: str = "logistic"):
    """
    Predict game outcome with automatic stats fetching

    Args:
        home_team: Home team abbreviation (e.g., 'BOS')
        away_team: Away team abbreviation (e.g., 'LAL')
        token: JWT access token
        model: Model type ('logistic', 'tree', or 'forest')
    """
    response = requests.post(
        f"{API_URL}/api/predict/simple",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "home_team": home_team,
            "away_team": away_team,
            "model_type": model
        }
    )

    return response.json()

# Example usage
prediction = predict_game("BOS", "LAL", access_token, model="logistic")

print(f"Prediction: {prediction['prediction']}")
print(f"Confidence: {prediction['confidence']:.1%}")
print(f"Home Win Probability: {prediction['home_win_probability']:.1%}")
print(f"Away Win Probability: {prediction['away_win_probability']:.1%}")
```

#### JavaScript/TypeScript
```typescript
interface GamePredictionResponse {
    prediction: "home" | "away";
    confidence: number;
    home_win_probability: number;
    away_win_probability: number;
    home_team: string;
    away_team: string;
    model_used: string;
    timestamp: string;
    cached?: boolean;
}

async function predictGame(
    homeTeam: string,
    awayTeam: string,
    token: string,
    model: "logistic" | "tree" | "forest" = "logistic"
): Promise<GamePredictionResponse> {
    const response = await fetch(`${API_URL}/api/predict/simple`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            home_team: homeTeam,
            away_team: awayTeam,
            model_type: model
        })
    });

    if (!response.ok) {
        throw new Error(`Prediction failed: ${response.statusText}`);
    }

    return response.json();
}

// Usage
const prediction = await predictGame("BOS", "LAL", token);
console.log(`${prediction.home_team} vs ${prediction.away_team}`);
console.log(`Winner: ${prediction.prediction}`);
console.log(`Confidence: ${(prediction.confidence * 100).toFixed(1)}%`);
```

#### cURL
```bash
# Simple prediction
curl -X POST https://nba-performance-prediction-production.up.railway.app/api/predict/simple \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "home_team": "BOS",
    "away_team": "LAL",
    "model_type": "logistic"
  }'

# Response:
# {
#   "prediction": "home",
#   "confidence": 0.682,
#   "home_win_probability": 0.682,
#   "away_win_probability": 0.318,
#   "home_team": "BOS",
#   "away_team": "LAL",
#   "model_used": "game_logistic:v1",
#   "timestamp": "2026-02-06T14:30:00.123456Z",
#   "cached": false
# }
```

### Manual Prediction (Custom Features)

#### Python
```python
def predict_game_manual(features: dict, token: str):
    """Predict with manually provided features"""
    response = requests.post(
        f"{API_URL}/api/predict",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "home_team": "BOS",
            "away_team": "LAL",
            "model_name": "game_logistic",
            "model_version": "v1",
            "features": features
        }
    )
    return response.json()

# Example features
features = {
    "home_win_pct": 0.720,
    "away_win_pct": 0.600,
    "home_avg_points": 119.5,
    "away_avg_points": 115.0,
    "home_avg_allowed": 110.8,
    "away_avg_allowed": 112.3,
    "home_point_diff": 8.7,
    "away_point_diff": 2.7,
    "h2h_games": 4,
    "home_h2h_win_pct": 0.750,
    "home_rest_days": 2,
    "away_rest_days": 1,
    "home_b2b": 0,
    "away_b2b": 0,
    "home_streak": 3,
    "away_streak": 1,
    "home_home_win_pct": 0.800,
    "away_away_win_pct": 0.450
}

prediction = predict_game_manual(features, access_token)
```

### Compare Multiple Models

#### Python
```python
def compare_models(home_team: str, away_team: str, token: str):
    """Get predictions from all three models"""
    response = requests.post(
        f"{API_URL}/api/predict/compare",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "home_team": home_team,
            "away_team": away_team
        }
    )

    data = response.json()

    print(f"\n{data['home_team']} vs {data['away_team']}\n")
    print("=" * 50)

    for model_name, result in data['models'].items():
        if 'error' not in result:
            print(f"\n{model_name.title()}:")
            print(f"  Winner: {result['prediction']}")
            print(f"  Confidence: {result['confidence']:.1%}")

    print(f"\nConsensus: {data['consensus']['prediction']}")
    print(f"Votes: Home ({data['consensus']['votes']['home']}) - Away ({data['consensus']['votes']['away']})")
    print(f"Average Confidence: {data['consensus']['average_confidence']:.1%}")

# Usage
compare_models("BOS", "LAL", access_token)
```

### Batch Predictions

#### Python
```python
def batch_predict(games: list, token: str):
    """Predict multiple games at once"""
    response = requests.post(
        f"{API_URL}/api/predict/batch",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "model_name": "game_logistic",
            "model_version": "v1",
            "games": games
        }
    )
    return response.json()

# Example batch
games = [
    {
        "home_team": "BOS",
        "away_team": "LAL",
        "features": {...}  # Full features
    },
    {
        "home_team": "GSW",
        "away_team": "MIA",
        "features": {...}
    },
    # ... up to 100 games
]

results = batch_predict(games, access_token)
print(f"Predicted {results['total_games']} games")
for prediction in results['predictions']:
    print(f"{prediction['home_team']} vs {prediction['away_team']}: {prediction['prediction']}")
```

---

## Player Predictions

### Predict Player Points

#### Python
```python
def predict_player_stats(player_data: dict, token: str):
    """
    Predict player performance for upcoming game

    Args:
        player_data: Player statistics and game context
        token: JWT access token
    """
    response = requests.post(
        f"{API_URL}/api/predict/player",
        headers={"Authorization": f"Bearer {token}"},
        json=player_data
    )
    return response.json()

# Example usage
player_data = {
    "player_avg_points": 28.5,
    "player_avg_rebounds": 8.2,
    "player_avg_assists": 6.1,
    "player_games_played": 45,
    "team_win_pct": 0.650,
    "opponent_def_rating": 112.0,
    "is_home": 1,  # 1 = home, 0 = away
    "rest_days": 2
}

prediction = predict_player_stats(player_data, access_token)

print(f"Predicted Points: {prediction['predicted_points']:.1f}")
print(f"Confidence Interval: {prediction['confidence_interval_low']:.1f} - {prediction['confidence_interval_high']:.1f}")
print(f"Model: {prediction['model_used']}")
```

#### JavaScript/TypeScript
```typescript
interface PlayerPredictionRequest {
    player_avg_points: number;
    player_avg_rebounds: number;
    player_avg_assists: number;
    player_games_played: number;
    team_win_pct: number;
    opponent_def_rating: number;
    is_home: 0 | 1;
    rest_days: number;
}

interface PlayerPredictionResponse {
    predicted_points: number;
    confidence_interval_low: number;
    confidence_interval_high: number;
    model_used: string;
    timestamp: string;
}

async function predictPlayerPoints(
    playerData: PlayerPredictionRequest,
    token: string
): Promise<PlayerPredictionResponse> {
    const response = await fetch(`${API_URL}/api/predict/player`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(playerData)
    });

    if (!response.ok) {
        throw new Error(`Player prediction failed: ${response.statusText}`);
    }

    return response.json();
}

// Usage
const prediction = await predictPlayerPoints({
    player_avg_points: 28.5,
    player_avg_rebounds: 8.2,
    player_avg_assists: 6.1,
    player_games_played: 45,
    team_win_pct: 0.650,
    opponent_def_rating: 112.0,
    is_home: 1,
    rest_days: 2
}, token);

console.log(`Predicted: ${prediction.predicted_points.toFixed(1)} points`);
console.log(`Range: ${prediction.confidence_interval_low.toFixed(1)} - ${prediction.confidence_interval_high.toFixed(1)}`);
```

---

## Model Management

### List All Models

#### Python
```python
def list_models(token: str):
    """Get list of all available models"""
    response = requests.get(
        f"{API_URL}/api/models",
        headers={"Authorization": f"Bearer {token}"}
    )
    data = response.json()

    print(f"Total Models: {data['total']}\n")
    for model in data['models']:
        print(f"- {model}")

# Usage
list_models(access_token)
```

### Get Model Information

#### Python
```python
def get_model_info(model_name: str, version: str, token: str):
    """Get detailed model information"""
    response = requests.get(
        f"{API_URL}/api/models/{model_name}/{version}",
        headers={"Authorization": f"Bearer {token}"}
    )
    model_info = response.json()

    print(f"Model: {model_info['name']}:{model_info['version']}")
    print(f"Type: {model_info['type']}")
    print(f"Metrics: {model_info['metrics']}")
    print(f"Created: {model_info['created_at']}")
    if model_info['last_used']:
        print(f"Last Used: {model_info['last_used']}")

# Usage
get_model_info("game_logistic", "v1", access_token)
```

### Preload Model

#### Python
```python
def preload_model(model_name: str, version: str, token: str):
    """Preload a model into memory for faster predictions"""
    response = requests.post(
        f"{API_URL}/api/models/{model_name}/{version}/load",
        headers={"Authorization": f"Bearer {token}"}
    )
    result = response.json()
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")

# Usage
preload_model("game_forest", "v1", access_token)
```

---

## Health & Monitoring

### Check API Health

#### Python
```python
def check_health():
    """Check if API is healthy (no auth required)"""
    response = requests.get(f"{API_URL}/api/health")
    health = response.json()

    print(f"Status: {health['status']}")
    print(f"Uptime: {health['uptime_seconds'] / 60:.1f} minutes")
    print(f"Models Loaded: {health['models_loaded']}")
    print(f"Version: {health['version']}")

# Usage
check_health()
```

### Get Metrics

#### Python
```python
def get_metrics(token: str):
    """Get API performance metrics"""
    response = requests.get(
        f"{API_URL}/api/metrics",
        headers={"Authorization": f"Bearer {token}"}
    )
    metrics = response.json()

    print(f"Predictions Total: {metrics['predictions_total']}")
    print(f"Cache Hits: {metrics['cache_hits']}")
    print(f"Cache Misses: {metrics['cache_misses']}")
    print(f"Cache Hit Rate: {metrics['cache_hit_rate']:.1%}")
    print(f"Errors Total: {metrics['errors_total']}")
    print(f"Models Loaded: {metrics['models_loaded']}")
    print(f"Uptime: {metrics['uptime_seconds'] / 3600:.1f} hours")

# Usage
get_metrics(access_token)
```

---

## Error Handling

### Robust Error Handling (Python)

```python
import requests
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class NBAAPIClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.token = None
        self.username = username
        self.password = password

    def login(self):
        """Authenticate and get token"""
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={"username": self.username, "password": self.password},
                timeout=10
            )
            response.raise_for_status()
            self.token = response.json()["access_token"]
            logger.info("✓ Authenticated successfully")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logger.error("✗ Invalid credentials")
            else:
                logger.error(f"✗ HTTP error: {e}")
            raise
        except requests.exceptions.Timeout:
            logger.error("✗ Request timed out")
            raise
        except requests.exceptions.ConnectionError:
            logger.error("✗ Connection failed")
            raise

    def predict_game(self, home_team: str, away_team: str, model: str = "logistic") -> Optional[dict]:
        """
        Predict game with comprehensive error handling
        """
        if not self.token:
            self.login()

        try:
            response = requests.post(
                f"{self.base_url}/api/predict/simple",
                headers={"Authorization": f"Bearer {self.token}"},
                json={
                    "home_team": home_team,
                    "away_team": away_team,
                    "model_type": model
                },
                timeout=30
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logger.warning("Token expired, re-authenticating...")
                self.login()
                return self.predict_game(home_team, away_team, model)
            elif e.response.status_code == 400:
                logger.error(f"Invalid request: {e.response.json()}")
            elif e.response.status_code == 429:
                logger.error("Rate limit exceeded. Wait before retrying.")
            elif e.response.status_code == 500:
                logger.error(f"Server error: {e.response.json()}")
            raise
        except requests.exceptions.Timeout:
            logger.error("Request timed out after 30 seconds")
            raise
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to API")
            raise

# Usage
client = NBAAPIClient(
    base_url=API_URL,
    username="admin",
    password="your_password"
)

try:
    prediction = client.predict_game("BOS", "LAL")
    print(f"Prediction: {prediction['prediction']}")
    print(f"Confidence: {prediction['confidence']:.1%}")
except Exception as e:
    print(f"Error: {e}")
```

### TypeScript Error Handling

```typescript
class NBAAPIError extends Error {
    constructor(
        message: string,
        public statusCode?: number,
        public details?: any
    ) {
        super(message);
        this.name = "NBAAPIError";
    }
}

class NBAAPIClient {
    private token: string | null = null;

    constructor(
        private baseURL: string,
        private username: string,
        private password: string
    ) {}

    async login(): Promise<void> {
        try {
            const response = await fetch(`${this.baseURL}/api/auth/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    username: this.username,
                    password: this.password
                })
            });

            if (!response.ok) {
                throw new NBAAPIError(
                    "Authentication failed",
                    response.status,
                    await response.json()
                );
            }

            const data = await response.json();
            this.token = data.access_token;
        } catch (error) {
            if (error instanceof NBAAPIError) throw error;
            throw new NBAAPIError("Network error during login");
        }
    }

    async predictGame(
        homeTeam: string,
        awayTeam: string,
        model: string = "logistic"
    ): Promise<GamePredictionResponse> {
        if (!this.token) {
            await this.login();
        }

        try {
            const response = await fetch(`${this.baseURL}/api/predict/simple`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${this.token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    home_team: homeTeam,
                    away_team: awayTeam,
                    model_type: model
                })
            });

            if (response.status === 401) {
                // Token expired, re-authenticate
                await this.login();
                return this.predictGame(homeTeam, awayTeam, model);
            }

            if (!response.ok) {
                const error = await response.json();
                throw new NBAAPIError(
                    error.detail || "Prediction failed",
                    response.status,
                    error
                );
            }

            return response.json();
        } catch (error) {
            if (error instanceof NBAAPIError) throw error;
            throw new NBAAPIError("Network error during prediction");
        }
    }
}

// Usage
const client = new NBAAPIClient(API_URL, "admin", "password");

try {
    const prediction = await client.predictGame("BOS", "LAL");
    console.log(`Winner: ${prediction.prediction}`);
} catch (error) {
    if (error instanceof NBAAPIError) {
        console.error(`API Error (${error.statusCode}): ${error.message}`);
        console.error("Details:", error.details);
    } else {
        console.error("Unexpected error:", error);
    }
}
```

---

## Complete Example: Full Workflow

```python
import requests
from datetime import datetime

class NBAPredictor:
    def __init__(self, api_url: str, username: str, password: str):
        self.api_url = api_url
        self.token = None
        self._login(username, password)

    def _login(self, username: str, password: str):
        """Authenticate with API"""
        response = requests.post(
            f"{self.api_url}/api/auth/login",
            json={"username": username, "password": password}
        )
        response.raise_for_status()
        self.token = response.json()["access_token"]

    def predict_todays_games(self, games: list):
        """
        Predict multiple games for today

        Args:
            games: List of (home_team, away_team) tuples
        """
        print(f"\nNBA Predictions for {datetime.now().strftime('%B %d, %Y')}\n")
        print("=" * 70)

        for home, away in games:
            try:
                # Get prediction
                response = requests.post(
                    f"{self.api_url}/api/predict/simple",
                    headers={"Authorization": f"Bearer {self.token}"},
                    json={"home_team": home, "away_team": away}
                )
                response.raise_for_status()
                pred = response.json()

                # Format output
                winner = home if pred['prediction'] == 'home' else away
                loser = away if pred['prediction'] == 'home' else home
                confidence = pred['confidence'] * 100

                print(f"\n{home} vs {away}")
                print(f"  → {winner} wins ({confidence:.1f}% confidence)")
                print(f"     Home: {pred['home_win_probability']*100:.1f}%")
                print(f"     Away: {pred['away_win_probability']*100:.1f}%")
                print(f"     Model: {pred['model_used']}")
                if pred.get('cached'):
                    print(f"     ⚡ Cached result")

            except Exception as e:
                print(f"\n{home} vs {away}")
                print(f"  ✗ Error: {e}")

        print("\n" + "=" * 70)

# Usage
predictor = NBAPredictor(
    api_url="https://nba-performance-prediction-production.up.railway.app",
    username="admin",
    password="your_password"
)

# Today's games (example)
todays_games = [
    ("BOS", "LAL"),
    ("GSW", "MIA"),
    ("DEN", "PHX"),
    ("MIL", "PHI"),
]

predictor.predict_todays_games(todays_games)
```

---

**API Base URL**: `https://nba-performance-prediction-production.up.railway.app`
**API Documentation**: https://nba-performance-prediction-production.up.railway.app/api/docs
**Maintained by**: Caleb Newton (https://calebnewton.me)

**Last Updated**: February 6, 2026
