'use client'

import { ModelInfo } from '@/lib/api-client'

interface ModelsGridProps {
  models: ModelInfo[]
  formatTimestamp: (timestamp: string) => string
}

export default function ModelsGrid({ models, formatTimestamp }: ModelsGridProps) {
  return (
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
  )
}
