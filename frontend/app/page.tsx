'use client'

import { useEffect, useState } from 'react'
import { apiClient, HealthResponse } from '@/lib/api-client'
import { BarChart3, Activity, TrendingUp, Database } from 'lucide-react'

export default function Home() {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchHealth() {
      try {
        const data = await apiClient.getHealth()
        setHealth(data)
      } catch (error) {
        console.error('Failed to fetch health:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchHealth()
  }, [])

  return (
    <div className="space-y-8">
      <div className="text-center space-y-4">
        <h1 className="text-5xl font-bold bg-gradient-to-r from-primary to-red-400 bg-clip-text text-transparent">
          NBA Performance Prediction
        </h1>
        <p className="text-xl text-gray-300">
          Machine learning-powered predictions for NBA games
        </p>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-primary border-r-transparent"></div>
        </div>
      ) : health ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title="API Status"
            value={health.status}
            icon={Activity}
            color="green"
          />
          <StatCard
            title="Uptime"
            value={`${Math.floor(health.uptime_seconds / 60)} min`}
            icon={TrendingUp}
            color="blue"
          />
          <StatCard
            title="Models Loaded"
            value={health.models_loaded.toString()}
            icon={Database}
            color="purple"
          />
          <StatCard
            title="Version"
            value={health.version}
            icon={BarChart3}
            color="orange"
          />
        </div>
      ) : (
        <div className="text-center text-red-400">
          Failed to connect to API
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
        <FeatureCard
          title="Game Predictions"
          description="Predict the outcome of NBA games using advanced machine learning models"
          href="/predictions"
        />
        <FeatureCard
          title="Player Analysis"
          description="Analyze individual player performance and statistics"
          href="/players"
        />
        <FeatureCard
          title="Model Performance"
          description="View detailed metrics and accuracy of prediction models"
          href="/performance"
        />
        <FeatureCard
          title="Data Explorer"
          description="Explore historical NBA game data and trends"
          href="/explorer"
        />
      </div>
    </div>
  )
}

function StatCard({ title, value, icon: Icon, color }: any) {
  const colorClasses = {
    green: 'bg-green-500/10 text-green-400',
    blue: 'bg-blue-500/10 text-blue-400',
    purple: 'bg-purple-500/10 text-purple-400',
    orange: 'bg-orange-500/10 text-orange-400',
  }

  return (
    <div className="bg-secondary p-6 rounded-lg border border-gray-700">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-400 text-sm">{title}</p>
          <p className="text-2xl font-bold mt-1">{value}</p>
        </div>
        <div className={`p-3 rounded-lg ${colorClasses[color as keyof typeof colorClasses]}`}>
          <Icon className="h-6 w-6" />
        </div>
      </div>
    </div>
  )
}

function FeatureCard({ title, description, href }: any) {
  return (
    <a
      href={href}
      className="block bg-secondary p-6 rounded-lg border border-gray-700 hover:border-primary transition-colors"
    >
      <h3 className="text-xl font-bold mb-2">{title}</h3>
      <p className="text-gray-400">{description}</p>
    </a>
  )
}
