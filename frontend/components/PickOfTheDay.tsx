'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { TeamAvatar } from './TeamAvatar'
import { getTeamColors, getTeamInfo, hexToRgba } from '@/lib/nba-teams'

// Curated featured matchups that rotate daily
const FEATURED_MATCHUPS = [
  { home: 'BOS', away: 'LAL', context: 'Historic rivalry — 17 combined championships', pick: 'BOS', confidence: 67 },
  { home: 'GSW', away: 'MIA', context: 'Western powerhouse hosts Heat at Chase Center', pick: 'GSW', confidence: 62 },
  { home: 'DEN', away: 'MIL', context: 'MVP showdown — altitude advantage for Nuggets', pick: 'DEN', confidence: 59 },
  { home: 'PHX', away: 'NYK', context: 'Desert clash as Suns defend home court', pick: 'PHX', confidence: 61 },
  { home: 'MIA', away: 'CHI', context: 'Southeast division rivalry on South Beach', pick: 'MIA', confidence: 64 },
  { home: 'LAL', away: 'BKN', context: 'Purple and gold look to assert West dominance', pick: 'LAL', confidence: 58 },
  { home: 'DAL', away: 'PHI', context: 'Mavericks host 76ers in cross-conference battle', pick: 'DAL', confidence: 55 },
]

interface PickOfTheDayData {
  home: string
  away: string
  context: string
  pick: string
  confidence: number
}

export function PickOfTheDay() {
  const [matchup, setMatchup] = useState<PickOfTheDayData | null>(null)
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    // Rotate daily based on day of year
    const dayOfYear = Math.floor(
      (Date.now() - new Date(new Date().getFullYear(), 0, 0).getTime()) / 86400000
    )
    const idx = dayOfYear % FEATURED_MATCHUPS.length
    setMatchup(FEATURED_MATCHUPS[idx])
    setIsLoaded(true)
  }, [])

  if (!matchup || !isLoaded) return null

  const homeColors = getTeamColors(matchup.home)
  const awayColors = getTeamColors(matchup.away)
  const homeInfo = getTeamInfo(matchup.home)
  const awayInfo = getTeamInfo(matchup.away)
  const pickColors = matchup.pick === matchup.home ? homeColors : awayColors

  return (
    <div
      className="relative overflow-hidden rounded-2xl border p-6"
      style={{
        background: `linear-gradient(135deg, ${hexToRgba(homeColors.primary, 0.08)}, #1a1f2e, ${hexToRgba(awayColors.primary, 0.08)})`,
        borderColor: hexToRgba(pickColors.primary, 0.4),
      }}
    >
      {/* Ambient glow */}
      <div
        className="absolute top-0 left-0 w-40 h-40 rounded-full blur-3xl opacity-10 pointer-events-none"
        style={{ background: homeColors.primary, transform: 'translate(-30%, -30%)' }}
      />
      <div
        className="absolute bottom-0 right-0 w-40 h-40 rounded-full blur-3xl opacity-10 pointer-events-none"
        style={{ background: awayColors.primary, transform: 'translate(30%, 30%)' }}
      />

      {/* Header */}
      <div className="flex items-center gap-2 mb-5">
        <div
          className="w-2 h-2 rounded-full animate-pulse"
          style={{ backgroundColor: pickColors.primary }}
        />
        <span
          className="text-xs font-bold uppercase tracking-widest"
          style={{ color: pickColors.primary }}
        >
          Pick of the Day
        </span>
        <span className="ml-auto text-xs text-gray-500 font-medium">
          {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
        </span>
      </div>

      {/* Matchup display */}
      <div className="flex items-center justify-between mb-5">
        {/* Home team */}
        <div className="flex flex-col items-center gap-2 flex-1">
          <TeamAvatar abbr={matchup.home} size="lg" />
          <div className="text-center">
            <div className="font-black text-white text-sm">{matchup.home}</div>
            <div className="text-gray-400 text-xs">{homeInfo?.name}</div>
            <div
              className="text-xs font-bold mt-1 px-2 py-0.5 rounded"
              style={{
                color: homeColors.primary,
                backgroundColor: hexToRgba(homeColors.primary, 0.1),
              }}
            >
              Home
            </div>
          </div>
        </div>

        {/* VS divider */}
        <div className="flex flex-col items-center gap-1 px-4">
          <div className="text-2xl font-black text-gray-600">VS</div>
          <div
            className="text-xs font-bold px-3 py-1 rounded-full"
            style={{
              backgroundColor: hexToRgba(pickColors.primary, 0.15),
              color: pickColors.primary,
              border: `1px solid ${hexToRgba(pickColors.primary, 0.3)}`,
            }}
          >
            {matchup.confidence}% pick
          </div>
        </div>

        {/* Away team */}
        <div className="flex flex-col items-center gap-2 flex-1">
          <TeamAvatar abbr={matchup.away} size="lg" />
          <div className="text-center">
            <div className="font-black text-white text-sm">{matchup.away}</div>
            <div className="text-gray-400 text-xs">{awayInfo?.name}</div>
            <div
              className="text-xs font-bold mt-1 px-2 py-0.5 rounded"
              style={{
                color: awayColors.primary,
                backgroundColor: hexToRgba(awayColors.primary, 0.1),
              }}
            >
              Away
            </div>
          </div>
        </div>
      </div>

      {/* Context */}
      <p className="text-gray-400 text-sm text-center mb-5 leading-relaxed italic">
        &ldquo;{matchup.context}&rdquo;
      </p>

      {/* Confidence bar */}
      <div className="mb-5">
        <div className="flex justify-between text-xs text-gray-500 mb-1.5">
          <span>{matchup.away}</span>
          <span className="font-semibold" style={{ color: pickColors.primary }}>
            Model Pick: {matchup.pick}
          </span>
          <span>{matchup.home}</span>
        </div>
        <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-1000"
            style={{
              width: `${matchup.pick === matchup.home ? matchup.confidence : 100 - matchup.confidence}%`,
              background: `linear-gradient(90deg, ${homeColors.primary}, ${hexToRgba(homeColors.primary, 0.7)})`,
              marginLeft:
                matchup.pick === matchup.away
                  ? `${matchup.confidence}%`
                  : undefined,
            }}
          />
        </div>
      </div>

      {/* CTA */}
      <Link
        href={`/predictions?home=${matchup.home}&away=${matchup.away}`}
        className="block w-full text-center py-2.5 px-4 rounded-xl text-sm font-bold transition-all duration-200 hover:opacity-90 hover:-translate-y-0.5"
        style={{
          background: `linear-gradient(135deg, ${pickColors.primary}, ${hexToRgba(pickColors.primary, 0.7)})`,
          color: '#FFFFFF',
          boxShadow: `0 4px 16px ${hexToRgba(pickColors.primary, 0.3)}`,
        }}
      >
        Run Full Prediction
      </Link>
    </div>
  )
}
