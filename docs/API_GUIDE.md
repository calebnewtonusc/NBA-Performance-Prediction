# NBA API Guide

This document provides details on the APIs used in this project for collecting NBA data.

## Primary API: balldontlie.io

**Base URL**: `https://www.balldontlie.io/api/v1`

**Rate Limits**: 60 requests per minute (free tier)

**Authentication**: No API key required (as of 2026)

### Available Endpoints

#### 1. Teams
```
GET /teams
GET /teams/:id
```

**Response Example**:
```json
{
  "data": [
    {
      "id": 1,
      "abbreviation": "ATL",
      "city": "Atlanta",
      "conference": "East",
      "division": "Southeast",
      "full_name": "Atlanta Hawks",
      "name": "Hawks"
    }
  ]
}
```

#### 2. Players
```
GET /players
GET /players/:id
```

**Query Parameters**:
- `search`: Search by player name
- `per_page`: Results per page (default: 25, max: 100)
- `page`: Page number

**Response Example**:
```json
{
  "data": [
    {
      "id": 237,
      "first_name": "LeBron",
      "last_name": "James",
      "position": "F",
      "height_feet": 6,
      "height_inches": 9,
      "weight_pounds": 250,
      "team": {
        "id": 14,
        "abbreviation": "LAL",
        "city": "Los Angeles",
        "conference": "West",
        "division": "Pacific",
        "full_name": "Los Angeles Lakers",
        "name": "Lakers"
      }
    }
  ],
  "meta": {
    "total_pages": 100,
    "current_page": 1,
    "next_page": 2,
    "per_page": 25,
    "total_count": 2500
  }
}
```

#### 3. Games
```
GET /games
GET /games/:id
```

**Query Parameters**:
- `dates[]`: Array of dates (YYYY-MM-DD)
- `seasons[]`: Array of seasons (e.g., 2023)
- `team_ids[]`: Array of team IDs
- `start_date`: Start date for range
- `end_date`: End date for range
- `per_page`: Results per page
- `page`: Page number

**Response Example**:
```json
{
  "data": [
    {
      "id": 12345,
      "date": "2023-10-24T00:00:00.000Z",
      "home_team": {
        "id": 14,
        "abbreviation": "LAL",
        "city": "Los Angeles",
        "conference": "West",
        "division": "Pacific",
        "full_name": "Los Angeles Lakers",
        "name": "Lakers"
      },
      "home_team_score": 103,
      "period": 4,
      "postseason": false,
      "season": 2023,
      "status": "Final",
      "time": "Final",
      "visitor_team": {
        "id": 2,
        "abbreviation": "BOS",
        "city": "Boston",
        "conference": "East",
        "division": "Atlantic",
        "full_name": "Boston Celtics",
        "name": "Celtics"
      },
      "visitor_team_score": 98
    }
  ]
}
```

#### 4. Stats (Player Game Stats)
```
GET /stats
```

**Query Parameters**:
- `dates[]`: Array of dates
- `seasons[]`: Array of seasons
- `player_ids[]`: Array of player IDs
- `game_ids[]`: Array of game IDs
- `start_date`: Start date
- `end_date`: End date
- `per_page`: Results per page
- `page`: Page number

**Response Example**:
```json
{
  "data": [
    {
      "id": 12345,
      "ast": 5,
      "blk": 2,
      "dreb": 7,
      "fg3_pct": 0.375,
      "fg3a": 8,
      "fg3m": 3,
      "fg_pct": 0.48,
      "fga": 25,
      "fgm": 12,
      "ft_pct": 0.85,
      "fta": 10,
      "ftm": 8,
      "game": {
        "id": 12345,
        "date": "2023-10-24T00:00:00.000Z",
        "home_team_id": 14,
        "home_team_score": 103,
        "period": 4,
        "postseason": false,
        "season": 2023,
        "status": "Final",
        "visitor_team_id": 2,
        "visitor_team_score": 98
      },
      "min": "38:25",
      "oreb": 2,
      "pf": 3,
      "player": {
        "id": 237,
        "first_name": "LeBron",
        "last_name": "James",
        "position": "F",
        "team_id": 14
      },
      "pts": 35,
      "reb": 9,
      "stl": 2,
      "team": {
        "id": 14,
        "abbreviation": "LAL",
        "city": "Los Angeles",
        "conference": "West",
        "division": "Pacific",
        "full_name": "Los Angeles Lakers",
        "name": "Lakers"
      },
      "turnover": 4
    }
  ]
}
```

## Statistics Abbreviations

- **pts**: Points
- **ast**: Assists
- **reb**: Total Rebounds
- **oreb**: Offensive Rebounds
- **dreb**: Defensive Rebounds
- **stl**: Steals
- **blk**: Blocks
- **turnover**: Turnovers
- **pf**: Personal Fouls
- **fga**: Field Goals Attempted
- **fgm**: Field Goals Made
- **fg_pct**: Field Goal Percentage
- **fg3a**: Three Point Attempts
- **fg3m**: Three Pointers Made
- **fg3_pct**: Three Point Percentage
- **fta**: Free Throws Attempted
- **ftm**: Free Throws Made
- **ft_pct**: Free Throw Percentage
- **min**: Minutes Played

## Alternative APIs

### NBA API (Unofficial)
- Python package: `nba_api`
- More comprehensive data
- No official documentation
- Can be unreliable

### ESPN API
- Base URL: `http://site.api.espn.com/apis/site/v2/sports/basketball/nba`
- Free, no authentication required
- Limited historical data

## Best Practices

1. **Respect Rate Limits**: Implement delays between requests
2. **Cache Data**: Store raw JSON to avoid repeated API calls
3. **Batch Requests**: Use date ranges instead of individual queries
4. **Error Handling**: Always handle 429 (rate limit) and 5xx errors
5. **Pagination**: Loop through all pages for complete datasets

## Data Collection Strategy

For this project, we'll primarily use **balldontlie.io** because:
- Free and reliable
- No authentication required
- Comprehensive player and game stats
- Good documentation
- Predictable response format

We'll collect:
1. **Historical Games**: 2020-2025 seasons (5 seasons)
2. **Player Stats**: All players from games
3. **Team Information**: All 30 NBA teams
4. **Season Data**: Regular season + playoffs

## Storage Strategy

```
data/raw/
├── games/
│   ├── 2020_season.json
│   ├── 2021_season.json
│   ├── ...
├── players/
│   ├── all_players.json
│   └── player_stats_2020_2025.json
└── teams/
    └── all_teams.json
```

## Sample API Calls

```python
from src.data_collection.base_client import BaseAPIClient

client = BaseAPIClient(base_url="https://www.balldontlie.io/api/v1")

# Get all teams
teams = client.get("/teams")

# Get games for a specific date range
games = client.get("/games", params={
    "start_date": "2023-10-01",
    "end_date": "2023-10-31",
    "per_page": 100
})

# Get player stats for a season
stats = client.get("/stats", params={
    "seasons[]": [2023],
    "per_page": 100,
    "page": 1
})
```
