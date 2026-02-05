export interface Team {
  id: string;
  name: string;
  abbreviation: string;
}

export interface Game {
  home_team: string;
  away_team: string;
  home_win_pct: number;
  away_win_pct: number;
  season: number;
}

export interface Prediction {
  prediction: number;
  probability: number;
  home_team: string;
  away_team: string;
  predicted_winner: string;
  confidence: string;
}
