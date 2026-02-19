'use client'

import { Alert } from '@/lib/api-client'

interface AlertsListProps {
  alerts: Alert[]
  getSeverityColor: (severity: string) => string
  formatTimestamp: (timestamp: string) => string
}

export default function AlertsList({ alerts, getSeverityColor, formatTimestamp }: AlertsListProps) {
  return (
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
  )
}
