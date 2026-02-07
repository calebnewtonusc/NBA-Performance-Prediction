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
  private cache: Map<string, { data: any; timestamp: number }> = new Map();
  private cacheDuration = 5 * 60 * 1000; // 5 minutes

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000, // 30 second timeout
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add response interceptor for better error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        // Transform errors into user-friendly messages
        return Promise.reject(this.handleError(error));
      }
    );
  }

  private handleError(error: any): Error {
    // Network error (no internet, server down, etc.)
    if (error.code === 'ECONNABORTED') {
      return new Error('Request timed out. Please try again.');
    }

    if (error.code === 'ERR_NETWORK' || !error.response) {
      return new Error('Unable to connect to server. Please check your internet connection.');
    }

    // HTTP error responses
    if (error.response) {
      const status = error.response.status;
      const message = error.response.data?.detail || error.response.data?.message;

      switch (status) {
        case 400:
          return new Error(message || 'Invalid request. Please check your input.');
        case 401:
          return new Error('Session expired. Please refresh the page.');
        case 403:
          return new Error('Access denied. You do not have permission to perform this action.');
        case 404:
          return new Error(message || 'Resource not found. Please try again.');
        case 429:
          return new Error('Too many requests. Please wait a moment and try again.');
        case 500:
          return new Error(message || 'Server error. Please try again later.');
        case 502:
        case 503:
        case 504:
          return new Error('Service temporarily unavailable. Please try again in a few moments.');
        default:
          return new Error(message || `Error ${status}: Unable to complete request`);
      }
    }

    // Unknown error
    return new Error(error.message || 'An unexpected error occurred. Please try again.');
  }

  private getCacheKey(method: string, url: string, params?: any): string {
    return `${method}:${url}:${JSON.stringify(params || {})}`;
  }

  private getCached<T>(key: string): T | null {
    const cached = this.cache.get(key);
    if (!cached) return null;

    const age = Date.now() - cached.timestamp;
    if (age > this.cacheDuration) {
      this.cache.delete(key);
      return null;
    }

    return cached.data as T;
  }

  private setCache(key: string, data: any): void {
    this.cache.set(key, { data, timestamp: Date.now() });
  }

  clearCache(): void {
    this.cache.clear();
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

  async compareModels(homeTeam: string, awayTeam: string): Promise<Array<{ model: ModelInfo; prediction: PredictionResponse }>> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }

    // Get all available models
    const models = await this.getModelsList();

    // Make predictions with each model
    const comparisons = await Promise.all(
      models.map(async (model) => {
        try {
          const response = await this.client.post('/api/v1/predict/simple', {
            home_team: homeTeam,
            away_team: awayTeam,
            model_name: model.name,
            model_version: model.version,
          });
          return {
            model,
            prediction: response.data,
          };
        } catch (error) {
          console.error(`Failed to get prediction from ${model.name} v${model.version}:`, error);
          return null;
        }
      })
    );

    // Filter out failed predictions
    return comparisons.filter((c): c is { model: ModelInfo; prediction: PredictionResponse } => c !== null);
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

  async searchPlayers(query: string, limit: number = 20): Promise<{ players: Player[], dataSource?: string, timestamp?: string }> {
    // Check cache first
    const cacheKey = this.getCacheKey('GET', 'players/search', { query, limit });
    const cached = this.getCached<{ players: Player[], dataSource?: string, timestamp?: string }>(cacheKey);
    if (cached) {
      console.log('[Cache] Using cached player search results');
      return cached;
    }

    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }

    const response = await this.client.get('/api/v1/players/search', {
      params: { q: query, limit }
    });

    // Validate response
    if (!response.data || !Array.isArray(response.data.players)) {
      throw new Error('Invalid response format from server');
    }

    const result = {
      players: response.data.players,
      dataSource: response.data.data_source,
      timestamp: response.data.timestamp
    };

    // Cache the results
    this.setCache(cacheKey, result);

    return result;
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
    // Check cache first
    const cacheKey = this.getCacheKey('GET', 'games', filters);
    const cached = this.getCached<Game[]>(cacheKey);
    if (cached) {
      console.log('[Cache] Using cached games data');
      return cached;
    }

    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }

    const response = await this.client.get('/api/v1/games', {
      params: filters
    });

    // Validate response
    if (!response.data || !Array.isArray(response.data.games)) {
      throw new Error('Invalid response format from server');
    }

    const games = response.data.games;

    // Cache the results
    this.setCache(cacheKey, games);

    return games;
  }

  async getGameDetails(gameId: number): Promise<Game> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.get(`/api/v1/games/${gameId}`);
    return response.data;
  }

  async getTeamStats(team: string, season: string = '2024'): Promise<TeamStats> {
    // Check cache first
    const cacheKey = this.getCacheKey('GET', 'teams/stats', { team, season });
    const cached = this.getCached<TeamStats>(cacheKey);
    if (cached) {
      console.log('[Cache] Using cached team stats');
      return cached;
    }

    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }

    const response = await this.client.get('/api/v1/teams/stats', {
      params: { team, season }
    });

    // Validate response
    if (!response.data) {
      throw new Error('Invalid response format from server');
    }

    const teamStats = response.data;

    // Cache the results
    this.setCache(cacheKey, teamStats);

    return teamStats;
  }
}

export const apiClient = new APIClient();
