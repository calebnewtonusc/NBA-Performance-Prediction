'use client'

import { useState } from 'react'
import { apiClient, PredictionResponse } from '@/lib/api-client'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from '@/components/LazyChart'

const NBA_TEAMS = [
  { name: 'Atlanta Hawks', abbr: 'ATL' },
  { name: 'Boston Celtics', abbr: 'BOS' },
  { name: 'Brooklyn Nets', abbr: 'BKN' },
  { name: 'Charlotte Hornets', abbr: 'CHA' },
  { name: 'Chicago Bulls', abbr: 'CHI' },
  { name: 'Cleveland Cavaliers', abbr: 'CLE' },
  { name: 'Dallas Mavericks', abbr: 'DAL' },
  { name: 'Denver Nuggets', abbr: 'DEN' },
  { name: 'Detroit Pistons', abbr: 'DET' },
  { name: 'Golden State Warriors', abbr: 'GSW' },
  { name: 'Houston Rockets', abbr: 'HOU' },
  { name: 'Indiana Pacers', abbr: 'IND' },
  { name: 'LA Clippers', abbr: 'LAC' },
  { name: 'Los Angeles Lakers', abbr: 'LAL' },
  { name: 'Memphis Grizzlies', abbr: 'MEM' },
  { name: 'Miami Heat', abbr: 'MIA' },
  { name: 'Milwaukee Bucks', abbr: 'MIL' },
  { name: 'Minnesota Timberwolves', abbr: 'MIN' },
  { name: 'New Orleans Pelicans', abbr: 'NOP' },
  { name: 'New York Knicks', abbr: 'NYK' },
  { name: 'Oklahoma City Thunder', abbr: 'OKC' },
  { name: 'Orlando Magic', abbr: 'ORL' },
  { name: 'Philadelphia 76ers', abbr: 'PHI' },
  { name: 'Phoenix Suns', abbr: 'PHX' },
  { name: 'Portland Trail Blazers', abbr: 'POR' },
  { name: 'Sacramento Kings', abbr: 'SAC' },
  { name: 'San Antonio Spurs', abbr: 'SAS' },
  { name: 'Toronto Raptors', abbr: 'TOR' },
  { name: 'Utah Jazz', abbr: 'UTA' },
  { name: 'Washington Wizards', abbr: 'WAS' },
]

export default function Predictions() {
  const [homeTeam, setHomeTeam] = useState('BOS')
  const [awayTeam, setAwayTeam] = useState('LAL')
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [predictionHistory, setPredictionHistory] = useState<any[]>([])

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      // Call simplified endpoint - backend fetches live stats automatically
      const result = await apiClient.predictSimple(homeTeam, awayTeam)
      setPrediction(result)

      // Add to history
      const historyEntry = {
        ...result,
        home_team: homeTeam,
        away_team: awayTeam,
        timestamp: new Date().toISOString(),
      }
      setPredictionHistory((prev) => [...prev, historyEntry])
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get prediction')
    } finally {
      setLoading(false)
    }
  }

  const handleExportCSV = async () => {
    try {
      const blob = await apiClient.exportPredictionsCSV(predictionHistory)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `predictions_${new Date().toISOString().split('T')[0]}.csv`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    } catch (err: any) {
      setError('Failed to export CSV')
    }
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8" role="main" aria-labelledby="page-title">
      <div>
        <h1 className="text-4xl font-bold" id="page-title">Game Predictions</h1>
        <p className="text-gray-400 mt-2">
          Predict NBA game outcomes using live stats and machine learning
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-secondary p-6 rounded-lg border border-gray-700">
          <h2 className="text-2xl font-bold mb-6" id="matchup-heading">Select Matchup</h2>
          <form onSubmit={handlePredict} className="space-y-6" aria-labelledby="matchup-heading">
            <div>
              <label htmlFor="home-team-select" className="block text-sm font-medium mb-2">
                Home Team
              </label>
              <select
                id="home-team-select"
                value={homeTeam}
                onChange={(e) => setHomeTeam(e.target.value)}
                className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary"
                aria-label="Select home team"
                aria-required="true"
              >
                {NBA_TEAMS.map((team) => (
                  <option key={team.abbr} value={team.abbr}>
                    {team.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="away-team-select" className="block text-sm font-medium mb-2">
                Away Team
              </label>
              <select
                id="away-team-select"
                value={awayTeam}
                onChange={(e) => setAwayTeam(e.target.value)}
                className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary"
                aria-label="Select away team"
                aria-required="true"
              >
                {NBA_TEAMS.map((team) => (
                  <option key={team.abbr} value={team.abbr}>
                    {team.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="bg-blue-500/10 border border-blue-500 rounded-lg p-4" role="note" aria-live="polite">
              <p className="text-sm text-blue-400">
                Stats are automatically fetched from live NBA data sources
              </p>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary hover:bg-red-600 text-white font-bold py-3 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              aria-label={loading ? 'Loading prediction' : 'Get game prediction'}
              aria-busy={loading}
            >
              {loading ? 'Fetching stats and predicting...' : 'Get Prediction'}
            </button>
          </form>

          {error && (
            <div
              className="mt-4 p-4 bg-red-500/10 border border-red-500 rounded-lg text-red-400"
              role="alert"
              aria-live="assertive"
            >
              {error}
            </div>
          )}
        </div>

        <div className="bg-secondary p-6 rounded-lg border border-gray-700">
          <h2 className="text-2xl font-bold mb-6" id="results-heading">Prediction Result</h2>
          {prediction ? (
            <div className="space-y-6" role="region" aria-labelledby="results-heading" aria-live="polite">
              <div className="text-center space-y-4">
                <div className="text-6xl font-bold text-primary" aria-label={`Predicted winner: ${prediction.prediction === 'home' ? homeTeam : awayTeam}`}>
                  {prediction.prediction === 'home' ? homeTeam : awayTeam}
                </div>
                <div className="text-2xl text-gray-300" aria-label={`Confidence: ${(prediction.confidence * 100).toFixed(1)} percent`}>
                  Wins with {(prediction.confidence * 100).toFixed(1)}% confidence
                </div>
                <div className="inline-block px-4 py-2 bg-primary/20 rounded-lg">
                  <span className="text-lg font-medium">
                    {prediction.prediction === 'home' ? 'Home' : 'Away'} Victory Predicted
                  </span>
                </div>
              </div>

              <div className="pt-6 border-t border-gray-700">
                <h3 className="text-lg font-bold mb-4">Win Probability</h3>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart
                    data={[
                      {
                        team: homeTeam,
                        probability: prediction.home_win_probability,
                      },
                      {
                        team: awayTeam,
                        probability: prediction.away_win_probability,
                      },
                    ]}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="team" stroke="#9CA3AF" />
                    <YAxis stroke="#9CA3AF" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#262730',
                        border: '1px solid #374151',
                        borderRadius: '8px',
                      }}
                    />
                    <Bar dataKey="probability" fill="#FF6B6B" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="grid grid-cols-2 gap-4 pt-6 border-t border-gray-700">
                <div>
                  <div className="text-gray-400 text-sm">Home Team</div>
                  <div className="text-xl font-bold">{homeTeam}</div>
                  <div className="text-primary font-bold mt-1">{(prediction.home_win_probability * 100).toFixed(1)}% to win</div>
                </div>
                <div>
                  <div className="text-gray-400 text-sm">Away Team</div>
                  <div className="text-xl font-bold">{awayTeam}</div>
                  <div className="text-primary font-bold mt-1">{(prediction.away_win_probability * 100).toFixed(1)}% to win</div>
                </div>
              </div>

              {predictionHistory.length > 0 && (
                <div className="pt-6 border-t border-gray-700">
                  <button
                    onClick={handleExportCSV}
                    className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                    Export {predictionHistory.length} Prediction{predictionHistory.length > 1 ? 's' : ''} to CSV
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-12 text-gray-400">
              Select teams and click "Get Prediction" to see results
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
