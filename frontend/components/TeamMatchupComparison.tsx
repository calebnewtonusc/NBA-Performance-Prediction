'use client'

import { getTeamColors, getTeamInfo, hexToRgba } from '@/lib/nba-teams'
import { TeamAvatar } from './TeamAvatar'

interface TeamStat {
  label: string
  home: number
  away: number
  format?: 'pct' | 'pts' | 'number'
  higherIsBetter?: boolean
}

interface TeamMatchupComparisonProps {
  homeTeam: string
  awayTeam: string
  stats?: TeamStat[]
}

const DEFAULT_STATS: TeamStat[] = [
  { label: 'Win %', home: 0.58, away: 0.52, format: 'pct', higherIsBetter: true },
  { label: 'PPG', home: 114.2, away: 111.8, format: 'pts', higherIsBetter: true },
  { label: 'Opp PPG', home: 108.5, away: 112.1, format: 'pts', higherIsBetter: false },
  { label: 'Point Diff', home: 5.7, away: -0.3, format: 'pts', higherIsBetter: true },
  { label: 'Home W%', home: 0.68, away: 0.44, format: 'pct', higherIsBetter: true },
]

function StatRow({
  stat,
  homeColors,
  awayColors,
}: {
  stat: TeamStat
  homeColors: ReturnType<typeof getTeamColors>
  awayColors: ReturnType<typeof getTeamColors>
}) {
  const { label, home, away, format, higherIsBetter = true } = stat
  const homeWins = higherIsBetter ? home >= away : home <= away
  const awayWins = higherIsBetter ? away > home : away < home

  const formatVal = (v: number) => {
    if (format === 'pct') return `${(v * 100).toFixed(0)}%`
    if (format === 'pts') return v > 0 ? `+${v.toFixed(1)}` : v.toFixed(1)
    return v.toFixed(1)
  }

  // Bar widths: normalize based on the two values
  const total = Math.abs(home) + Math.abs(away) || 1
  const homeBarPct = (Math.abs(home) / total) * 50
  const awayBarPct = (Math.abs(away) / total) * 50

  return (
    <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-2 py-2">
      {/* Home value */}
      <div className="flex items-center gap-2 justify-end">
        <span
          className="text-sm font-bold tabular-nums"
          style={{ color: homeWins ? homeColors.primary : '#9CA3AF' }}
        >
          {formatVal(home)}
        </span>
        <div
          className="h-1.5 rounded-l-full"
          style={{
            width: `${homeBarPct}%`,
            minWidth: 8,
            backgroundColor: homeWins ? homeColors.primary : '#374151',
            opacity: homeWins ? 1 : 0.5,
          }}
        />
      </div>

      {/* Label */}
      <div className="text-center text-xs font-semibold text-gray-400 uppercase tracking-wider w-20">
        {label}
      </div>

      {/* Away value */}
      <div className="flex items-center gap-2 justify-start">
        <div
          className="h-1.5 rounded-r-full"
          style={{
            width: `${awayBarPct}%`,
            minWidth: 8,
            backgroundColor: awayWins ? awayColors.primary : '#374151',
            opacity: awayWins ? 1 : 0.5,
          }}
        />
        <span
          className="text-sm font-bold tabular-nums"
          style={{ color: awayWins ? awayColors.primary : '#9CA3AF' }}
        >
          {formatVal(away)}
        </span>
      </div>
    </div>
  )
}

export function TeamMatchupComparison({
  homeTeam,
  awayTeam,
  stats = DEFAULT_STATS,
}: TeamMatchupComparisonProps) {
  const homeColors = getTeamColors(homeTeam)
  const awayColors = getTeamColors(awayTeam)
  const homeInfo = getTeamInfo(homeTeam)
  const awayInfo = getTeamInfo(awayTeam)

  // Count advantages
  const homeAdvantages = stats.filter((s) =>
    (s.higherIsBetter !== false ? s.home >= s.away : s.home <= s.away)
  ).length
  const awayAdvantages = stats.length - homeAdvantages

  return (
    <div
      className="rounded-2xl border overflow-hidden"
      style={{
        background: `linear-gradient(135deg, ${hexToRgba(homeColors.primary, 0.05)}, #0E1117, ${hexToRgba(awayColors.primary, 0.05)})`,
        borderColor: '#374151',
      }}
    >
      {/* Header */}
      <div className="grid grid-cols-[1fr_auto_1fr] items-center p-4 border-b border-gray-700/50">
        {/* Home team */}
        <div className="flex items-center gap-3">
          <TeamAvatar abbr={homeTeam} size="md" />
          <div>
            <div className="font-black text-white text-sm">{homeTeam}</div>
            <div className="text-xs text-gray-400">{homeInfo?.name}</div>
            <div
              className="text-xs font-bold mt-0.5"
              style={{ color: homeColors.primary }}
            >
              {homeAdvantages}/{stats.length} edges
            </div>
          </div>
        </div>

        <div className="text-center px-2">
          <div className="text-xs text-gray-500 font-semibold uppercase tracking-widest">
            Matchup
          </div>
          <div className="text-lg font-black text-gray-600 mt-0.5">VS</div>
        </div>

        {/* Away team */}
        <div className="flex items-center gap-3 justify-end">
          <div className="text-right">
            <div className="font-black text-white text-sm">{awayTeam}</div>
            <div className="text-xs text-gray-400">{awayInfo?.name}</div>
            <div
              className="text-xs font-bold mt-0.5"
              style={{ color: awayColors.primary }}
            >
              {awayAdvantages}/{stats.length} edges
            </div>
          </div>
          <TeamAvatar abbr={awayTeam} size="md" />
        </div>
      </div>

      {/* Stats */}
      <div className="px-4 py-2 divide-y divide-gray-700/30">
        {stats.map((stat, i) => (
          <StatRow key={i} stat={stat} homeColors={homeColors} awayColors={awayColors} />
        ))}
      </div>

      {/* Summary bar */}
      <div className="p-4 border-t border-gray-700/50">
        <div className="flex items-center gap-2">
          <div
            className="text-xs font-bold"
            style={{ color: homeColors.primary }}
          >
            {homeTeam}
          </div>
          <div className="flex-1 h-2 bg-gray-700 rounded-full overflow-hidden flex">
            <div
              className="h-full rounded-l-full transition-all duration-700"
              style={{
                width: `${(homeAdvantages / stats.length) * 100}%`,
                backgroundColor: homeColors.primary,
              }}
            />
            <div
              className="h-full rounded-r-full transition-all duration-700"
              style={{
                width: `${(awayAdvantages / stats.length) * 100}%`,
                backgroundColor: awayColors.primary,
              }}
            />
          </div>
          <div
            className="text-xs font-bold"
            style={{ color: awayColors.primary }}
          >
            {awayTeam}
          </div>
        </div>
      </div>
    </div>
  )
}
