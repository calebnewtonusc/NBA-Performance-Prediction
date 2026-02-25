'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { apiClient, HealthResponse } from '@/lib/api-client'
import { BarChart3, Activity, TrendingUp, Database, Zap, Target, Users, ArrowRight } from 'lucide-react'
import { AnimatedCounter } from '@/components/AnimatedCounter'
import { PickOfTheDay } from '@/components/PickOfTheDay'
import { ModelAccuracyWidget } from '@/components/ModelAccuracyWidget'
import { StatCardSkeleton } from '@/components/SkeletonLoader'
import Link from 'next/link'

const SF_DISPLAY = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif"
const SF_TEXT = "-apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif"

const EASE = [0.25, 0.46, 0.45, 0.94] as const

const fadeUp = {
  hidden: { opacity: 0, y: 32 },
  visible: { opacity: 1, y: 0 },
}

const stagger = (i: number) => ({
  duration: 0.6,
  delay: i * 0.08,
  ease: EASE,
})

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
    <div style={{ maxWidth: '1152px', margin: '0 auto' }}>

      {/* ── HERO ────────────────────────────────────────────────────── */}
      <section
        style={{
          minHeight: '90vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          position: 'relative',
          padding: '80px 20px 60px',
        }}
      >
        {/* Radial gradient ambience */}
        <div
          aria-hidden
          style={{
            position: 'absolute',
            top: 0,
            left: '50%',
            transform: 'translateX(-50%)',
            width: '800px',
            height: '500px',
            background: 'radial-gradient(ellipse at top, rgba(255,59,48,0.07) 0%, transparent 70%)',
            pointerEvents: 'none',
          }}
        />

        {/* ML label */}
        <motion.p
          variants={fadeUp}
          initial="hidden"
          animate="visible"
          transition={stagger(0)}
          style={{
            fontFamily: SF_TEXT,
            fontSize: '12px',
            fontWeight: 600,
            letterSpacing: '1.5px',
            textTransform: 'uppercase',
            color: 'rgba(255,255,255,0.45)',
            marginBottom: '20px',
          }}
        >
          Machine Learning
        </motion.p>

        {/* Hero title */}
        <motion.h1
          variants={fadeUp}
          initial="hidden"
          animate="visible"
          transition={stagger(1)}
          style={{
            fontFamily: SF_DISPLAY,
            fontWeight: 900,
            letterSpacing: '-3px',
            lineHeight: 0.95,
            margin: '0 0 28px',
          }}
        >
          <span
            style={{
              display: 'block',
              fontSize: 'clamp(54px, 8vw, 80px)',
              color: '#ffffff',
            }}
          >
            NBA Performance
          </span>
          <span
            style={{
              display: 'block',
              fontSize: 'clamp(54px, 8vw, 80px)',
              background: 'linear-gradient(90deg, #FF3B30 0%, #FF6B35 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
            }}
          >
            Prediction
          </span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          variants={fadeUp}
          initial="hidden"
          animate="visible"
          transition={stagger(2)}
          style={{
            fontFamily: SF_TEXT,
            fontSize: '18px',
            fontWeight: 400,
            lineHeight: 1.6,
            color: 'rgba(255,255,255,0.6)',
            maxWidth: '480px',
            margin: '0 0 36px',
          }}
        >
          6 trained models. Real NBA data. 72.3% accuracy.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          variants={fadeUp}
          initial="hidden"
          animate="visible"
          transition={stagger(3)}
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '12px',
            justifyContent: 'center',
            marginBottom: '28px',
          }}
        >
          <Link
            href="/predictions"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              height: '56px',
              padding: '0 28px',
              backgroundColor: '#FF3B30',
              color: '#ffffff',
              fontFamily: SF_DISPLAY,
              fontWeight: 700,
              fontSize: '16px',
              letterSpacing: '-0.3px',
              borderRadius: '100px',
              textDecoration: 'none',
              boxShadow: '0 4px 24px rgba(255,59,48,0.35)',
              transition: 'all 180ms ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = '#e0342a'
              e.currentTarget.style.transform = 'translateY(-2px)'
              e.currentTarget.style.boxShadow = '0 8px 32px rgba(255,59,48,0.45)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = '#FF3B30'
              e.currentTarget.style.transform = 'translateY(0)'
              e.currentTarget.style.boxShadow = '0 4px 24px rgba(255,59,48,0.35)'
            }}
          >
            <Zap style={{ width: '16px', height: '16px' }} />
            Make a Prediction
            <ArrowRight style={{ width: '16px', height: '16px' }} />
          </Link>

          <Link
            href="/players"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              height: '56px',
              padding: '0 28px',
              backgroundColor: 'rgba(255,255,255,0.08)',
              color: '#ffffff',
              fontFamily: SF_DISPLAY,
              fontWeight: 600,
              fontSize: '16px',
              letterSpacing: '-0.3px',
              borderRadius: '100px',
              textDecoration: 'none',
              border: '0.5px solid rgba(255,255,255,0.18)',
              transition: 'all 180ms ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.13)'
              e.currentTarget.style.transform = 'translateY(-2px)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.08)'
              e.currentTarget.style.transform = 'translateY(0)'
            }}
          >
            <Users style={{ width: '16px', height: '16px' }} />
            Player Stats
          </Link>
        </motion.div>

        {/* Accuracy badge */}
        <motion.div
          variants={fadeUp}
          initial="hidden"
          animate="visible"
          transition={stagger(4)}
        >
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              padding: '8px 16px',
              borderRadius: '100px',
              backgroundColor: 'rgba(255,59,48,0.1)',
              border: '0.5px solid rgba(255,59,48,0.25)',
            }}
          >
            <motion.div
              animate={{ opacity: [1, 0.4, 1] }}
              transition={{ duration: 2.2, repeat: Infinity, ease: 'easeInOut' }}
              style={{
                width: '6px',
                height: '6px',
                borderRadius: '50%',
                backgroundColor: '#FF3B30',
              }}
            />
            <span
              style={{
                fontFamily: SF_TEXT,
                fontSize: '13px',
                fontWeight: 600,
                color: '#FF3B30',
                letterSpacing: '0.2px',
              }}
            >
              72.3% Model Accuracy
            </span>
          </div>
        </motion.div>
      </section>

      {/* ── STAT CARDS ─────────────────────────────────────────────── */}
      <motion.section
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        transition={{ duration: 0.6, ease: EASE }}
        style={{ marginBottom: '64px' }}
      >
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: '12px',
          }}
        >
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
                subtitle="All systems operational"
                icon={Activity}
                accentColor="#30D158"
                isText
                index={0}
              />
              <StatCard
                title="Uptime"
                value={Math.floor(health.uptime_seconds / 60)}
                suffix=" min"
                subtitle="Continuous operation"
                icon={TrendingUp}
                accentColor="#0A84FF"
                animated
                index={1}
              />
              <StatCard
                title="Models Loaded"
                value={health.models_loaded}
                subtitle="Ready to predict"
                icon={Database}
                accentColor="#BF5AF2"
                animated
                index={2}
              />
              <StatCard
                title="Version"
                value={health.version}
                subtitle="Current build"
                icon={BarChart3}
                accentColor="#FF9F0A"
                isText
                index={3}
              />
            </>
          ) : (
            <div
              style={{
                gridColumn: '1 / -1',
                textAlign: 'center',
                padding: '28px',
                color: '#FF3B30',
                background: 'rgba(255,59,48,0.06)',
                border: '0.5px solid rgba(255,59,48,0.2)',
                borderRadius: '16px',
                fontFamily: SF_TEXT,
                fontSize: '14px',
                fontWeight: 500,
              }}
            >
              Unable to connect to API. Backend may be starting up
            </div>
          )}
        </div>
      </motion.section>

      {/* ── FEATURED + MODEL ACCURACY ──────────────────────────────── */}
      <motion.section
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        transition={{ duration: 0.6, ease: EASE }}
        style={{ marginBottom: '64px' }}
      >
        <SectionLabel>Live Intelligence</SectionLabel>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))',
            gap: '16px',
            marginTop: '16px',
          }}
        >
          <div>
            <SectionHeader icon={Target} iconColor="#FF3B30" label="Featured Matchup" />
            <PickOfTheDay />
          </div>
          <div>
            <SectionHeader icon={BarChart3} iconColor="#0A84FF" label="Model Performance" />
            <ModelAccuracyWidget />
          </div>
        </div>
      </motion.section>

      {/* ── FEATURE CARDS ──────────────────────────────────────────── */}
      <motion.section
        variants={fadeUp}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        transition={{ duration: 0.6, ease: EASE }}
        style={{ marginBottom: '64px' }}
      >
        <SectionLabel>Explore the Platform</SectionLabel>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: '12px',
            marginTop: '16px',
          }}
        >
          <FeatureCard
            title="Game Predictions"
            description="Pick any two NBA teams and get ML-powered win probabilities with confidence scores across multiple models."
            href="/predictions"
            icon={Zap}
            accentColor="#FF3B30"
            index={0}
          />
          <FeatureCard
            title="Player Analysis"
            description="Search any NBA player and dive into season stats, shooting splits, and year-over-year comparisons."
            href="/players"
            icon={Users}
            accentColor="#0A84FF"
            index={1}
          />
          <FeatureCard
            title="Model Performance"
            description="Track the accuracy, precision, and F1 scores of each ML model in real time. Full transparency."
            href="/performance"
            icon={TrendingUp}
            accentColor="#BF5AF2"
            index={2}
          />
          <FeatureCard
            title="Data Explorer"
            description="Browse historical game data with filters by team, date, and season to find patterns and trends."
            href="/explorer"
            icon={Database}
            accentColor="#30D158"
            index={3}
          />
        </div>
      </motion.section>
    </div>
  )
}

// ── Sub-components ──────────────────────────────────────────────────────────

function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <p
      style={{
        fontFamily: SF_TEXT,
        fontSize: '12px',
        fontWeight: 600,
        letterSpacing: '1px',
        textTransform: 'uppercase',
        color: 'rgba(255,255,255,0.45)',
        margin: '0 0 4px',
      }}
    >
      {children}
    </p>
  )
}

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
        <div
          style={{
            width: '28px',
            height: '28px',
            borderRadius: '8px',
            backgroundColor: `${iconColor}18`,
            border: `0.5px solid ${iconColor}30`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0,
          }}
        >
          <Icon style={{ width: '14px', height: '14px', color: iconColor }} />
        </div>
      )}
      <span
        style={{
          fontFamily: SF_DISPLAY,
          fontSize: '20px',
          fontWeight: 800,
          color: '#ffffff',
          letterSpacing: '-0.5px',
        }}
      >
        {label}
      </span>
    </div>
  )
}

// Stat Card

interface StatCardProps {
  title: string
  value: string | number
  subtitle?: string
  suffix?: string
  icon: React.ComponentType<{ style?: React.CSSProperties }>
  accentColor: string
  isText?: boolean
  animated?: boolean
  index: number
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
  index,
}: StatCardProps) {
  return (
    <motion.div
      variants={fadeUp}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay: index * 0.08, ease: EASE }}
      whileHover={{ y: -2, borderColor: 'rgba(255,255,255,0.14)' }}
      style={{
        background: '#1c1c1e',
        borderRadius: '16px',
        border: '0.5px solid rgba(255,255,255,0.08)',
        padding: '20px',
        boxShadow: '0 2px 20px rgba(0,0,0,0.5)',
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'flex-start',
          justifyContent: 'space-between',
          marginBottom: '16px',
        }}
      >
        <div
          style={{
            width: '36px',
            height: '36px',
            borderRadius: '10px',
            backgroundColor: `${accentColor}18`,
            border: `0.5px solid ${accentColor}28`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Icon style={{ width: '18px', height: '18px', color: accentColor }} />
        </div>
        <motion.div
          animate={{ opacity: [1, 0.35, 1] }}
          transition={{ duration: 2.5, repeat: Infinity, ease: 'easeInOut', delay: index * 0.3 }}
          style={{
            width: '6px',
            height: '6px',
            borderRadius: '50%',
            backgroundColor: accentColor,
            boxShadow: `0 0 6px ${accentColor}80`,
          }}
        />
      </div>

      <p
        style={{
          fontFamily: SF_TEXT,
          fontSize: '11px',
          fontWeight: 600,
          color: 'rgba(255,255,255,0.45)',
          textTransform: 'uppercase',
          letterSpacing: '1px',
          marginBottom: '4px',
        }}
      >
        {title}
      </p>
      <p
        style={{
          fontFamily: SF_DISPLAY,
          fontSize: '28px',
          fontWeight: 800,
          color: '#ffffff',
          letterSpacing: '-0.5px',
          lineHeight: 1.1,
          marginBottom: subtitle ? '4px' : '0',
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
            fontFamily: SF_TEXT,
            fontSize: '12px',
            color: 'rgba(255,255,255,0.4)',
            fontWeight: 500,
          }}
        >
          {subtitle}
        </p>
      )}
    </motion.div>
  )
}

// Feature Card

interface FeatureCardProps {
  title: string
  description: string
  href: string
  icon: React.ComponentType<{ style?: React.CSSProperties }>
  accentColor: string
  index: number
}

function FeatureCard({ title, description, href, icon: Icon, accentColor, index }: FeatureCardProps) {
  return (
    <motion.div
      variants={fadeUp}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay: index * 0.08, ease: EASE }}
      whileHover={{ y: -2, borderColor: `rgba(255,59,48,0.25)` }}
      style={{
        background: '#1c1c1e',
        borderRadius: '20px',
        border: '0.5px solid rgba(255,255,255,0.08)',
        boxShadow: '0 2px 20px rgba(0,0,0,0.5)',
      }}
    >
      <Link
        href={href}
        style={{
          display: 'block',
          padding: '24px',
          textDecoration: 'none',
          height: '100%',
        }}
      >
        {/* Icon circle */}
        <div
          style={{
            width: '48px',
            height: '48px',
            borderRadius: '14px',
            backgroundColor: `${accentColor}18`,
            border: `0.5px solid ${accentColor}28`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '16px',
          }}
        >
          <Icon style={{ width: '22px', height: '22px', color: accentColor }} />
        </div>

        <h3
          style={{
            fontFamily: SF_DISPLAY,
            fontSize: '18px',
            fontWeight: 700,
            color: '#ffffff',
            letterSpacing: '-0.3px',
            margin: '0 0 8px',
          }}
        >
          {title}
        </h3>

        <p
          style={{
            fontFamily: SF_TEXT,
            fontSize: '14px',
            color: 'rgba(255,255,255,0.55)',
            lineHeight: 1.55,
            margin: '0 0 20px',
          }}
        >
          {description}
        </p>

        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
            fontFamily: SF_TEXT,
            fontSize: '14px',
            fontWeight: 600,
            color: accentColor,
            letterSpacing: '-0.1px',
          }}
        >
          Explore
          <ArrowRight style={{ width: '14px', height: '14px' }} />
        </div>
      </Link>
    </motion.div>
  )
}
