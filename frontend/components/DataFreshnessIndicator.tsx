/**
 * DataFreshnessIndicator Component
 *
 * Shows when data was last updated and from what source
 */

'use client'

interface DataFreshnessIndicatorProps {
  timestamp?: string
  dataSource?: string
  className?: string
}

export function DataFreshnessIndicator({
  timestamp,
  dataSource,
  className = ''
}: DataFreshnessIndicatorProps) {
  if (!timestamp && !dataSource) return null

  const formatTimestamp = (ts: string) => {
    try {
      const date = new Date(ts)
      const now = new Date()
      const diffMs = now.getTime() - date.getTime()
      const diffSec = Math.floor(diffMs / 1000)
      const diffMin = Math.floor(diffSec / 60)
      const diffHour = Math.floor(diffMin / 60)

      if (diffSec < 60) return 'just now'
      if (diffMin < 60) return `${diffMin}m ago`
      if (diffHour < 24) return `${diffHour}h ago`

      return date.toLocaleString()
    } catch (e) {
      return 'recently'
    }
  }

  const getSourceDisplay = () => {
    if (dataSource === 'api') {
      return { text: 'Live Data', color: 'text-green-400', bg: 'bg-green-900/40' }
    } else if (dataSource === 'fallback_cache') {
      return { text: 'Cached Data', color: 'text-yellow-400', bg: 'bg-yellow-900/40' }
    } else {
      return { text: 'Data', color: 'text-gray-400', bg: 'bg-gray-900/40' }
    }
  }

  const source = getSourceDisplay()

  return (
    <div className={`flex items-center gap-2 text-xs ${className}`}>
      {dataSource && (
        <span className={`px-2 py-1 rounded ${source.bg} ${source.color}`}>
          {source.text}
        </span>
      )}
      {timestamp && (
        <span className="text-gray-500">
          Updated {formatTimestamp(timestamp)}
        </span>
      )}
    </div>
  )
}
