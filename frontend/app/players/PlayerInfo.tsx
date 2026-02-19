'use client'

import { Player } from '@/lib/api-client'

interface PlayerInfoProps {
  player: Player
  getPlayerHeight: (player: Player) => string
}

export function PlayerInfo({ player, getPlayerHeight }: PlayerInfoProps) {
  return (
    <div className="bg-secondary p-6 rounded-lg border border-gray-700">
      <h2 className="text-2xl font-bold mb-4">Player Information</h2>
      <div className="space-y-3">
        <div>
          <p className="text-sm text-gray-400">Full Name</p>
          <p className="text-xl font-semibold">
            {player.first_name} {player.last_name}
          </p>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-400">Position</p>
            <p className="text-lg font-semibold">{player.position || 'N/A'}</p>
          </div>
          <div>
            <p className="text-sm text-gray-400">Team</p>
            <p className="text-lg font-semibold">{player.team?.abbreviation || 'FA'}</p>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-400">Height</p>
            <p className="text-lg font-semibold">{getPlayerHeight(player)}</p>
          </div>
          <div>
            <p className="text-sm text-gray-400">Weight</p>
            <p className="text-lg font-semibold">
              {player.weight_pounds ? `${player.weight_pounds} lbs` : 'N/A'}
            </p>
          </div>
        </div>
        {player.team && (
          <div>
            <p className="text-sm text-gray-400">Team Details</p>
            <p className="text-base">{player.team.full_name}</p>
            <p className="text-sm text-gray-500">
              {player.team.conference} Conference | {player.team.division} Division
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
