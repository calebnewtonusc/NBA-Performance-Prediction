'use client'

import { PlayerStats } from '@/lib/api-client'
import { AnimatedCounter, TrendIndicator } from '@/components/AnimatedCounter'
import { ChartSkeleton } from '@/components/SkeletonLoader'

const SEASONS = ['2024', '2023', '2022', '2021', '2020']

interface StatBlockProps {
  label: string
  value: number
  format?: 'decimal' | 'pct'
  accentColor?: string
  trend?: number
}

function StatBlock({ label, value, format = 'decimal', accentColor = '#FF6B6B', trend }: StatBlockProps) {
  const displayValue = format === 'pct' ? value * 100 : value

  return (
    <div
      className="rounded-xl p-3 border transition-colors"
      style={{
        backgroundColor: `${accentColor}0a`,
        borderColor: `${accentColor}20`,
      }}
    >
      <div className="text-xs font-bold uppercase tracking-widest mb-1" style={{ color: accentColor }}>
        {label}
      </div>
      <div className="flex items-end gap-1.5">
        <div className="text-2xl font-black text-white">
          <AnimatedCounter
            value={displayValue}
            decimals={1}
            suffix={format === 'pct' ? '%' : ''}
            duration={900}
          />
        </div>
        {trend !== undefined && (
          <div className="mb-0.5">
            <TrendIndicator value={displayValue} previousValue={displayValue - trend} threshold={0.05} />
          </div>
        )}
      </div>
    </div>
  )
}

interface PlayerSeasonStatsProps {
  selectedSeason: string
  statsLoading: boolean
  playerStats: PlayerStats | null
  onSeasonChange: (season: string) => void
}

export function PlayerSeasonStats({
  selectedSeason,
  statsLoading,
  playerStats,
  onSeasonChange,
}: PlayerSeasonStatsProps) {
  const avg = playerStats?.averages

  // Simulated trend values (small deltas for demonstration)
  const trends = {
    pts: 1.2,
    reb: -0.3,
    ast: 0.7,
    stl: 0.1,
    blk: -0.1,
  }

  return (
    <div className="bg-secondary rounded-2xl border border-gray-700/50 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-gray-700/50">
        <div>
          <h2 className="text-base font-bold text-white">Season Statistics</h2>
          <p className="text-xs text-gray-500 mt-0.5">Per game averages</p>
        </div>
        <select
          value={selectedSeason}
          onChange={(e) => onSeasonChange(e.target.value)}
          className="px-3 py-1.5 bg-background border border-gray-600 rounded-lg text-sm font-semibold text-white focus:ring-2 focus:ring-primary focus:border-primary focus:outline-none transition-colors"
          aria-label="Select season"
        >
          {SEASONS.map((season) => (
            <option key={season} value={season}>
              {season}-{parseInt(season.slice(2)) + 1}
            </option>
          ))}
        </select>
      </div>

      <div className="p-6">
        {statsLoading ? (
          <div className="space-y-3">
            {/* Games played skeleton */}
            <div className="h-16 bg-gray-700/50 rounded-xl animate-pulse" />
            {/* Stat grid skeleton */}
            <div className="grid grid-cols-2 gap-3">
              {(['sk-a', 'sk-b', 'sk-c', 'sk-d', 'sk-e', 'sk-f']).map((id) => (
                <div key={id} className="h-20 bg-gray-700/50 rounded-xl animate-pulse" />
              ))}
            </div>
          </div>
        ) : playerStats && playerStats.games_played > 0 ? (
          <div className="space-y-4">
            {/* Games played highlight */}
            <div className="flex items-center gap-3 p-3 bg-gray-700/30 rounded-xl border border-gray-600/30">
              <div>
                <div className="text-xs font-bold text-gray-500 uppercase tracking-widest">Games Played</div>
                <div className="text-3xl font-black text-white">
                  <AnimatedCounter value={playerStats.games_played} duration={800} />
                </div>
              </div>
              <div className="ml-auto text-right">
                <div className="text-xs text-gray-500">
                  {selectedSeason}-{parseInt(selectedSeason.slice(2)) + 1} Season
                </div>
                <div className="text-xs font-semibold text-green-400 mt-0.5">
                  {playerStats.games_played >= 40 ? 'Full season' : 'Partial season'}
                </div>
              </div>
            </div>

            {/* Main stats */}
            {avg && (
              <>
                {/* Primary stats */}
                <div className="grid grid-cols-3 gap-3">
                  {avg.pts !== undefined && (
                    <StatBlock label="PPG" value={avg.pts} accentColor="#FF6B6B" trend={trends.pts} />
                  )}
                  {avg.reb !== undefined && (
                    <StatBlock label="RPG" value={avg.reb} accentColor="#3B82F6" trend={trends.reb} />
                  )}
                  {avg.ast !== undefined && (
                    <StatBlock label="APG" value={avg.ast} accentColor="#10B981" trend={trends.ast} />
                  )}
                </div>

                {/* Secondary stats */}
                <div className="grid grid-cols-2 gap-3">
                  {avg.stl !== undefined && (
                    <StatBlock label="SPG" value={avg.stl} accentColor="#F59E0B" trend={trends.stl} />
                  )}
                  {avg.blk !== undefined && (
                    <StatBlock label="BPG" value={avg.blk} accentColor="#8B5CF6" trend={trends.blk} />
                  )}
                </div>

                {/* Shooting splits */}
                {(avg.fg_pct !== undefined || avg.fg3_pct !== undefined || avg.ft_pct !== undefined) && (
                  <div>
                    <div className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">
                      Shooting
                    </div>
                    <div className="grid grid-cols-3 gap-3">
                      {avg.fg_pct !== undefined && (
                        <StatBlock label="FG%" value={avg.fg_pct} format="pct" accentColor="#EF4444" />
                      )}
                      {avg.fg3_pct !== undefined && (
                        <StatBlock label="3P%" value={avg.fg3_pct} format="pct" accentColor="#06B6D4" />
                      )}
                      {avg.ft_pct !== undefined && (
                        <StatBlock label="FT%" value={avg.ft_pct} format="pct" accentColor="#84CC16" />
                      )}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        ) : (
          <div className="text-center py-10">
            <div className="w-12 h-12 bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg className="w-6 h-6 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <p className="text-gray-400 font-medium text-sm">
              No stats for {selectedSeason}-{parseInt(selectedSeason.slice(2)) + 1}
            </p>
            <p className="text-gray-600 text-xs mt-1">Try a different season</p>
          </div>
        )}
      </div>
    </div>
  )
}
