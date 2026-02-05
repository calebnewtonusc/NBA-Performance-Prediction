'use client'

import { useState } from 'react'
import { apiClient, PredictionResponse } from '@/lib/api-client'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

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
  const [homeWinPct, setHomeWinPct] = useState(0.650)
  const [awayWinPct, setAwayWinPct] = useState(0.600)
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const result = await apiClient.predict({
        home_team: homeTeam,
        away_team: awayTeam,
        home_win_pct: homeWinPct,
        away_win_pct: awayWinPct,
        season: 2024,
      })
      setPrediction(result)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get prediction')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div>
        <h1 className="text-4xl font-bold">Game Predictions</h1>
        <p className="text-gray-400 mt-2">
          Predict NBA game outcomes using machine learning
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-secondary p-6 rounded-lg border border-gray-700">
          <h2 className="text-2xl font-bold mb-6">Game Setup</h2>
          <form onSubmit={handlePredict} className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">
                Home Team
              </label>
              <select
                value={homeTeam}
                onChange={(e) => setHomeTeam(e.target.value)}
                className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary"
              >
                {NBA_TEAMS.map((team) => (
                  <option key={team.abbr} value={team.abbr}>
                    {team.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Home Win % (Current Season)
              </label>
              <input
                type="number"
                min="0"
                max="1"
                step="0.001"
                value={homeWinPct}
                onChange={(e) => setHomeWinPct(parseFloat(e.target.value))}
                className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Away Team
              </label>
              <select
                value={awayTeam}
                onChange={(e) => setAwayTeam(e.target.value)}
                className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary"
              >
                {NBA_TEAMS.map((team) => (
                  <option key={team.abbr} value={team.abbr}>
                    {team.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Away Win % (Current Season)
              </label>
              <input
                type="number"
                min="0"
                max="1"
                step="0.001"
                value={awayWinPct}
                onChange={(e) => setAwayWinPct(parseFloat(e.target.value))}
                className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary hover:bg-red-600 text-white font-bold py-3 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Predicting...' : 'Get Prediction'}
            </button>
          </form>

          {error && (
            <div className="mt-4 p-4 bg-red-500/10 border border-red-500 rounded-lg text-red-400">
              {error}
            </div>
          )}
        </div>

        <div className="bg-secondary p-6 rounded-lg border border-gray-700">
          <h2 className="text-2xl font-bold mb-6">Prediction Result</h2>
          {prediction ? (
            <div className="space-y-6">
              <div className="text-center space-y-4">
                <div className="text-6xl font-bold text-primary">
                  {prediction.predicted_winner}
                </div>
                <div className="text-2xl text-gray-300">
                  Wins with {(prediction.probability * 100).toFixed(1)}% confidence
                </div>
                <div className="inline-block px-4 py-2 bg-primary/20 rounded-lg">
                  <span className="text-lg font-medium">
                    Confidence: {prediction.confidence}
                  </span>
                </div>
              </div>

              <div className="pt-6 border-t border-gray-700">
                <h3 className="text-lg font-bold mb-4">Win Probability</h3>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart
                    data={[
                      {
                        team: prediction.home_team,
                        probability: prediction.prediction === 1 ? prediction.probability : 1 - prediction.probability,
                      },
                      {
                        team: prediction.away_team,
                        probability: prediction.prediction === 0 ? prediction.probability : 1 - prediction.probability,
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
                  <div className="text-xl font-bold">{prediction.home_team}</div>
                  <div className="text-gray-400">{(homeWinPct * 100).toFixed(1)}% win rate</div>
                </div>
                <div>
                  <div className="text-gray-400 text-sm">Away Team</div>
                  <div className="text-xl font-bold">{prediction.away_team}</div>
                  <div className="text-gray-400">{(awayWinPct * 100).toFixed(1)}% win rate</div>
                </div>
              </div>
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
