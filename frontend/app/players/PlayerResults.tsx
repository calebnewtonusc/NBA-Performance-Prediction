'use client'

import { Player } from '@/lib/api-client'
import { DataFreshnessIndicator } from '@/components/DataFreshnessIndicator'
import { PlayerAvatar } from '@/components/TeamAvatar'
import { getTeamColors, hexToRgba } from '@/lib/nba-teams'
import { CheckCircle2 } from 'lucide-react'

interface PlayerResultsProps {
  searchResults: Player[]
  selectedPlayer: Player | null
  dataSource?: string
  timestamp?: string
  onSelectPlayer: (player: Player) => void
  getPlayerHeight: (player: Player) => string
}

const POSITION_COLORS: Record<string, string> = {
  G: '#3B82F6',
  F: '#10B981',
  C: '#F59E0B',
  'G-F': '#8B5CF6',
  'F-G': '#8B5CF6',
  'F-C': '#EF4444',
  'C-F': '#EF4444',
}

export function PlayerResults({
  searchResults,
  selectedPlayer,
  dataSource,
  timestamp,
  onSelectPlayer,
  getPlayerHeight,
}: PlayerResultsProps) {
  if (searchResults.length === 0) return null

  return (
    <div className="bg-secondary rounded-2xl border border-gray-700/50 overflow-hidden">
      <div className="flex items-center justify-between px-6 py-4 border-b border-gray-700/50">
        <div className="flex items-center gap-2">
          <h2 className="text-base font-bold text-white">Search Results</h2>
          <span
            className="text-xs font-bold px-2 py-0.5 rounded-full bg-primary/15 text-primary border border-primary/20"
          >
            {searchResults.length}
          </span>
        </div>
        <DataFreshnessIndicator dataSource={dataSource} timestamp={timestamp} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 p-4 max-h-96 overflow-y-auto">
        {searchResults.map((player) => {
          const isSelected = selectedPlayer?.id === player.id
          const teamAbbr = player.team?.abbreviation
          const colors = teamAbbr ? getTeamColors(teamAbbr) : null
          const posColor = POSITION_COLORS[player.position] || '#6B7280'

          return (
            <button
              key={player.id}
              onClick={() => onSelectPlayer(player)}
              className="text-left p-4 rounded-xl border transition-all duration-200 hover:-translate-y-0.5 relative"
              style={isSelected ? {
                backgroundColor: hexToRgba(colors?.primary || '#FF6B6B', 0.12),
                borderColor: colors?.primary || '#FF6B6B',
                boxShadow: `0 0 12px ${hexToRgba(colors?.primary || '#FF6B6B', 0.2)}`,
              } : {
                backgroundColor: 'rgba(31,41,55,0.4)',
                borderColor: 'rgba(55,65,81,0.5)',
              }}
            >
              {isSelected && (
                <div className="absolute top-2 right-2">
                  <CheckCircle2
                    className="w-4 h-4"
                    style={{ color: colors?.primary || '#FF6B6B' }}
                  />
                </div>
              )}

              <div className="flex items-center gap-3 mb-2">
                <PlayerAvatar
                  firstName={player.first_name}
                  lastName={player.last_name}
                  teamAbbr={teamAbbr}
                  size="md"
                />
                <div className="flex-1 min-w-0">
                  <div className="font-bold text-white text-sm leading-tight truncate">
                    {player.first_name} {player.last_name}
                  </div>
                  {teamAbbr && (
                    <div
                      className="text-xs font-bold mt-0.5"
                      style={{ color: colors?.primary || '#9CA3AF' }}
                    >
                      {teamAbbr}
                    </div>
                  )}
                </div>
              </div>

              <div className="flex items-center gap-2 flex-wrap">
                {player.position && (
                  <span
                    className="text-xs font-bold px-1.5 py-0.5 rounded"
                    style={{
                      backgroundColor: `${posColor}18`,
                      color: posColor,
                      border: `1px solid ${posColor}30`,
                    }}
                  >
                    {player.position}
                  </span>
                )}
                <span className="text-xs text-gray-500 truncate">
                  {player.team?.name || 'Free Agent'}
                </span>
              </div>

              <div className="text-xs text-gray-600 mt-1.5">
                {getPlayerHeight(player)}
                {player.weight_pounds ? ` · ${player.weight_pounds} lbs` : ''}
              </div>
            </button>
          )
        })}
      </div>
    </div>
  )
}
