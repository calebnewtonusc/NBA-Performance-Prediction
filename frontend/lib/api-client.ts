import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://nba-performance-prediction-production.up.railway.app';

export interface PredictionRequest {
  home_team: string;
  away_team: string;
  home_win_pct?: number;
  away_win_pct?: number;
  season?: number;
}

export interface PredictionResponse {
  prediction: number;
  probability: number;
  home_team: string;
  away_team: string;
  predicted_winner: string;
  confidence: string;
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
      await this.login('admin', 'G9.zs8FGHP1W_lx^5eP,}mU2');
    }
    const response = await this.client.post('/api/predict', data);
    return response.data;
  }

  async batchPredict(predictions: PredictionRequest[]): Promise<PredictionResponse[]> {
    if (!this.token) {
      await this.login('admin', 'G9.zs8FGHP1W_lx^5eP,}mU2');
    }
    const response = await this.client.post('/api/predict/batch', { predictions });
    return response.data.predictions;
  }

  async getModels(): Promise<any> {
    if (!this.token) {
      await this.login('admin', 'G9.zs8FGHP1W_lx^5eP,}mU2');
    }
    const response = await this.client.get('/api/models');
    return response.data;
  }
}

export const apiClient = new APIClient();
