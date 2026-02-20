'use client'

import { useEffect, useState } from 'react'
import { apiClient, HealthResponse } from '@/lib/api-client'
import { BarChart3, Activity, TrendingUp, Database, Zap, Target, Users, ArrowRight } from 'lucide-react'
import { AnimatedCounter } from '@/components/AnimatedCounter'
import { PickOfTheDay } from '@/components/PickOfTheDay'
import { ModelAccuracyWidget } from '@/components/ModelAccuracyWidget'
import { StatCardSkeleton } from '@/components/SkeletonLoader'
import Link from 'next/link'

export default function HomeClient() {
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
    <div className="space-y-10 max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="text-center space-y-5 pt-4">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary/10 border border-primary/30 text-primary text-xs font-bold uppercase tracking-widest mb-2">
          <div className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
          ML-Powered Predictions
        </div>
        <h1 className="text-5xl sm:text-6xl font-black tracking-tight">
          <span className="bg-gradient-to-r from-white via-gray-100 to-gray-300 bg-clip-text text-transparent">
            NBA Performance
          </span>
          <br />
          <span className="bg-gradient-to-r from-primary via-red-400 to-orange-400 bg-clip-text text-transparent">
            Prediction
          </span>
        </h1>
        <p className="text-lg text-gray-400 max-w-xl mx-auto leading-relaxed">
          Machine learning models trained on real NBA data — predict game outcomes, analyze players, and track model accuracy in real time.
        </p>
        <div className="flex flex-wrap gap-3 justify-center pt-2">
          <Link
            href="/predictions"
            className="flex items-center gap-2 px-6 py-3 bg-primary hover:bg-red-500 text-white font-bold rounded-xl transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-primary/30"
          >
            <Zap className="w-4 h-4" />
            Get a Prediction
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            href="/players"
            className="flex items-center gap-2 px-6 py-3 bg-secondary hover:bg-gray-700 text-white font-bold rounded-xl border border-gray-600 hover:border-gray-500 transition-all duration-200 hover:-translate-y-0.5"
          >
            <Users className="w-4 h-4" />
            Player Stats
          </Link>
        </div>
      </div>

      {/* API Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {loading ? (
          <>
            <StatCardSkeleton />
            <StatCardSkeleton />
            <StatCardSkeleton />
            <StatCardSkeleton />
          </>
        ) : health ? (
          <>
            <StatCard
              title="API Status"
              value={health.status.toUpperCase()}
              subtitle="All systems go"
              icon={Activity}
              accentColor="#10B981"
              isText
            />
            <StatCard
              title="Uptime"
              value={Math.floor(health.uptime_seconds / 60)}
              suffix=" min"
              subtitle="Continuous operation"
              icon={TrendingUp}
              accentColor="#3B82F6"
              animated
            />
            <StatCard
              title="Models Loaded"
              value={health.models_loaded}
              subtitle="Ready to predict"
              icon={Database}
              accentColor="#8B5CF6"
              animated
            />
            <StatCard
              title="Version"
              value={health.version}
              subtitle="Current build"
              icon={BarChart3}
              accentColor="#F59E0B"
              isText
            />
          </>
        ) : (
          <div className="col-span-4 text-center py-8 text-red-400 bg-red-500/10 border border-red-500/30 rounded-xl">
            Unable to connect to API — backend may be starting up
          </div>
        )}
      </div>

      {/* Pick of the Day + Model Accuracy */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h2 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
            <Target className="w-4 h-4 text-primary" />
            Featured Matchup
          </h2>
          <PickOfTheDay />
        </div>
        <div>
          <h2 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-blue-400" />
            Model Performance
          </h2>
          <ModelAccuracyWidget />
        </div>
      </div>

      {/* Feature Cards */}
      <div>
        <h2 className="text-lg font-bold text-white mb-4">Explore the Platform</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <FeatureCard
            title="Game Predictions"
            description="Pick any two NBA teams and get ML-powered win probabilities with confidence scores across multiple models."
            href="/predictions"
            icon={Zap}
            accentColor="#FF6B6B"
          />
          <FeatureCard
            title="Player Analysis"
            description="Search any NBA player and dive into season stats, shooting splits, and year-over-year comparisons."
            href="/players"
            icon={Users}
            accentColor="#3B82F6"
          />
          <FeatureCard
            title="Model Performance"
            description="Track the accuracy, precision, and F1 scores of each ML model in real time — full transparency."
            href="/performance"
            icon={TrendingUp}
            accentColor="#8B5CF6"
          />
          <FeatureCard
            title="Data Explorer"
            description="Browse historical game data with filters by team, date, and season to find patterns and trends."
            href="/explorer"
            icon={Database}
            accentColor="#10B981"
          />
        </div>
      </div>
    </div>
  )
}

// ---- Sub-components ----

interface StatCardProps {
  title: string
  value: string | number
  subtitle?: string
  suffix?: string
  icon: React.ComponentType<{ className?: string; style?: React.CSSProperties }>
  accentColor: string
  isText?: boolean
  animated?: boolean
}

function StatCard({
  title,
  value,
  subtitle,
  suffix = '',
  icon: Icon,
  accentColor,
  isText = false,
  animated = false,
}: StatCardProps) {
  return (
    <div className="bg-secondary rounded-xl border border-gray-700/50 p-5 hover:border-gray-600 transition-colors group">
      <div className="flex items-start justify-between mb-3">
        <div
          className="p-2.5 rounded-xl"
          style={{ backgroundColor: `${accentColor}18`, border: `1px solid ${accentColor}30` }}
        >
          <Icon className="h-5 w-5" style={{ color: accentColor }} />
        </div>
        <div
          className="w-1.5 h-1.5 rounded-full mt-1"
          style={{ backgroundColor: accentColor, boxShadow: `0 0 6px ${accentColor}80` }}
        />
      </div>
      <p className="text-xs font-semibold text-gray-500 uppercase tracking-widest mb-1">{title}</p>
      <p className="text-2xl font-black text-white">
        {animated && typeof value === 'number' ? (
          <AnimatedCounter value={value} suffix={suffix} duration={1000} />
        ) : (
          <>
            {value}
            {suffix}
          </>
        )}
      </p>
      {subtitle && <p className="text-xs text-gray-500 mt-1 font-medium">{subtitle}</p>}
    </div>
  )
}

interface FeatureCardProps {
  title: string
  description: string
  href: string
  icon: React.ComponentType<{ className?: string; style?: React.CSSProperties }>
  accentColor: string
}

function FeatureCard({ title, description, href, icon: Icon, accentColor }: FeatureCardProps) {
  return (
    <Link
      href={href}
      className="group block bg-secondary rounded-xl border border-gray-700/50 p-6 hover:border-gray-600 transition-all duration-200 hover:-translate-y-0.5"
    >
      <div className="flex items-start gap-4">
        <div
          className="p-3 rounded-xl flex-shrink-0 transition-all duration-200 group-hover:scale-110"
          style={{ backgroundColor: `${accentColor}15`, border: `1px solid ${accentColor}25` }}
        >
          <Icon className="h-6 w-6" style={{ color: accentColor }} />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2">
            <h3 className="text-base font-bold text-white group-hover:text-gray-100 transition-colors">
              {title}
            </h3>
            <ArrowRight
              className="w-3.5 h-3.5 text-gray-600 group-hover:text-gray-400 group-hover:translate-x-0.5 transition-all"
            />
          </div>
          <p className="text-sm text-gray-400 leading-relaxed">{description}</p>
        </div>
      </div>
    </Link>
  )
}
