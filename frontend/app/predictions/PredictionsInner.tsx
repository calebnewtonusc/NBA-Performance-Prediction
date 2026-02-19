'use client'

import { useReducer, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { toast } from 'sonner'
import { apiClient, PredictionResponse, ModelInfo } from '@/lib/api-client'
import { MatchupForm } from './MatchupForm'
import { PredictionResult } from './PredictionResult'
import { ModelComparisonPanel } from './ModelComparisonPanel'

// ---------------------------------------------------------------------------
// State & reducer
// ---------------------------------------------------------------------------

interface PredictionsState {
  homeTeam: string
  awayTeam: string
  prediction: PredictionResponse | null
  loading: boolean
  error: string | null
  predictionHistory: any[]
  comparing: boolean
  modelComparisons: Array<{ model: ModelInfo; prediction: PredictionResponse }> | null
}

type PredictionsAction =
  | { type: 'SET_TEAMS'; home: string; away: string }
  | { type: 'SET_HOME'; payload: string }
  | { type: 'SET_AWAY'; payload: string }
  | { type: 'PREDICT_START' }
  | { type: 'PREDICT_SUCCESS'; payload: PredictionResponse; home: string; away: string }
  | { type: 'PREDICT_ERROR'; payload: string }
  | { type: 'PREDICT_END' }
  | { type: 'COMPARE_START' }
  | { type: 'COMPARE_SUCCESS'; payload: Array<{ model: ModelInfo; prediction: PredictionResponse }> }
  | { type: 'COMPARE_ERROR'; payload: string }
  | { type: 'COMPARE_END' }
  | { type: 'SET_ERROR'; payload: string | null }

const initialState: PredictionsState = {
  homeTeam: 'BOS',
  awayTeam: 'LAL',
  prediction: null,
  loading: false,
  error: null,
  predictionHistory: [],
  comparing: false,
  modelComparisons: null,
}

function predictionsReducer(
  state: PredictionsState,
  action: PredictionsAction
): PredictionsState {
  switch (action.type) {
    case 'SET_TEAMS':
      return { ...state, homeTeam: action.home, awayTeam: action.away }
    case 'SET_HOME':
      return { ...state, homeTeam: action.payload }
    case 'SET_AWAY':
      return { ...state, awayTeam: action.payload }
    case 'PREDICT_START':
      return { ...state, loading: true, error: null, prediction: null }
    case 'PREDICT_SUCCESS':
      return {
        ...state,
        prediction: action.payload,
        predictionHistory: [
          ...state.predictionHistory,
          {
            ...action.payload,
            home_team: action.home,
            away_team: action.away,
            timestamp: new Date().toISOString(),
          },
        ],
      }
    case 'PREDICT_ERROR':
      return { ...state, error: action.payload }
    case 'PREDICT_END':
      return { ...state, loading: false }
    case 'COMPARE_START':
      return { ...state, comparing: true, error: null }
    case 'COMPARE_SUCCESS':
      return { ...state, modelComparisons: action.payload }
    case 'COMPARE_ERROR':
      return { ...state, error: action.payload }
    case 'COMPARE_END':
      return { ...state, comparing: false }
    case 'SET_ERROR':
      return { ...state, error: action.payload }
    default:
      return state
  }
}

function PredictionLoadingSkeleton() {
  return (
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
  )
}

// ---------------------------------------------------------------------------
// PredictionsInner — uses useSearchParams; must be rendered inside <Suspense>
// ---------------------------------------------------------------------------

export function PredictionsInner() {
  const router = useRouter()
  const [state, dispatch] = useReducer(predictionsReducer, initialState)

  const {
    homeTeam,
    awayTeam,
    prediction,
    loading,
    error,
    predictionHistory,
    comparing,
    modelComparisons,
  } = state

  // Read URL params via window.location.search (client-side only) to avoid
  // useSearchParams() which triggers a Next.js Suspense boundary requirement.
  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const urlHome = params.get('home')
    const urlAway = params.get('away')

    if (urlHome && urlAway && urlHome !== urlAway) {
      dispatch({ type: 'SET_TEAMS', home: urlHome, away: urlAway })
      setTimeout(() => {
        handlePredict(new Event('submit') as any, urlHome, urlAway)
      }, 500)
    } else if (urlHome && urlAway) {
      dispatch({ type: 'SET_TEAMS', home: urlHome, away: urlAway })
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const handlePredict = async (
    e: React.FormEvent,
    overrideHome?: string,
    overrideAway?: string
  ) => {
    e.preventDefault()
    const home = overrideHome ?? homeTeam
    const away = overrideAway ?? awayTeam

    if (home === away) {
      toast.error('Invalid matchup', {
        description: 'Home team and away team cannot be the same. Please select different teams.',
      })
      return
    }

    dispatch({ type: 'PREDICT_START' })

    try {
      const result = await apiClient.predictSimple(home, away)
      dispatch({ type: 'PREDICT_SUCCESS', payload: result, home, away })

      toast.success('Prediction generated', {
        description: `${result.prediction === 'home' ? home : away} predicted to win with ${(result.confidence * 100).toFixed(1)}% confidence`,
      })

      router.push(`/predictions?home=${home}&away=${away}`, { scroll: false })
    } catch (err: any) {
      const errorMessage = err.message || err.response?.data?.detail || 'Failed to get prediction'
      dispatch({ type: 'PREDICT_ERROR', payload: errorMessage })

      toast.error('Prediction failed', {
        description: errorMessage,
        action: { label: 'Retry', onClick: () => handlePredict(e) },
      })
    } finally {
      dispatch({ type: 'PREDICT_END' })
    }
  }

  const handleCompareAll = async () => {
    if (homeTeam === awayTeam) {
      toast.error('Invalid matchup', {
        description: 'Home team and away team cannot be the same. Please select different teams.',
      })
      return
    }

    dispatch({ type: 'COMPARE_START' })

    try {
      const comparisons = await apiClient.compareModels(homeTeam, awayTeam)
      dispatch({ type: 'COMPARE_SUCCESS', payload: comparisons })

      toast.success(`Compared ${comparisons.length} model(s)`, {
        description: `All models have predicted the ${homeTeam} vs ${awayTeam} matchup`,
      })
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to compare models'
      dispatch({ type: 'COMPARE_ERROR', payload: errorMessage })

      toast.error('Model comparison failed', {
        description: errorMessage,
        action: { label: 'Retry', onClick: () => handleCompareAll() },
      })
    } finally {
      dispatch({ type: 'COMPARE_END' })
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
        description: `${predictionHistory.length} prediction(s) exported successfully`,
      })
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to export CSV'
      dispatch({ type: 'SET_ERROR', payload: errorMessage })
      toast.error('Export failed', { description: errorMessage })
    }
  }

  const handleShare = async () => {
    const url = `${window.location.origin}/predictions?home=${homeTeam}&away=${awayTeam}`
    const title = `NBA Prediction: ${homeTeam} vs ${awayTeam}`
    const text = prediction
      ? `${prediction.prediction === 'home' ? homeTeam : awayTeam} predicted to win with ${(prediction.confidence * 100).toFixed(1)}% confidence`
      : `Predict ${homeTeam} vs ${awayTeam}`

    if (navigator.share) {
      try {
        await navigator.share({ title, text, url })
        toast.success('Shared successfully')
      } catch (err: any) {
        if (err.name !== 'AbortError') console.error('Share failed:', err)
      }
    } else {
      try {
        await navigator.clipboard.writeText(url)
        toast.success('Link copied to clipboard!', { description: 'Share this link with friends' })
      } catch {
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
        <MatchupForm
          homeTeam={homeTeam}
          awayTeam={awayTeam}
          loading={loading}
          comparing={comparing}
          error={error}
          onHomeChange={(team) => dispatch({ type: 'SET_HOME', payload: team })}
          onAwayChange={(team) => dispatch({ type: 'SET_AWAY', payload: team })}
          onPredict={handlePredict}
          onCompareAll={handleCompareAll}
        />

        <div className="bg-secondary p-4 sm:p-6 rounded-lg border border-gray-700">
          <h2 className="text-xl sm:text-2xl font-bold mb-4 sm:mb-6" id="results-heading">
            Prediction Result
          </h2>
          {loading ? (
            <PredictionLoadingSkeleton />
          ) : prediction ? (
            <PredictionResult
              prediction={prediction}
              homeTeam={homeTeam}
              awayTeam={awayTeam}
              predictionHistory={predictionHistory}
              onShare={handleShare}
              onExportCSV={handleExportCSV}
            />
          ) : (
            <div className="text-center py-12 text-gray-400">
              Select teams and click "Get Prediction" to see results
            </div>
          )}
        </div>
      </div>

      {modelComparisons && modelComparisons.length > 0 && (
        <ModelComparisonPanel
          modelComparisons={modelComparisons}
          homeTeam={homeTeam}
          awayTeam={awayTeam}
        />
      )}
    </div>
  )
}
