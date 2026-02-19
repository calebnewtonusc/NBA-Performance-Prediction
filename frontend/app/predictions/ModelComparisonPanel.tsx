'use client'

import { PredictionResponse, ModelInfo } from '@/lib/api-client'
import { InfoTooltip } from '@/components/InfoTooltip'

interface ModelComparisonPanelProps {
  modelComparisons: Array<{ model: ModelInfo; prediction: PredictionResponse }>
  homeTeam: string
  awayTeam: string
}

export function ModelComparisonPanel({
  modelComparisons,
  homeTeam,
  awayTeam,
}: ModelComparisonPanelProps) {
  return (
    <div className="bg-secondary p-4 sm:p-6 rounded-lg border border-gray-700">
      <div className="flex items-center gap-2 mb-4 sm:mb-6">
        <h2 className="text-xl sm:text-2xl font-bold">Model Comparison</h2>
        <InfoTooltip content="Compare predictions from all available machine learning models to see consensus and variance in confidence levels." />
      </div>

      {/* Desktop Table */}
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
            {modelComparisons.map((comparison) => {
              const predictedWinner =
                comparison.prediction.prediction === 'home' ? homeTeam : awayTeam
              return (
                <tr
                  key={`${comparison.model.name}-${comparison.model.version}`}
                  className="border-b border-gray-700 last:border-0"
                >
                  <td className="py-3 pr-4">
                    <div className="font-semibold">{comparison.model.name}</div>
                    <div className="text-xs text-gray-500">v{comparison.model.version}</div>
                  </td>
                  <td className="py-3 pr-4">
                    <span className="font-bold text-primary">{predictedWinner}</span>
                  </td>
                  <td className="py-3 pr-4">
                    <span className="font-semibold">
                      {(comparison.prediction.confidence * 100).toFixed(1)}%
                    </span>
                  </td>
                  <td className="py-3 pr-4">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 bg-gray-700 rounded-full h-2 overflow-hidden">
                        <div
                          className="bg-primary h-full transition-all"
                          style={{ width: `${comparison.prediction.home_win_probability * 100}%` }}
                        />
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
                        />
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

      {/* Mobile Cards */}
      <div className="md:hidden space-y-4">
        {modelComparisons.map((comparison) => {
          const predictedWinner =
            comparison.prediction.prediction === 'home' ? homeTeam : awayTeam
          return (
            <div
              key={`mobile-${comparison.model.name}-${comparison.model.version}`}
              className="bg-background p-4 rounded-lg border border-gray-600"
            >
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
                      />
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
                      />
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
  )
}
