'use client'

import { DriftReport } from '@/lib/api-client'
import { InfoTooltip } from '@/components/InfoTooltip'

interface DriftDetectionSectionProps {
  drift: DriftReport
  formatTimestamp: (timestamp: string) => string
}

export default function DriftDetectionSection({ drift, formatTimestamp }: DriftDetectionSectionProps) {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4 flex items-center">
        Data Drift Detection
        <InfoTooltip content="Detects when input data patterns change significantly, which may reduce model accuracy. Retraining may be needed when drift is detected." />
      </h2>
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
            <p className="text-2xl font-bold">{drift.drift_score.toFixed(4)}</p>
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
  )
}
