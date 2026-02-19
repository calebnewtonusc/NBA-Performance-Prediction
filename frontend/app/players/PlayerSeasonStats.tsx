'use client'

import { PlayerStats } from '@/lib/api-client'

const SEASONS = ['2024', '2023', '2022', '2021', '2020']

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
  return (
    <div className="bg-secondary p-6 rounded-lg border border-gray-700">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Season Statistics</h2>
        <select
          value={selectedSeason}
          onChange={(e) => onSeasonChange(e.target.value)}
          className="px-3 py-2 bg-background border border-gray-600 rounded focus:ring-2 focus:ring-primary"
          aria-label="Select season"
        >
          {SEASONS.map((season) => (
            <option key={season} value={season}>
              {season}-{parseInt(season.slice(2)) + 1}
            </option>
          ))}
        </select>
      </div>

      {statsLoading ? (
        <div className="text-center py-8">
          <p className="text-gray-400">Loading stats...</p>
        </div>
      ) : playerStats && playerStats.games_played > 0 ? (
        <div className="space-y-4">
          <div>
            <p className="text-sm text-gray-400 mb-2">Games Played</p>
            <p className="text-2xl font-bold">{playerStats.games_played}</p>
          </div>
          {playerStats.averages && (
            <div className="grid grid-cols-2 gap-3">
              {playerStats.averages.pts !== undefined && (
                <div>
                  <p className="text-sm text-gray-400">PPG</p>
                  <p className="text-xl font-semibold">{playerStats.averages.pts.toFixed(1)}</p>
                </div>
              )}
              {playerStats.averages.reb !== undefined && (
                <div>
                  <p className="text-sm text-gray-400">RPG</p>
                  <p className="text-xl font-semibold">{playerStats.averages.reb.toFixed(1)}</p>
                </div>
              )}
              {playerStats.averages.ast !== undefined && (
                <div>
                  <p className="text-sm text-gray-400">APG</p>
                  <p className="text-xl font-semibold">{playerStats.averages.ast.toFixed(1)}</p>
                </div>
              )}
              {playerStats.averages.stl !== undefined && (
                <div>
                  <p className="text-sm text-gray-400">SPG</p>
                  <p className="text-xl font-semibold">{playerStats.averages.stl.toFixed(1)}</p>
                </div>
              )}
              {playerStats.averages.blk !== undefined && (
                <div>
                  <p className="text-sm text-gray-400">BPG</p>
                  <p className="text-xl font-semibold">{playerStats.averages.blk.toFixed(1)}</p>
                </div>
              )}
              {playerStats.averages.fg_pct !== undefined && (
                <div>
                  <p className="text-sm text-gray-400">FG%</p>
                  <p className="text-xl font-semibold">
                    {(playerStats.averages.fg_pct * 100).toFixed(1)}%
                  </p>
                </div>
              )}
              {playerStats.averages.fg3_pct !== undefined && (
                <div>
                  <p className="text-sm text-gray-400">3P%</p>
                  <p className="text-xl font-semibold">
                    {(playerStats.averages.fg3_pct * 100).toFixed(1)}%
                  </p>
                </div>
              )}
              {playerStats.averages.ft_pct !== undefined && (
                <div>
                  <p className="text-sm text-gray-400">FT%</p>
                  <p className="text-xl font-semibold">
                    {(playerStats.averages.ft_pct * 100).toFixed(1)}%
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-gray-400">
            No stats available for the {selectedSeason}-{parseInt(selectedSeason.slice(2)) + 1} season
          </p>
        </div>
      )}
    </div>
  )
}
