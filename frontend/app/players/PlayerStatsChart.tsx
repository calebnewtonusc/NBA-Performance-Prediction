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
} from '@/components/LazyChart'

interface PlayerStatsChartProps {
  playerStats: PlayerStats
}

export function PlayerStatsChart({ playerStats }: PlayerStatsChartProps) {
  if (!playerStats.averages) return null

  const chartData = [
    { name: 'Points', value: playerStats.averages.pts || 0 },
    { name: 'Rebounds', value: playerStats.averages.reb || 0 },
    { name: 'Assists', value: playerStats.averages.ast || 0 },
    { name: 'Steals', value: playerStats.averages.stl || 0 },
    { name: 'Blocks', value: playerStats.averages.blk || 0 },
  ]

  return (
    <div className="bg-secondary p-6 rounded-lg border border-gray-700">
      <h2 className="text-2xl font-bold mb-4">Season Averages Breakdown</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis dataKey="name" stroke="#9CA3AF" />
          <YAxis stroke="#9CA3AF" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1F2937',
              border: '1px solid #374151',
            }}
            formatter={(value: any) => value.toFixed(1)}
          />
          <Bar dataKey="value" fill="#3B82F6" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
