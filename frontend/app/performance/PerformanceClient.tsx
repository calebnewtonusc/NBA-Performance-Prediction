'use client'

import { useReducer, useEffect } from 'react'
import { toast } from 'sonner'
import { apiClient, ModelInfo, PerformanceMetrics, DriftReport, Alert } from '@/lib/api-client'
import ModelsGrid from './ModelsGrid'
import OverallPerformanceSection from './OverallPerformanceSection'
import DriftDetectionSection from './DriftDetectionSection'
import AlertsList from './AlertsList'

interface PerformanceState {
  models: ModelInfo[]
  performance: PerformanceMetrics | null
  drift: DriftReport | null
  alerts: Alert[]
  loading: boolean
  error: string | null
}

type PerformanceAction =
  | { type: 'FETCH_START' }
  | {
      type: 'FETCH_SUCCESS'
      payload: {
        models: ModelInfo[]
        performance: PerformanceMetrics
        drift: DriftReport
        alerts: Alert[]
      }
    }
  | { type: 'FETCH_ERROR'; payload: string }

const initialState: PerformanceState = {
  models: [],
  performance: null,
  drift: null,
  alerts: [],
  loading: true,
  error: null,
}

function performanceReducer(state: PerformanceState, action: PerformanceAction): PerformanceState {
  switch (action.type) {
    case 'FETCH_START':
      return { ...state, loading: true, error: null }
    case 'FETCH_SUCCESS':
      return {
        ...state,
        loading: false,
        error: null,
        models: action.payload.models,
        performance: action.payload.performance,
        drift: action.payload.drift,
        alerts: action.payload.alerts,
      }
    case 'FETCH_ERROR':
      return { ...state, loading: false, error: action.payload }
    default:
      return state
  }
}

export default function PerformanceClient() {
  const [state, dispatch] = useReducer(performanceReducer, initialState)
  const { models, performance, drift, alerts, loading, error } = state

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    dispatch({ type: 'FETCH_START' })

    try {
      const [modelsData, performanceData, driftData, alertsData] = await Promise.all([
        apiClient.getModelsList(),
        apiClient.getModelPerformance(),
        apiClient.getDriftStatus(),
        apiClient.getMonitoringAlerts(24),
      ])

      dispatch({
        type: 'FETCH_SUCCESS',
        payload: {
          models: modelsData,
          performance: performanceData,
          drift: driftData,
          alerts: alertsData,
        },
      })

      const criticalAlerts = alertsData.filter(a => a.severity === 'critical' && !a.resolved)

      if (driftData.drift_detected) {
        toast.warning('Data drift detected', {
          description: `Drift score: ${driftData.drift_score.toFixed(4)} (threshold: ${driftData.threshold.toFixed(4)})`
        })
      } else if (criticalAlerts.length > 0) {
        toast.error(`${criticalAlerts.length} critical alert(s)`, {
          description: 'Check the alerts section for details'
        })
      } else {
        toast.success('Performance data loaded', {
          description: `${modelsData.length} models, accuracy: ${(performanceData.accuracy * 100).toFixed(1)}%`
        })
      }
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to load performance data'
      dispatch({ type: 'FETCH_ERROR', payload: errorMessage })

      toast.error('Failed to load performance data', {
        description: errorMessage,
        action: {
          label: 'Retry',
          onClick: () => loadData()
        }
      })
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'text-red-500'
      case 'warning':
        return 'text-yellow-500'
      case 'info':
        return 'text-blue-500'
      default:
        return 'text-gray-500'
    }
  }

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString()
  }

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto space-y-8">
        <div>
          <h1 className="text-4xl font-black text-white" id="page-title">Model Performance</h1>
          <p className="text-gray-400 mt-2">View detailed metrics and accuracy of prediction models</p>
        </div>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {(['sk-stat-1', 'sk-stat-2', 'sk-stat-3', 'sk-stat-4']).map((id) => (
            <div key={id} className="h-28 bg-gray-700/40 rounded-xl animate-pulse" />
          ))}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {(['sk-chart-1', 'sk-chart-2', 'sk-chart-3']).map((id) => (
            <div key={id} className="h-48 bg-gray-700/40 rounded-xl animate-pulse" />
          ))}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-black text-white">Model Performance</h1>
        <div className="mt-8 bg-red-500/10 border border-red-500/30 rounded-xl p-5" role="alert">
          <p className="text-red-400 font-medium">{error}</p>
          <button
            onClick={loadData}
            className="mt-4 px-5 py-2.5 bg-primary text-white rounded-xl font-bold hover:bg-red-500 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8" role="main" aria-labelledby="page-title">
      <div>
        <h1 className="text-4xl font-black text-white" id="page-title">Model Performance</h1>
        <p className="text-gray-400 mt-2">
          View detailed metrics and accuracy of prediction models
        </p>
      </div>

      <ModelsGrid models={models} formatTimestamp={formatTimestamp} />

      {performance && (
        <OverallPerformanceSection performance={performance} />
      )}

      {drift && (
        <DriftDetectionSection drift={drift} formatTimestamp={formatTimestamp} />
      )}

      <AlertsList
        alerts={alerts}
        getSeverityColor={getSeverityColor}
        formatTimestamp={formatTimestamp}
      />

      <div className="flex justify-center">
        <button
          onClick={loadData}
          className="px-6 py-3 bg-primary text-white rounded-xl font-bold hover:bg-red-500 transition-all duration-200 hover:-translate-y-0.5 focus:ring-2 focus:ring-primary"
          aria-label="Refresh performance data"
        >
          Refresh Data
        </button>
      </div>
    </div>
  )
}
