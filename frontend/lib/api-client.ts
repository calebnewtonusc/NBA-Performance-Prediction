import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://nba-performance-prediction-production.up.railway.app';

export interface GameFeatures {
  home_win_pct: number;
  away_win_pct: number;
  home_avg_points: number;
  away_avg_points: number;
  home_avg_allowed: number;
  away_avg_allowed: number;
  home_point_diff: number;
  away_point_diff: number;
  h2h_games?: number;
  home_h2h_win_pct?: number;
  home_rest_days?: number;
  away_rest_days?: number;
  home_b2b?: number;
  away_b2b?: number;
  home_streak?: number;
  away_streak?: number;
  home_home_win_pct?: number;
  away_away_win_pct?: number;
}

export interface PredictionRequest {
  home_team: string;
  away_team: string;
  features: GameFeatures;
  model_name?: string;
  model_version?: string;
}

export interface PredictionResponse {
  prediction: string;
  confidence: number;
  home_win_probability: number;
  away_win_probability: number;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  uptime_seconds: number;
  models_loaded: number;
  version: string;
}

export interface ModelInfo {
  name: string;
  version: string;
  accuracy?: number;
  created_at?: string;
  last_used?: string;
  metrics?: {
    accuracy: number;
    precision: number;
    recall: number;
    f1_score: number;
  };
}

export interface PerformanceMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  predictions_count: number;
  correct_predictions: number;
  incorrect_predictions: number;
  recent_accuracy?: number;
}

export interface DriftReport {
  drift_detected: boolean;
  drift_score: number;
  threshold: number;
  features_with_drift: string[];
  timestamp: string;
}

export interface Alert {
  id: string;
  severity: 'critical' | 'warning' | 'info';
  message: string;
  timestamp: string;
  resolved: boolean;
}

export interface Player {
  id: number;
  first_name: string;
  last_name: string;
  position: string;
  height_feet?: number;
  height_inches?: number;
  weight_pounds?: number;
  team?: {
    id: number;
    abbreviation: string;
    city: string;
    conference: string;
    division: string;
    full_name: string;
    name: string;
  };
}

export interface PlayerStats {
  player_id: number;
  season: string;
  games_played: number;
  stats: any[];
  averages: {
    pts?: number;
    ast?: number;
    reb?: number;
    stl?: number;
    blk?: number;
    turnover?: number;
    fgm?: number;
    fga?: number;
    fg_pct?: number;
    fg3m?: number;
    fg3a?: number;
    fg3_pct?: number;
    ftm?: number;
    fta?: number;
    ft_pct?: number;
    oreb?: number;
    dreb?: number;
    pf?: number;
    games_played?: number;
  };
}

export interface Game {
  id: number;
  date: string;
  home_team: {
    id: number;
    abbreviation: string;
    city: string;
    conference: string;
    division: string;
    full_name: string;
    name: string;
  };
  visitor_team: {
    id: number;
    abbreviation: string;
    city: string;
    conference: string;
    division: string;
    full_name: string;
    name: string;
  };
  home_team_score: number;
  visitor_team_score: number;
  season: number;
  postseason: boolean;
  status: string;
  winner?: string;
  score_differential?: number;
  total_points?: number;
}

export interface GameFilters {
  team?: string;
  start_date?: string;
  end_date?: string;
  season?: string;
  limit?: number;
}

export interface TeamStats {
  team: string;
  season: string;
  games_played: number;
  wins: number;
  losses: number;
  win_percentage: number;
  games?: Game[];
  stats?: any;
}

class APIClient {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async login(username: string, password: string): Promise<string> {
    const response = await this.client.post('/api/v1/auth/login', {
      username,
      password,
    });
    const token = response.data.access_token;
    if (!token) {
      throw new Error('Failed to get access token from API');
    }
    this.token = token;
    this.client.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    return token;
  }

  async getHealth(): Promise<HealthResponse> {
    const response = await this.client.get('/api/v1/health');
    return response.data;
  }

  async predict(data: PredictionRequest): Promise<PredictionResponse> {
    if (!this.token) {
      // Auto-login with default credentials
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.post('/api/v1/predict', data);
    return response.data;
  }

  async predictSimple(homeTeam: string, awayTeam: string): Promise<PredictionResponse> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.post('/api/v1/predict/simple', {
      home_team: homeTeam,
      away_team: awayTeam,
    });
    return response.data;
  }

  async batchPredict(predictions: PredictionRequest[]): Promise<PredictionResponse[]> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.post('/api/v1/predict/batch', { predictions });
    return response.data.predictions;
  }

  async getModels(): Promise<any> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.get('/api/v1/models');
    return response.data;
  }

  async exportPredictionsCSV(predictions: any[], includeTimestamp: boolean = true): Promise<Blob> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.post(
      '/api/v1/export/csv',
      {
        predictions,
        include_timestamp: includeTimestamp,
      },
      {
        responseType: 'blob',
      }
    );
    return response.data;
  }

  async getModelsList(): Promise<ModelInfo[]> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.get('/api/v1/models');
    return response.data.models || [];
  }

  async getModelDetails(name: string, version: string): Promise<ModelInfo> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.get(`/api/v1/models/${name}/${version}`);
    return response.data;
  }

  async getModelPerformance(): Promise<PerformanceMetrics> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.get('/api/v1/monitoring/performance');
    return response.data;
  }

  async getDriftStatus(): Promise<DriftReport> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.get('/api/v1/monitoring/drift');
    return response.data;
  }

  async getMonitoringAlerts(hours: number = 24): Promise<Alert[]> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.get(`/api/v1/monitoring/alerts?hours=${hours}`);
    return response.data.alerts || [];
  }

  async searchPlayers(query: string, limit: number = 20): Promise<Player[]> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.get('/api/v1/players/search', {
      params: { q: query, limit }
    });
    return response.data.players || [];
  }

  async getPlayerDetails(playerId: number): Promise<Player> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.get(`/api/v1/players/${playerId}`);
    return response.data;
  }

  async getPlayerStats(playerId: number, season: string = '2024'): Promise<PlayerStats> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.get(`/api/v1/players/${playerId}/stats`, {
      params: { season }
    });
    return response.data;
  }

  async getGames(filters: GameFilters = {}): Promise<Game[]> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.get('/api/v1/games', {
      params: filters
    });
    return response.data.games || [];
  }

  async getGameDetails(gameId: number): Promise<Game> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.get(`/api/v1/games/${gameId}`);
    return response.data;
  }

  async getTeamStats(team: string, season: string = '2024'): Promise<TeamStats> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.get('/api/v1/teams/stats', {
      params: { team, season }
    });
    return response.data;
  }
}

export const apiClient = new APIClient();
