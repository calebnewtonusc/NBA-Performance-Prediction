'use client'

import { PlayerStats } from '@/lib/api-client'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
} from '@/components/LazyChart'

interface PlayerStatsChartProps {
  playerStats: PlayerStats
  teamAbbr?: string
}

const STAT_COLORS = ['#FF6B6B', '#3B82F6', '#10B981', '#F59E0B', '#8B5CF6']

const STAT_DESCRIPTIONS: Record<string, string> = {
  Points: 'Points per game average this season',
  Rebounds: 'Total rebounds (offensive + defensive) per game',
  Assists: 'Assists per game',
  Steals: 'Steals per game — defensive impact',
  Blocks: 'Blocks per game — rim protection',
}

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload || !payload.length) return null

  const entry = payload[0]
  const color = entry.fill || '#FF6B6B'
  const desc = STAT_DESCRIPTIONS[label] || label

  return (
    <div
      className="rounded-xl border p-3 shadow-xl"
      style={{
        backgroundColor: '#1a1f2e',
        borderColor: color,
        minWidth: 160,
        maxWidth: 200,
      }}
    >
      <div className="flex items-center gap-2 mb-1.5">
        <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: color }} />
        <span className="text-xs font-bold text-white uppercase tracking-wide">{label}</span>
      </div>
      <div className="text-2xl font-black mb-1" style={{ color }}>
        {entry.value.toFixed(1)}
      </div>
      <div className="text-xs text-gray-400 leading-snug">{desc}</div>
    </div>
  )
}

export function PlayerStatsChart({ playerStats, teamAbbr }: PlayerStatsChartProps) {
  if (!playerStats.averages) return null

  const chartData = [
    { name: 'Points', value: playerStats.averages.pts || 0 },
    { name: 'Rebounds', value: playerStats.averages.reb || 0 },
    { name: 'Assists', value: playerStats.averages.ast || 0 },
    { name: 'Steals', value: playerStats.averages.stl || 0 },
    { name: 'Blocks', value: playerStats.averages.blk || 0 },
  ]

  // Radar/spider chart data (normalized 0-100)
  const maxes = { pts: 35, reb: 15, ast: 12, stl: 3, blk: 4 }
  const radarData = [
    { stat: 'Scoring', value: Math.min(((playerStats.averages.pts || 0) / maxes.pts) * 100, 100) },
    { stat: 'Boards', value: Math.min(((playerStats.averages.reb || 0) / maxes.reb) * 100, 100) },
    { stat: 'Playmaking', value: Math.min(((playerStats.averages.ast || 0) / maxes.ast) * 100, 100) },
    { stat: 'Defense', value: Math.min(((playerStats.averages.stl || 0) / maxes.stl) * 100, 100) },
    { stat: 'Rim Prot', value: Math.min(((playerStats.averages.blk || 0) / maxes.blk) * 100, 100) },
  ]

  return (
    <div className="space-y-4">
      {/* Bar chart */}
      <div className="bg-secondary rounded-2xl border border-gray-700/50 p-6">
        <div className="flex items-center justify-between mb-5">
          <div>
            <h2 className="text-base font-bold text-white">Season Averages</h2>
            <p className="text-xs text-gray-500 mt-0.5">Per game statistics</p>
          </div>
          <div className="flex items-center gap-1.5">
            {chartData.map((d, i) => (
              <div key={d.name} className="flex items-center gap-1">
                <div
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: STAT_COLORS[i] }}
                />
              </div>
            ))}
          </div>
        </div>

        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 5 }}>
            <defs>
              {STAT_COLORS.map((color, i) => (
                <linearGradient key={color} id={`barGrad${i}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={color} stopOpacity={0.95} />
                  <stop offset="100%" stopColor={color} stopOpacity={0.4} />
                </linearGradient>
              ))}
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
            <XAxis
              dataKey="name"
              stroke="#4B5563"
              tick={{ fontWeight: 600, fontSize: 11, fill: '#9CA3AF' }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              stroke="#374151"
              tick={{ fontSize: 10, fill: '#6B7280' }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
            <Bar dataKey="value" radius={[8, 8, 0, 0]} maxBarSize={56}>
              {chartData.map((entry, index) => (
                <Cell key={entry.name} fill={`url(#barGrad${index})`} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Shooting splits */}
      {(playerStats.averages.fg_pct !== undefined ||
        playerStats.averages.fg3_pct !== undefined ||
        playerStats.averages.ft_pct !== undefined) && (
        <div className="bg-secondary rounded-2xl border border-gray-700/50 p-6">
          <h2 className="text-base font-bold text-white mb-4">Shooting Splits</h2>
          <div className="grid grid-cols-3 gap-4">
            {playerStats.averages.fg_pct !== undefined && (
              <ShootingSplitBar
                label="FG%"
                value={playerStats.averages.fg_pct}
                color="#FF6B6B"
                description="Field Goal %"
              />
            )}
            {playerStats.averages.fg3_pct !== undefined && (
              <ShootingSplitBar
                label="3P%"
                value={playerStats.averages.fg3_pct}
                color="#3B82F6"
                description="Three Point %"
              />
            )}
            {playerStats.averages.ft_pct !== undefined && (
              <ShootingSplitBar
                label="FT%"
                value={playerStats.averages.ft_pct}
                color="#10B981"
                description="Free Throw %"
              />
            )}
          </div>
        </div>
      )}
    </div>
  )
}

function ShootingSplitBar({
  label,
  value,
  color,
  description,
}: {
  label: string
  value: number
  color: string
  description: string
}) {
  const pct = value * 100
  return (
    <div className="text-center">
      {/* Circular progress ring */}
      <div className="relative inline-flex items-center justify-center mb-2">
        <svg width="72" height="72" className="-rotate-90">
          <circle cx="36" cy="36" r="28" fill="none" stroke="#1F2937" strokeWidth="8" />
          <circle
            cx="36"
            cy="36"
            r="28"
            fill="none"
            stroke={color}
            strokeWidth="8"
            strokeDasharray={`${2 * Math.PI * 28}`}
            strokeDashoffset={`${2 * Math.PI * 28 * (1 - value)}`}
            strokeLinecap="round"
            style={{ transition: 'stroke-dashoffset 1s ease-out', filter: `drop-shadow(0 0 4px ${color}60)` }}
          />
        </svg>
        <div className="absolute text-center">
          <div className="text-sm font-black text-white">{pct.toFixed(0)}%</div>
        </div>
      </div>
      <div className="text-xs font-bold text-white">{label}</div>
      <div className="text-xs text-gray-500">{description}</div>
    </div>
  )
}
