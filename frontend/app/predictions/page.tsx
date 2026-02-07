'use client'

import { Suspense, useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { toast } from 'sonner'
import { apiClient, PredictionResponse } from '@/lib/api-client'
import { InfoTooltip } from '@/components/InfoTooltip'
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

function PredictionsContent() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const [homeTeam, setHomeTeam] = useState('BOS')
  const [awayTeam, setAwayTeam] = useState('LAL')
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [predictionHistory, setPredictionHistory] = useState<any[]>([])
  const [comparing, setComparing] = useState(false)
  const [modelComparisons, setModelComparisons] = useState<Array<{ model: any; prediction: PredictionResponse }> | null>(null)

  // Load from URL parameters on mount
  useEffect(() => {
    const urlHome = searchParams.get('home')
    const urlAway = searchParams.get('away')

    if (urlHome && urlAway) {
      setHomeTeam(urlHome)
      setAwayTeam(urlAway)

      // Auto-predict if valid teams from URL
      if (urlHome !== urlAway) {
        setTimeout(() => {
          handlePredict(new Event('submit') as any)
        }, 500)
      }
    }
  }, [])

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault()

    // Validation: Prevent same team selection
    if (homeTeam === awayTeam) {
      toast.error('Invalid matchup', {
        description: 'Home team and away team cannot be the same. Please select different teams.'
      })
      return
    }

    setLoading(true)
    setError(null)
    setPrediction(null)

    try {
      // Call simplified endpoint - backend fetches live stats automatically
      const result = await apiClient.predictSimple(homeTeam, awayTeam)
      setPrediction(result)

      // Show success toast
      toast.success('Prediction generated', {
        description: `${result.prediction === 'home' ? homeTeam : awayTeam} predicted to win with ${(result.confidence * 100).toFixed(1)}% confidence`
      })

      // Update URL with current prediction
      router.push(`/predictions?home=${homeTeam}&away=${awayTeam}`, { scroll: false })

      // Add to history
      const historyEntry = {
        ...result,
        home_team: homeTeam,
        away_team: awayTeam,
        timestamp: new Date().toISOString(),
      }
      setPredictionHistory((prev) => [...prev, historyEntry])
    } catch (err: any) {
      const errorMessage = err.message || err.response?.data?.detail || 'Failed to get prediction'
      setError(errorMessage)

      toast.error('Prediction failed', {
        description: errorMessage,
        action: {
          label: 'Retry',
          onClick: () => handlePredict(e)
        }
      })
    } finally {
      setLoading(false)
    }
  }

  const handleCompareAll = async () => {
    // Validation: Prevent same team selection
    if (homeTeam === awayTeam) {
      toast.error('Invalid matchup', {
        description: 'Home team and away team cannot be the same. Please select different teams.'
      })
      return
    }

    setComparing(true)
    setError(null)

    try {
      const comparisons = await apiClient.compareModels(homeTeam, awayTeam)
      setModelComparisons(comparisons)

      toast.success(`Compared ${comparisons.length} model(s)`, {
        description: `All models have predicted the ${homeTeam} vs ${awayTeam} matchup`
      })
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to compare models'
      setError(errorMessage)

      toast.error('Model comparison failed', {
        description: errorMessage,
        action: {
          label: 'Retry',
          onClick: () => handleCompareAll()
        }
      })
    } finally {
      setComparing(false)
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

      toast.success('CSV exported', {
        description: `${predictionHistory.length} prediction(s) exported successfully`
      })
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to export CSV'
      setError(errorMessage)
      toast.error('Export failed', {
        description: errorMessage
      })
    }
  }

  const handleShare = async () => {
    const url = `${window.location.origin}/predictions?home=${homeTeam}&away=${awayTeam}`
    const title = `NBA Prediction: ${homeTeam} vs ${awayTeam}`
    const text = prediction
      ? `${prediction.prediction === 'home' ? homeTeam : awayTeam} predicted to win with ${(prediction.confidence * 100).toFixed(1)}% confidence`
      : `Predict ${homeTeam} vs ${awayTeam}`

    // Try native share API first (mobile)
    if (navigator.share) {
      try {
        await navigator.share({ title, text, url })
        toast.success('Shared successfully')
      } catch (err: any) {
        // User canceled or share failed
        if (err.name !== 'AbortError') {
          console.error('Share failed:', err)
        }
      }
    } else {
      // Fallback to clipboard copy (desktop)
      try {
        await navigator.clipboard.writeText(url)
        toast.success('Link copied to clipboard!', {
          description: 'Share this link with friends'
        })
      } catch (err) {
        toast.error('Failed to copy link')
      }
    }
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6 sm:space-y-8" role="main" aria-labelledby="page-title">
      <div>
        <h1 className="text-3xl sm:text-4xl font-bold" id="page-title">Game Predictions</h1>
        <p className="text-sm sm:text-base text-gray-400 mt-2">
          Predict NBA game outcomes using live stats and machine learning
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
        <div className="bg-secondary p-4 sm:p-6 rounded-lg border border-gray-700">
          <h2 className="text-xl sm:text-2xl font-bold mb-4 sm:mb-6" id="matchup-heading">Select Matchup</h2>
          <form onSubmit={handlePredict} className="space-y-6" aria-labelledby="matchup-heading">
            <div>
              <label htmlFor="home-team-select" className="block text-sm font-medium mb-2 flex items-center">
                Home Team
                <InfoTooltip content="The team playing at home. Home court advantage is automatically factored into predictions." />
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
              <label htmlFor="away-team-select" className="block text-sm font-medium mb-2 flex items-center">
                Away Team
                <InfoTooltip content="The visiting team. Road game statistics and travel fatigue are considered in predictions." />
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

            {homeTeam === awayTeam && (
              <div className="bg-yellow-500/10 border border-yellow-500 rounded-lg p-4" role="alert" aria-live="polite">
                <p className="text-sm text-yellow-400 flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  Please select different teams for home and away
                </p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading || homeTeam === awayTeam}
              className="w-full bg-primary hover:bg-red-600 text-white font-bold py-3 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              aria-label={loading ? 'Loading prediction' : 'Get game prediction'}
              aria-busy={loading}
            >
              {loading ? 'Fetching stats and predicting...' : 'Get Prediction'}
            </button>
          </form>

          {/* Compare All Models Button */}
          <button
            type="button"
            onClick={handleCompareAll}
            disabled={comparing || loading || homeTeam === awayTeam}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed mt-3 flex items-center justify-center gap-2"
            aria-label={comparing ? 'Comparing models' : 'Compare all models'}
            aria-busy={comparing}
          >
            {comparing ? (
              <>
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Comparing models...
              </>
            ) : (
              <>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                  <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
                </svg>
                Compare All Models
              </>
            )}
          </button>

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

        <div className="bg-secondary p-4 sm:p-6 rounded-lg border border-gray-700">
          <h2 className="text-xl sm:text-2xl font-bold mb-4 sm:mb-6" id="results-heading">Prediction Result</h2>
          {loading ? (
            <div className="space-y-6 animate-pulse">
              <div className="text-center space-y-4">
                <div className="h-16 sm:h-24 bg-gray-700 rounded-lg mx-auto w-32 sm:w-40"></div>
                <div className="h-6 sm:h-8 bg-gray-700 rounded-lg mx-auto w-48 sm:w-64"></div>
                <div className="h-10 bg-gray-700 rounded-lg mx-auto w-40 sm:w-52"></div>
              </div>
              <div className="pt-4 sm:pt-6 border-t border-gray-700">
                <div className="h-40 sm:h-48 bg-gray-700 rounded-lg"></div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 sm:pt-6 border-t border-gray-700">
                <div className="bg-gray-700 h-24 rounded-lg"></div>
                <div className="bg-gray-700 h-24 rounded-lg"></div>
              </div>
            </div>
          ) : prediction ? (
            <div className="space-y-6" role="region" aria-labelledby="results-heading" aria-live="polite">
              <div className="text-center space-y-4">
                <div className="text-4xl sm:text-6xl font-bold text-primary break-words" aria-label={`Predicted winner: ${prediction.prediction === 'home' ? homeTeam : awayTeam}`}>
                  {prediction.prediction === 'home' ? homeTeam : awayTeam}
                </div>
                <div className="text-lg sm:text-2xl text-gray-300" aria-label={`Confidence: ${(prediction.confidence * 100).toFixed(1)} percent`}>
                  Wins with {(prediction.confidence * 100).toFixed(1)}% confidence
                </div>
                <div className="inline-block px-3 sm:px-4 py-2 bg-primary/20 rounded-lg">
                  <span className="text-base sm:text-lg font-medium">
                    {prediction.prediction === 'home' ? 'Home' : 'Away'} Victory Predicted
                  </span>
                </div>
              </div>

              <div className="pt-4 sm:pt-6 border-t border-gray-700">
                <h3 className="text-base sm:text-lg font-bold mb-3 sm:mb-4">Win Probability</h3>
                <ResponsiveContainer width="100%" height={180}>
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

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-6 border-t border-gray-700">
                <div className="bg-background p-4 rounded-lg border border-gray-600">
                  <div className="text-gray-400 text-xs sm:text-sm uppercase tracking-wider">Home Team</div>
                  <div className="text-lg sm:text-xl font-bold mt-1">{homeTeam}</div>
                  <div className="text-primary font-bold mt-2 text-base sm:text-lg">{(prediction.home_win_probability * 100).toFixed(1)}% to win</div>
                </div>
                <div className="bg-background p-4 rounded-lg border border-gray-600">
                  <div className="text-gray-400 text-xs sm:text-sm uppercase tracking-wider">Away Team</div>
                  <div className="text-lg sm:text-xl font-bold mt-1">{awayTeam}</div>
                  <div className="text-primary font-bold mt-2 text-base sm:text-lg">{(prediction.away_win_probability * 100).toFixed(1)}% to win</div>
                </div>
              </div>

              {/* Share Button */}
              <div className="pt-6 border-t border-gray-700">
                <button
                  onClick={handleShare}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
                  </svg>
                  Share Prediction
                </button>
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

      {/* Model Comparison Results */}
      {modelComparisons && modelComparisons.length > 0 && (
        <div className="bg-secondary p-4 sm:p-6 rounded-lg border border-gray-700">
          <div className="flex items-center gap-2 mb-4 sm:mb-6">
            <h2 className="text-xl sm:text-2xl font-bold">Model Comparison</h2>
            <InfoTooltip content="Compare predictions from all available machine learning models to see consensus and variance in confidence levels." />
          </div>

          {/* Desktop Table View */}
          <div className="hidden md:block overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-gray-700">
                  <th className="pb-3 pr-4 font-semibold text-gray-400">Model</th>
                  <th className="pb-3 pr-4 font-semibold text-gray-400">Prediction</th>
                  <th className="pb-3 pr-4 font-semibold text-gray-400">Confidence</th>
                  <th className="pb-3 pr-4 font-semibold text-gray-400">Home Win %</th>
                  <th className="pb-3 font-semibold text-gray-400">Away Win %</th>
                  <th className="pb-3 font-semibold text-gray-400">Accuracy</th>
                </tr>
              </thead>
              <tbody>
                {modelComparisons.map((comparison, index) => {
                  const predictedWinner = comparison.prediction.prediction === 'home' ? homeTeam : awayTeam
                  return (
                    <tr key={index} className="border-b border-gray-700 last:border-0">
                      <td className="py-3 pr-4">
                        <div>
                          <div className="font-semibold">{comparison.model.name}</div>
                          <div className="text-xs text-gray-500">v{comparison.model.version}</div>
                        </div>
                      </td>
                      <td className="py-3 pr-4">
                        <span className="font-bold text-primary">{predictedWinner}</span>
                      </td>
                      <td className="py-3 pr-4">
                        <span className="font-semibold">{(comparison.prediction.confidence * 100).toFixed(1)}%</span>
                      </td>
                      <td className="py-3 pr-4">
                        <div className="flex items-center gap-2">
                          <div className="flex-1 bg-gray-700 rounded-full h-2 overflow-hidden">
                            <div
                              className="bg-primary h-full transition-all"
                              style={{ width: `${comparison.prediction.home_win_probability * 100}%` }}
                            ></div>
                          </div>
                          <span className="text-sm font-medium w-12 text-right">
                            {(comparison.prediction.home_win_probability * 100).toFixed(1)}%
                          </span>
                        </div>
                      </td>
                      <td className="py-3 pr-4">
                        <div className="flex items-center gap-2">
                          <div className="flex-1 bg-gray-700 rounded-full h-2 overflow-hidden">
                            <div
                              className="bg-blue-500 h-full transition-all"
                              style={{ width: `${comparison.prediction.away_win_probability * 100}%` }}
                            ></div>
                          </div>
                          <span className="text-sm font-medium w-12 text-right">
                            {(comparison.prediction.away_win_probability * 100).toFixed(1)}%
                          </span>
                        </div>
                      </td>
                      <td className="py-3">
                        {comparison.model.metrics?.accuracy ? (
                          <span className="text-sm text-green-400 font-medium">
                            {(comparison.model.metrics.accuracy * 100).toFixed(1)}%
                          </span>
                        ) : (
                          <span className="text-sm text-gray-500">N/A</span>
                        )}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>

          {/* Mobile Card View */}
          <div className="md:hidden space-y-4">
            {modelComparisons.map((comparison, index) => {
              const predictedWinner = comparison.prediction.prediction === 'home' ? homeTeam : awayTeam
              return (
                <div key={index} className="bg-background p-4 rounded-lg border border-gray-600">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <div className="font-bold text-lg">{comparison.model.name}</div>
                      <div className="text-xs text-gray-500">v{comparison.model.version}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-gray-400">Accuracy</div>
                      {comparison.model.metrics?.accuracy ? (
                        <div className="text-green-400 font-semibold">
                          {(comparison.model.metrics.accuracy * 100).toFixed(1)}%
                        </div>
                      ) : (
                        <div className="text-gray-500">N/A</div>
                      )}
                    </div>
                  </div>

                  <div className="space-y-2">
                    <div>
                      <div className="text-sm text-gray-400 mb-1">Prediction</div>
                      <div className="text-xl font-bold text-primary">{predictedWinner}</div>
                      <div className="text-sm text-gray-300">
                        {(comparison.prediction.confidence * 100).toFixed(1)}% confidence
                      </div>
                    </div>

                    <div>
                      <div className="text-sm text-gray-400 mb-1">Home: {homeTeam}</div>
                      <div className="flex items-center gap-2">
                        <div className="flex-1 bg-gray-700 rounded-full h-2 overflow-hidden">
                          <div
                            className="bg-primary h-full transition-all"
                            style={{ width: `${comparison.prediction.home_win_probability * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-medium">
                          {(comparison.prediction.home_win_probability * 100).toFixed(1)}%
                        </span>
                      </div>
                    </div>

                    <div>
                      <div className="text-sm text-gray-400 mb-1">Away: {awayTeam}</div>
                      <div className="flex items-center gap-2">
                        <div className="flex-1 bg-gray-700 rounded-full h-2 overflow-hidden">
                          <div
                            className="bg-blue-500 h-full transition-all"
                            style={{ width: `${comparison.prediction.away_win_probability * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-medium">
                          {(comparison.prediction.away_win_probability * 100).toFixed(1)}%
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>

          <div className="mt-4 pt-4 border-t border-gray-700">
            <p className="text-xs text-gray-500 flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
              Tip: Different models may have varying strengths. Compare accuracy and confidence when making decisions.
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

export default function Predictions() {
  return (
    <Suspense fallback={
      <div className="max-w-6xl mx-auto space-y-6 sm:space-y-8">
        <div>
          <h1 className="text-3xl sm:text-4xl font-bold">Game Predictions</h1>
          <p className="text-sm sm:text-base text-gray-400 mt-2">Loading...</p>
        </div>
      </div>
    }>
      <PredictionsContent />
    </Suspense>
  )
}
