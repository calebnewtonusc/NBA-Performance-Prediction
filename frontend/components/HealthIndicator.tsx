/**
 * HealthIndicator Component
 *
 * Shows the API health status with automatic periodic checks
 */

'use client'

import { useState, useEffect } from 'react'

type HealthStatus = 'healthy' | 'degraded' | 'down' | 'checking'

export function HealthIndicator() {
  const [status, setStatus] = useState<HealthStatus>('checking')
  const [lastCheck, setLastCheck] = useState<Date | null>(null)

  const checkHealth = async () => {
    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 5000) // 5s timeout

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'https://nba-performance-prediction-production.up.railway.app'}/api/v1/health`,
        {
          signal: controller.signal,
          cache: 'no-store',
        }
      )

      clearTimeout(timeoutId)
      setLastCheck(new Date())

      if (response.ok) {
        setStatus('healthy')
      } else if (response.status >= 500) {
        setStatus('degraded')
      } else {
        setStatus('down')
      }
    } catch (error: any) {
      setLastCheck(new Date())
      if (error.name === 'AbortError') {
        setStatus('degraded') // Timeout = degraded
      } else {
        setStatus('down') // Network error = down
      }
    }
  }

  useEffect(() => {
    // Initial check
    checkHealth()

    // Check every 60 seconds
    const interval = setInterval(checkHealth, 60000)

    return () => clearInterval(interval)
  }, [])

  const statusConfig = {
    healthy: {
      color: 'bg-green-500',
      text: 'Healthy',
      textColor: 'text-green-400',
    },
    degraded: {
      color: 'bg-yellow-500',
      text: 'Degraded',
      textColor: 'text-yellow-400',
    },
    down: {
      color: 'bg-red-500',
      text: 'Down',
      textColor: 'text-red-400',
    },
    checking: {
      color: 'bg-gray-500',
      text: 'Checking',
      textColor: 'text-gray-400',
    },
  }

  const config = statusConfig[status]

  return (
    <div className="flex items-center gap-2 text-xs" title={lastCheck ? `Last checked: ${lastCheck.toLocaleTimeString()}` : 'Checking API status...'}>
      <div className={`w-2 h-2 rounded-full ${config.color} ${status === 'checking' ? 'animate-pulse' : ''}`}></div>
      <span className={`${config.textColor} font-medium`}>
        API: {config.text}
      </span>
    </div>
  )
}
