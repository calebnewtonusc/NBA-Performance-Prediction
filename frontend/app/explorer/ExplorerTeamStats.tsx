'use client'

import { TeamStats } from '@/lib/api-client'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from '@/components/LazyChart'
import { TeamAvatar } from '@/components/TeamAvatar'
import { AnimatedCounter } from '@/components/AnimatedCounter'
import { getTeamColors, hexToRgba } from '@/lib/nba-teams'

interface ExplorerTeamStatsProps {
  teamStats: TeamStats
}

export function ExplorerTeamStats({ teamStats }: ExplorerTeamStatsProps) {
  const colors = getTeamColors(teamStats.team)
  const winPct = teamStats.win_percentage * 100

  const chartData = [
    { name: 'Wins', value: teamStats.wins, color: '#10B981' },
    { name: 'Losses', value: teamStats.losses, color: '#EF4444' },
  ]

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Stats Card */}
      <div
        className="rounded-2xl border overflow-hidden"
        style={{
          backgroundColor: hexToRgba(colors.primary, 0.06),
          borderColor: hexToRgba(colors.primary, 0.25),
        }}
      >
        {/* Header */}
        <div
          className="px-6 py-4 border-b flex items-center gap-3"
          style={{ borderColor: hexToRgba(colors.primary, 0.2) }}
        >
          <TeamAvatar abbr={teamStats.team} size="md" />
          <div>
            <h2 className="text-lg font-black text-white">{teamStats.team}</h2>
            <div className="text-xs font-medium text-gray-400">
              {teamStats.season}-{parseInt(teamStats.season.slice(2)) + 1} Season
            </div>
          </div>
          <div
            className="ml-auto text-2xl font-black"
            style={{ color: colors.primary }}
          >
            <AnimatedCounter value={winPct} decimals={1} suffix="%" duration={900} />
          </div>
        </div>

        {/* Stats */}
        <div className="p-6 space-y-3">
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="text-center">
              <div className="text-3xl font-black text-white">
                <AnimatedCounter value={teamStats.games_played} duration={700} />
              </div>
              <div className="text-xs text-gray-500 font-medium mt-0.5">Games</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-black text-green-400">
                <AnimatedCounter value={teamStats.wins} duration={800} />
              </div>
              <div className="text-xs text-gray-500 font-medium mt-0.5">Wins</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-black text-red-400">
                <AnimatedCounter value={teamStats.losses} duration={900} />
              </div>
              <div className="text-xs text-gray-500 font-medium mt-0.5">Losses</div>
            </div>
          </div>

          {/* W/L bar */}
          <div>
            <div className="flex justify-between text-xs text-gray-500 mb-1.5">
              <span className="text-green-400 font-semibold">W {teamStats.wins}</span>
              <span className="font-bold" style={{ color: colors.primary }}>
                {winPct.toFixed(1)}% Win Rate
              </span>
              <span className="text-red-400 font-semibold">L {teamStats.losses}</span>
            </div>
            <div className="h-3 bg-gray-700 rounded-full overflow-hidden flex">
              <div
                className="h-full bg-green-500 rounded-l-full transition-all duration-1000"
                style={{ width: `${winPct}%` }}
              />
              <div
                className="h-full bg-red-500 rounded-r-full transition-all duration-1000"
                style={{ width: `${100 - winPct}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Chart Card */}
      <div className="bg-secondary rounded-2xl border border-gray-700/50 p-5">
        <h2 className="text-base font-bold text-white mb-4">Season Record</h2>
        <ResponsiveContainer width="100%" height={230}>
          <BarChart data={chartData} margin={{ top: 10, right: 10, left: -15, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
            <XAxis
              dataKey="name"
              stroke="#4B5563"
              tick={{ fontWeight: 700, fontSize: 13, fill: '#9CA3AF' }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              stroke="#374151"
              tick={{ fontSize: 10, fill: '#6B7280' }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1a1f2e',
                border: '1px solid #374151',
                borderRadius: 12,
                color: '#F9FAFB',
              }}
            />
            <Bar dataKey="value" radius={[8, 8, 0, 0]} maxBarSize={72}>
              {chartData.map((entry) => (
                <Cell key={entry.name} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
