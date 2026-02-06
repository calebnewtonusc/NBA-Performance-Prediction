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
    const response = await this.client.post('/api/auth/login', {
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
    const response = await this.client.get('/api/health');
    return response.data;
  }

  async predict(data: PredictionRequest): Promise<PredictionResponse> {
    if (!this.token) {
      // Auto-login with default credentials
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.post('/api/predict', data);
    return response.data;
  }

  async predictSimple(homeTeam: string, awayTeam: string): Promise<PredictionResponse> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.post('/api/predict/simple', {
      home_team: homeTeam,
      away_team: awayTeam,
    });
    return response.data;
  }

  async batchPredict(predictions: PredictionRequest[]): Promise<PredictionResponse[]> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.post('/api/predict/batch', { predictions });
    return response.data.predictions;
  }

  async getModels(): Promise<any> {
    if (!this.token) {
      await this.login('admin', '3vmPHdnH8RSfvqc-UCdy5A');
    }
    const response = await this.client.get('/api/models');
    return response.data;
  }
}

export const apiClient = new APIClient();
