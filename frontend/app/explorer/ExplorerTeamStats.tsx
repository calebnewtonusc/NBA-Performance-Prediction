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
} from '@/components/LazyChart'

interface ExplorerTeamStatsProps {
  teamStats: TeamStats
}

export function ExplorerTeamStats({ teamStats }: ExplorerTeamStatsProps) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="bg-secondary p-6 rounded-lg border border-gray-700">
        <h2 className="text-2xl font-bold mb-4">Team Statistics</h2>
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-gray-400">Team:</span>
            <span className="text-xl font-semibold">{teamStats.team}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-400">Season:</span>
            <span className="text-xl font-semibold">
              {teamStats.season}-{parseInt(teamStats.season.slice(2)) + 1}
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-400">Games Played:</span>
            <span className="text-xl font-semibold">{teamStats.games_played}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-400">Wins:</span>
            <span className="text-xl font-semibold text-green-500">{teamStats.wins}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-400">Losses:</span>
            <span className="text-xl font-semibold text-red-500">{teamStats.losses}</span>
          </div>
          <div className="flex justify-between items-center pt-3 border-t border-gray-600">
            <span className="text-gray-400">Win Percentage:</span>
            <span className="text-2xl font-bold text-primary">
              {(teamStats.win_percentage * 100).toFixed(1)}%
            </span>
          </div>
        </div>
      </div>

      <div className="bg-secondary p-6 rounded-lg border border-gray-700">
        <h2 className="text-2xl font-bold mb-4">Record Chart</h2>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart
            data={[
              { name: 'Wins', value: teamStats.wins, fill: '#10B981' },
              { name: 'Losses', value: teamStats.losses, fill: '#EF4444' },
            ]}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="name" stroke="#9CA3AF" />
            <YAxis stroke="#9CA3AF" />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1F2937',
                border: '1px solid #374151',
              }}
            />
            <Bar dataKey="value" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
