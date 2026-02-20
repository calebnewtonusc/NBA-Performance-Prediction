'use client'

import { useEffect, useRef, useState } from 'react'
import { getTeamColors, hexToRgba } from '@/lib/nba-teams'

interface WinProbabilityGaugeProps {
  homeTeam: string
  awayTeam: string
  homeWinProbability: number
  awayWinProbability: number
  winner: 'home' | 'away'
}

export function WinProbabilityGauge({
  homeTeam,
  awayTeam,
  homeWinProbability,
  awayWinProbability,
  winner,
}: WinProbabilityGaugeProps) {
  const homeColors = getTeamColors(homeTeam)
  const awayColors = getTeamColors(awayTeam)
  const [animatedHome, setAnimatedHome] = useState(0.5)
  const frameRef = useRef<number | null>(null)
  const startTimeRef = useRef<number | null>(null)

  useEffect(() => {
    const targetHome = homeWinProbability
    startTimeRef.current = null

    const animate = (timestamp: number) => {
      if (!startTimeRef.current) {
        startTimeRef.current = timestamp
      }
      const elapsed = timestamp - startTimeRef.current
      const progress = Math.min(elapsed / 1400, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      setAnimatedHome(0.5 + (targetHome - 0.5) * eased)
      if (progress < 1) {
        frameRef.current = requestAnimationFrame(animate)
      }
    }

    frameRef.current = requestAnimationFrame(animate)
    return () => {
      if (frameRef.current) cancelAnimationFrame(frameRef.current)
    }
  }, [homeWinProbability])

  // Semicircular gauge: 180 degrees arc, 0% = left, 100% = right
  const size = 280
  const strokeWidth = 22
  const radius = (size - strokeWidth * 2) / 2
  const cx = size / 2
  const cy = size / 2

  // Arc from 180deg (left) to 0deg (right) = semicircle
  const startAngleDeg = 180
  const endAngleDeg = 0
  const totalAngleDeg = 180

  function polarToCartesian(cx: number, cy: number, r: number, angleDeg: number) {
    const rad = (angleDeg * Math.PI) / 180
    return {
      x: cx + r * Math.cos(rad),
      y: cy - r * Math.sin(rad),
    }
  }

  function describeArc(cx: number, cy: number, r: number, startDeg: number, endDeg: number) {
    const start = polarToCartesian(cx, cy, r, startDeg)
    const end = polarToCartesian(cx, cy, r, endDeg)
    const largeArc = Math.abs(endDeg - startDeg) > 180 ? 1 : 0
    const sweep = endDeg > startDeg ? 1 : 0
    return `M ${start.x} ${start.y} A ${r} ${r} 0 ${largeArc} ${sweep} ${end.x} ${end.y}`
  }

  // Needle position based on animated home probability
  // 0% home = 180deg, 100% home = 0deg
  const needleAngle = startAngleDeg - animatedHome * totalAngleDeg
  const needleLength = radius - 8
  const needleTip = polarToCartesian(cx, cy, needleLength, needleAngle)
  const needleBase1 = polarToCartesian(cx, cy, 10, needleAngle + 90)
  const needleBase2 = polarToCartesian(cx, cy, 10, needleAngle - 90)

  // Home arc: from 180 to home-probability position
  const homeEndAngle = startAngleDeg - animatedHome * totalAngleDeg
  // Away arc: from home-probability position to 0
  const awayStartAngle = homeEndAngle

  return (
    <div className="flex flex-col items-center gap-2">
      <h3 className="text-base font-semibold text-gray-300 uppercase tracking-widest text-center">
        Win Probability
      </h3>

      <div className="relative" style={{ width: size, height: size / 2 + 40 }}>
        <svg
          width={size}
          height={size / 2 + strokeWidth}
          viewBox={`0 0 ${size} ${size / 2 + strokeWidth}`}
          className="overflow-visible"
        >
          <defs>
            <linearGradient id="homeGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor={homeColors.primary} stopOpacity="0.7" />
              <stop offset="100%" stopColor={homeColors.primary} />
            </linearGradient>
            <linearGradient id="awayGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor={awayColors.primary} />
              <stop offset="100%" stopColor={awayColors.primary} stopOpacity="0.7" />
            </linearGradient>
            <filter id="glow">
              <feGaussianBlur stdDeviation="3" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          {/* Background track */}
          <path
            d={describeArc(cx, cy, radius, 180, 0)}
            fill="none"
            stroke="#374151"
            strokeWidth={strokeWidth}
            strokeLinecap="round"
          />

          {/* Home arc */}
          {animatedHome > 0.01 && (
            <path
              d={describeArc(cx, cy, radius, 180, homeEndAngle)}
              fill="none"
              stroke={homeColors.primary}
              strokeWidth={strokeWidth}
              strokeLinecap="round"
              filter="url(#glow)"
            />
          )}

          {/* Away arc */}
          {animatedHome < 0.99 && (
            <path
              d={describeArc(cx, cy, radius, awayStartAngle, 0)}
              fill="none"
              stroke={awayColors.primary}
              strokeWidth={strokeWidth}
              strokeLinecap="round"
              filter="url(#glow)"
            />
          )}

          {/* Needle */}
          <polygon
            points={`${needleTip.x},${needleTip.y} ${needleBase1.x},${needleBase1.y} ${needleBase2.x},${needleBase2.y}`}
            fill="#F9FAFB"
            opacity="0.95"
            style={{ filter: 'drop-shadow(0 0 4px rgba(255,255,255,0.4))' }}
          />

          {/* Center hub */}
          <circle cx={cx} cy={cy} r={10} fill="#1F2937" stroke="#6B7280" strokeWidth={2} />
        </svg>

        {/* Labels */}
        <div
          className="absolute bottom-0 left-0 text-center"
          style={{ width: 70 }}
        >
          <div
            className="text-xs font-bold uppercase tracking-wide"
            style={{ color: homeColors.primary }}
          >
            {homeTeam}
          </div>
          <div className="text-lg font-black text-white">
            {(animatedHome * 100).toFixed(0)}%
          </div>
        </div>

        <div
          className="absolute bottom-0 right-0 text-center"
          style={{ width: 70 }}
        >
          <div
            className="text-xs font-bold uppercase tracking-wide"
            style={{ color: awayColors.primary }}
          >
            {awayTeam}
          </div>
          <div className="text-lg font-black text-white">
            {((1 - animatedHome) * 100).toFixed(0)}%
          </div>
        </div>
      </div>

      {/* Winner badge */}
      <div
        className="px-4 py-1.5 rounded-full text-sm font-bold uppercase tracking-widest"
        style={{
          backgroundColor: hexToRgba(
            winner === 'home' ? homeColors.primary : awayColors.primary,
            0.2
          ),
          border: `1px solid ${winner === 'home' ? homeColors.primary : awayColors.primary}`,
          color: winner === 'home' ? homeColors.primary : awayColors.primary,
        }}
      >
        {winner === 'home' ? homeTeam : awayTeam} Favored
      </div>
    </div>
  )
}
