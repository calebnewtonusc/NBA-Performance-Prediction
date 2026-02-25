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
    <div style={{ maxWidth: '1152px', margin: '0 auto' }} className="space-y-12">

      {/* Hero Section */}
      <div style={{ textAlign: 'center', paddingTop: '24px' }} className="space-y-5">

        {/* Status badge */}
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '7px',
            padding: '6px 14px',
            borderRadius: '100px',
            background: 'rgba(255,59,48,0.1)',
            border: '0.5px solid rgba(255,59,48,0.3)',
            marginBottom: '8px',
          }}
        >
          <div
            style={{
              width: '6px',
              height: '6px',
              borderRadius: '50%',
              backgroundColor: '#FF3B30',
              animation: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            }}
          />
          <span
            style={{
              fontSize: '11px',
              fontWeight: 700,
              color: '#FF3B30',
              textTransform: 'uppercase',
              letterSpacing: '0.8px',
              fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif",
            }}
          >
            ML-Powered Predictions
          </span>
        </div>

        {/* Title */}
        <h1
          style={{
            fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif",
            fontWeight: 900,
            letterSpacing: '-0.6px',
            lineHeight: 1.08,
            margin: 0,
          }}
        >
          <span
            style={{
              display: 'block',
              fontSize: 'clamp(42px, 7vw, 64px)',
              color: '#ffffff',
            }}
          >
            NBA Performance
          </span>
          <span
            style={{
              display: 'block',
              fontSize: 'clamp(42px, 7vw, 64px)',
              color: '#FF3B30',
            }}
          >
            Prediction
          </span>
        </h1>

        <p
          style={{
            fontSize: '17px',
            color: 'rgba(255,255,255,0.6)',
            maxWidth: '520px',
            margin: '0 auto',
            lineHeight: 1.55,
            fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif",
          }}
        >
          Machine learning models trained on real NBA data — predict game outcomes, analyze players, and track model accuracy in real time.
        </p>

        {/* CTA Buttons */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', justifyContent: 'center', paddingTop: '8px' }}>
          <Link
            href="/predictions"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '7px',
              padding: '12px 22px',
              backgroundColor: '#FF3B30',
              color: '#ffffff',
              fontWeight: 700,
              fontSize: '15px',
              borderRadius: '12px',
              textDecoration: 'none',
              letterSpacing: '-0.2px',
              fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif",
              transition: 'all 150ms ease',
              boxShadow: '0 1px 12px rgba(255,59,48,0.3)',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = '#e0342a'
              e.currentTarget.style.transform = 'translateY(-1px)'
              e.currentTarget.style.boxShadow = '0 4px 20px rgba(255,59,48,0.4)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = '#FF3B30'
              e.currentTarget.style.transform = 'translateY(0)'
              e.currentTarget.style.boxShadow = '0 1px 12px rgba(255,59,48,0.3)'
            }}
          >
            <Zap style={{ width: '15px', height: '15px' }} />
            Get a Prediction
            <ArrowRight style={{ width: '15px', height: '15px' }} />
          </Link>
          <Link
            href="/players"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '7px',
              padding: '12px 22px',
              backgroundColor: '#2c2c2e',
              color: '#ffffff',
              fontWeight: 700,
              fontSize: '15px',
              borderRadius: '12px',
              textDecoration: 'none',
              letterSpacing: '-0.2px',
              fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif",
              border: '0.5px solid rgba(255,255,255,0.1)',
              transition: 'all 150ms ease',
              boxShadow: '0 1px 12px rgba(0,0,0,0.3)',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = '#3a3a3c'
              e.currentTarget.style.transform = 'translateY(-1px)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = '#2c2c2e'
              e.currentTarget.style.transform = 'translateY(0)'
            }}
          >
            <Users style={{ width: '15px', height: '15px' }} />
            Player Stats
          </Link>
        </div>
      </div>

      {/* API Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
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
              accentColor="#30D158"
              isText
            />
            <StatCard
              title="Uptime"
              value={Math.floor(health.uptime_seconds / 60)}
              suffix=" min"
              subtitle="Continuous operation"
              icon={TrendingUp}
              accentColor="#0A84FF"
              animated
            />
            <StatCard
              title="Models Loaded"
              value={health.models_loaded}
              subtitle="Ready to predict"
              icon={Database}
              accentColor="#BF5AF2"
              animated
            />
            <StatCard
              title="Version"
              value={health.version}
              subtitle="Current build"
              icon={BarChart3}
              accentColor="#FF9F0A"
              isText
            />
          </>
        ) : (
          <div
            className="col-span-4"
            style={{
              textAlign: 'center',
              padding: '24px',
              color: '#FF3B30',
              background: 'rgba(255,59,48,0.08)',
              border: '0.5px solid rgba(255,59,48,0.25)',
              borderRadius: '16px',
              fontSize: '14px',
              fontWeight: 500,
            }}
          >
            Unable to connect to API — backend may be starting up
          </div>
        )}
      </div>

      {/* Pick of the Day + Model Accuracy */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div>
          <SectionHeader icon={Target} iconColor="#FF3B30" label="Featured Matchup" />
          <PickOfTheDay />
        </div>
        <div>
          <SectionHeader icon={BarChart3} iconColor="#0A84FF" label="Model Performance" />
          <ModelAccuracyWidget />
        </div>
      </div>

      {/* Feature Cards */}
      <div>
        <SectionHeader label="Explore the Platform" />
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-4">
          <FeatureCard
            title="Game Predictions"
            description="Pick any two NBA teams and get ML-powered win probabilities with confidence scores across multiple models."
            href="/predictions"
            icon={Zap}
            accentColor="#FF3B30"
          />
          <FeatureCard
            title="Player Analysis"
            description="Search any NBA player and dive into season stats, shooting splits, and year-over-year comparisons."
            href="/players"
            icon={Users}
            accentColor="#0A84FF"
          />
          <FeatureCard
            title="Model Performance"
            description="Track the accuracy, precision, and F1 scores of each ML model in real time — full transparency."
            href="/performance"
            icon={TrendingUp}
            accentColor="#BF5AF2"
          />
          <FeatureCard
            title="Data Explorer"
            description="Browse historical game data with filters by team, date, and season to find patterns and trends."
            href="/explorer"
            icon={Database}
            accentColor="#30D158"
          />
        </div>
      </div>
    </div>
  )
}

// ---- Sub-components ----

function SectionHeader({
  icon: Icon,
  iconColor,
  label,
}: {
  icon?: React.ComponentType<{ style?: React.CSSProperties }>
  iconColor?: string
  label: string
}) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
      {Icon && iconColor && (
        <Icon style={{ width: '15px', height: '15px', color: iconColor, flexShrink: 0 }} />
      )}
      <span
        style={{
          fontSize: '16px',
          fontWeight: 700,
          color: '#ffffff',
          letterSpacing: '-0.3px',
          fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif",
        }}
      >
        {label}
      </span>
    </div>
  )
}

interface StatCardProps {
  title: string
  value: string | number
  subtitle?: string
  suffix?: string
  icon: React.ComponentType<{ style?: React.CSSProperties }>
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
    <div
      style={{
        background: '#1c1c1e',
        borderRadius: '16px',
        border: '0.5px solid rgba(255,255,255,0.08)',
        padding: '18px',
        boxShadow: '0 1px 12px rgba(0,0,0,0.4)',
        transition: 'border-color 150ms ease',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.borderColor = 'rgba(255,255,255,0.14)'
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)'
      }}
    >
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '14px' }}>
        <div
          style={{
            padding: '8px',
            borderRadius: '10px',
            backgroundColor: `${accentColor}18`,
            border: `0.5px solid ${accentColor}30`,
          }}
        >
          <Icon style={{ width: '18px', height: '18px', color: accentColor }} />
        </div>
        <div
          style={{
            width: '6px',
            height: '6px',
            borderRadius: '50%',
            backgroundColor: accentColor,
            marginTop: '2px',
            boxShadow: `0 0 6px ${accentColor}80`,
          }}
        />
      </div>
      <p
        style={{
          fontSize: '11px',
          fontWeight: 600,
          color: 'rgba(255,255,255,0.45)',
          textTransform: 'uppercase',
          letterSpacing: '0.5px',
          marginBottom: '4px',
          fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif",
        }}
      >
        {title}
      </p>
      <p
        style={{
          fontSize: '24px',
          fontWeight: 800,
          color: '#ffffff',
          letterSpacing: '-0.4px',
          lineHeight: 1.1,
          fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif",
        }}
      >
        {animated && typeof value === 'number' ? (
          <AnimatedCounter value={value} suffix={suffix} duration={1000} />
        ) : (
          <>
            {value}
            {suffix}
          </>
        )}
      </p>
      {subtitle && (
        <p
          style={{
            fontSize: '12px',
            color: 'rgba(255,255,255,0.4)',
            marginTop: '4px',
            fontWeight: 500,
          }}
        >
          {subtitle}
        </p>
      )}
    </div>
  )
}

interface FeatureCardProps {
  title: string
  description: string
  href: string
  icon: React.ComponentType<{ style?: React.CSSProperties }>
  accentColor: string
}

function FeatureCard({ title, description, href, icon: Icon, accentColor }: FeatureCardProps) {
  return (
    <Link
      href={href}
      style={{
        display: 'block',
        background: '#1c1c1e',
        borderRadius: '16px',
        border: '0.5px solid rgba(255,255,255,0.08)',
        padding: '22px',
        textDecoration: 'none',
        boxShadow: '0 1px 12px rgba(0,0,0,0.4)',
        transition: 'all 200ms ease',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.borderColor = 'rgba(255,255,255,0.14)'
        e.currentTarget.style.transform = 'translateY(-2px)'
        e.currentTarget.style.boxShadow = '0 6px 24px rgba(0,0,0,0.5)'
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)'
        e.currentTarget.style.transform = 'translateY(0)'
        e.currentTarget.style.boxShadow = '0 1px 12px rgba(0,0,0,0.4)'
      }}
    >
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
        <div
          style={{
            padding: '10px',
            borderRadius: '12px',
            backgroundColor: `${accentColor}14`,
            border: `0.5px solid ${accentColor}28`,
            flexShrink: 0,
          }}
        >
          <Icon style={{ width: '22px', height: '22px', color: accentColor }} />
        </div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
            <h3
              style={{
                fontSize: '15px',
                fontWeight: 700,
                color: '#ffffff',
                letterSpacing: '-0.2px',
                margin: 0,
                fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif",
              }}
            >
              {title}
            </h3>
            <ArrowRight
              style={{
                width: '13px',
                height: '13px',
                color: 'rgba(255,255,255,0.3)',
                flexShrink: 0,
                transition: 'all 150ms ease',
              }}
            />
          </div>
          <p
            style={{
              fontSize: '13px',
              color: 'rgba(255,255,255,0.5)',
              lineHeight: 1.5,
              margin: 0,
              fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif",
            }}
          >
            {description}
          </p>
        </div>
      </div>
    </Link>
  )
}
