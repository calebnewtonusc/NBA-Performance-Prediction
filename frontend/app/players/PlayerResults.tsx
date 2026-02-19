'use client'

import { Player } from '@/lib/api-client'
import { DataFreshnessIndicator } from '@/components/DataFreshnessIndicator'

interface PlayerResultsProps {
  searchResults: Player[]
  selectedPlayer: Player | null
  dataSource?: string
  timestamp?: string
  onSelectPlayer: (player: Player) => void
  getPlayerHeight: (player: Player) => string
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
    <div className="bg-secondary p-6 rounded-lg border border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold">Search Results ({searchResults.length})</h2>
        <DataFreshnessIndicator dataSource={dataSource} timestamp={timestamp} />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-h-96 overflow-y-auto">
        {searchResults.map((player) => (
          <button
            key={player.id}
            onClick={() => onSelectPlayer(player)}
            className={`text-left p-4 rounded-lg border transition-colors ${
              selectedPlayer?.id === player.id
                ? 'border-primary bg-primary/10'
                : 'border-gray-600 hover:border-gray-500'
            }`}
          >
            <h3 className="font-semibold text-lg">
              {player.first_name} {player.last_name}
            </h3>
            <p className="text-sm text-gray-400 mt-1">
              {player.position} | {player.team?.full_name || 'Free Agent'}
            </p>
            <p className="text-xs text-gray-500 mt-1">
              {getPlayerHeight(player)} | {player.weight_pounds ? `${player.weight_pounds} lbs` : 'N/A'}
            </p>
          </button>
        ))}
      </div>
    </div>
  )
}
