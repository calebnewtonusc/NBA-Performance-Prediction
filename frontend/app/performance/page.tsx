'use client'

import { useState, useEffect } from 'react'
import { toast } from 'sonner'
import { apiClient, ModelInfo, PerformanceMetrics, DriftReport, Alert } from '@/lib/api-client'
import { SkeletonCardGrid, SkeletonStats, SkeletonChart } from '@/components/LoadingSkeleton'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from '@/components/LazyChart'

export default function Performance() {
  const [models, setModels] = useState<ModelInfo[]>([])
  const [performance, setPerformance] = useState<PerformanceMetrics | null>(null)
  const [drift, setDrift] = useState<DriftReport | null>(null)
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setLoading(true)
    setError(null)

    try {
      const [modelsData, performanceData, driftData, alertsData] = await Promise.all([
        apiClient.getModelsList(),
        apiClient.getModelPerformance(),
        apiClient.getDriftStatus(),
        apiClient.getMonitoringAlerts(24),
      ])

      setModels(modelsData)
      setPerformance(performanceData)
      setDrift(driftData)
      setAlerts(alertsData)

      // Show alerts if drift detected or critical alerts exist
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
      setError(errorMessage)

      toast.error('Failed to load performance data', {
        description: errorMessage,
        action: {
          label: 'Retry',
          onClick: () => loadData()
        }
      })
    } finally {
      setLoading(false)
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
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold">Model Performance</h1>
        <div className="mt-8 text-center">
          <p className="text-gray-400">Loading performance data...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold">Model Performance</h1>
        <div className="mt-8 bg-red-900/20 border border-red-500 rounded-lg p-4" role="alert">
          <p className="text-red-400">{error}</p>
          <button
            onClick={loadData}
            className="mt-4 px-4 py-2 bg-primary text-white rounded hover:bg-primary/80"
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
        <h1 className="text-4xl font-bold" id="page-title">Model Performance</h1>
        <p className="text-gray-400 mt-2">
          View detailed metrics and accuracy of prediction models
        </p>
      </div>

      {/* Models Grid */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Available Models</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {models.map((model) => (
            <div
              key={`${model.name}-${model.version}`}
              className="bg-secondary p-6 rounded-lg border border-gray-700 hover:border-primary transition-colors"
            >
              <h3 className="text-lg font-semibold mb-2">{model.name}</h3>
              <p className="text-sm text-gray-400 mb-3">Version {model.version}</p>
              {model.metrics && (
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-400">Accuracy:</span>
                    <span className="text-sm font-semibold">
                      {(model.metrics.accuracy * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-400">Precision:</span>
                    <span className="text-sm font-semibold">
                      {(model.metrics.precision * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-400">F1 Score:</span>
                    <span className="text-sm font-semibold">
                      {(model.metrics.f1_score * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              )}
              {model.last_used && (
                <p className="text-xs text-gray-500 mt-3">
                  Last used: {formatTimestamp(model.last_used)}
                </p>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Performance Metrics */}
      {performance && (
        <div>
          <h2 className="text-2xl font-bold mb-4">Overall Performance</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-secondary p-6 rounded-lg border border-gray-700">
              <h3 className="text-xl font-semibold mb-4">Current Metrics</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Accuracy:</span>
                  <span className="text-2xl font-bold text-green-500">
                    {(performance.accuracy * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Precision:</span>
                  <span className="text-xl font-semibold">
                    {(performance.precision * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Recall:</span>
                  <span className="text-xl font-semibold">
                    {(performance.recall * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">F1 Score:</span>
                  <span className="text-xl font-semibold">
                    {(performance.f1_score * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>

            <div className="bg-secondary p-6 rounded-lg border border-gray-700">
              <h3 className="text-xl font-semibold mb-4">Prediction Statistics</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Total Predictions:</span>
                  <span className="text-2xl font-bold">{performance.predictions_count}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Correct:</span>
                  <span className="text-xl font-semibold text-green-500">
                    {performance.correct_predictions}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Incorrect:</span>
                  <span className="text-xl font-semibold text-red-500">
                    {performance.incorrect_predictions}
                  </span>
                </div>
                {performance.recent_accuracy && (
                  <div className="flex justify-between items-center pt-3 border-t border-gray-600">
                    <span className="text-gray-400">Recent Accuracy:</span>
                    <span className="text-xl font-semibold">
                      {(performance.recent_accuracy * 100).toFixed(1)}%
                    </span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Metrics Chart */}
          <div className="bg-secondary p-6 rounded-lg border border-gray-700 mt-6">
            <h3 className="text-xl font-semibold mb-4">Metrics Comparison</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={[
                  {
                    name: 'Accuracy',
                    value: performance.accuracy * 100,
                  },
                  {
                    name: 'Precision',
                    value: performance.precision * 100,
                  },
                  {
                    name: 'Recall',
                    value: performance.recall * 100,
                  },
                  {
                    name: 'F1 Score',
                    value: performance.f1_score * 100,
                  },
                ]}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="name" stroke="#9CA3AF" />
                <YAxis stroke="#9CA3AF" domain={[0, 100]} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: '1px solid #374151',
                  }}
                  formatter={(value: any) => `${value.toFixed(1)}%`}
                />
                <Bar dataKey="value" fill="#3B82F6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Drift Detection */}
      {drift && (
        <div>
          <h2 className="text-2xl font-bold mb-4">Data Drift Detection</h2>
          <div
            className={`p-6 rounded-lg border ${
              drift.drift_detected
                ? 'bg-red-900/20 border-red-500'
                : 'bg-green-900/20 border-green-500'
            }`}
            role="region"
            aria-label="Drift detection status"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold">
                {drift.drift_detected ? 'Drift Detected' : 'No Drift Detected'}
              </h3>
              <span
                className={`px-3 py-1 rounded ${
                  drift.drift_detected
                    ? 'bg-red-500 text-white'
                    : 'bg-green-500 text-white'
                }`}
              >
                {drift.drift_detected ? 'Warning' : 'Healthy'}
              </span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-gray-400 mb-2">Drift Score:</p>
                <p className="text-2xl font-bold">
                  {drift.drift_score.toFixed(4)}
                </p>
              </div>
              <div>
                <p className="text-gray-400 mb-2">Threshold:</p>
                <p className="text-2xl font-bold">{drift.threshold.toFixed(4)}</p>
              </div>
            </div>
            {drift.features_with_drift && drift.features_with_drift.length > 0 && (
              <div className="mt-4">
                <p className="text-gray-400 mb-2">Features with Drift:</p>
                <div className="flex flex-wrap gap-2">
                  {drift.features_with_drift.map((feature) => (
                    <span
                      key={feature}
                      className="px-3 py-1 bg-red-900/40 rounded text-sm"
                    >
                      {feature}
                    </span>
                  ))}
                </div>
              </div>
            )}
            <p className="text-sm text-gray-500 mt-4">
              Last checked: {formatTimestamp(drift.timestamp)}
            </p>
          </div>
        </div>
      )}

      {/* Recent Alerts */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Recent Alerts (24h)</h2>
        {alerts.length === 0 ? (
          <div className="bg-secondary p-6 rounded-lg border border-gray-700 text-center">
            <p className="text-gray-400">No alerts in the last 24 hours</p>
          </div>
        ) : (
          <div className="space-y-3">
            {alerts.map((alert) => (
              <div
                key={alert.id}
                className={`p-4 rounded-lg border ${
                  alert.resolved
                    ? 'bg-gray-900/50 border-gray-600'
                    : 'bg-secondary border-gray-700'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`font-semibold ${getSeverityColor(alert.severity)}`}>
                        {alert.severity.toUpperCase()}
                      </span>
                      {alert.resolved && (
                        <span className="text-xs px-2 py-0.5 bg-green-900/40 text-green-500 rounded">
                          Resolved
                        </span>
                      )}
                    </div>
                    <p className="text-gray-300">{alert.message}</p>
                    <p className="text-sm text-gray-500 mt-1">
                      {formatTimestamp(alert.timestamp)}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Refresh Button */}
      <div className="flex justify-center">
        <button
          onClick={loadData}
          className="px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary/80 transition-colors focus:ring-2 focus:ring-primary"
          aria-label="Refresh performance data"
        >
          Refresh Data
        </button>
      </div>
    </div>
  )
}
