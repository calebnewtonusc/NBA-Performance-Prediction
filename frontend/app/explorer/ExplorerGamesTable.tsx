'use client'

import { Game } from '@/lib/api-client'

interface ExplorerGamesTableProps {
  sortedGames: Game[]
  sortColumn: string
  sortDirection: 'asc' | 'desc'
  currentPage: number
  pageSize: number
  totalGames: number
  loading: boolean
  onSort: (column: string) => void
  onPageSizeChange: (size: number) => void
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString()
}

export function ExplorerGamesTable({
  sortedGames,
  sortColumn,
  sortDirection,
  currentPage,
  pageSize,
  totalGames,
  loading,
  onSort,
  onPageSizeChange,
}: ExplorerGamesTableProps) {
  return (
    <>
      <div className="p-4 md:p-6 border-b border-gray-700 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <h2 className="text-xl md:text-2xl font-bold">Games</h2>
        <div className="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-4 w-full sm:w-auto">
          <div className="text-xs sm:text-sm text-gray-400">
            Showing {(currentPage - 1) * pageSize + 1}-{Math.min(currentPage * pageSize, totalGames)} of {totalGames}
          </div>
          <select
            value={pageSize}
            onChange={(e) => onPageSizeChange(Number(e.target.value))}
            className="w-full sm:w-auto px-3 py-2 bg-background border border-gray-600 rounded text-sm"
            aria-label="Results per page"
          >
            <option value={10}>10 per page</option>
            <option value={25}>25 per page</option>
            <option value={50}>50 per page</option>
            <option value={100}>100 per page</option>
          </select>
        </div>
      </div>

      {/* Desktop Table View */}
      <div className="hidden md:block overflow-x-auto">
        <table className="w-full">
          <thead className="bg-background">
            <tr>
              <th
                onClick={() => onSort('date')}
                className="px-6 py-3 text-left text-sm font-semibold cursor-pointer hover:bg-gray-700"
              >
                Date {sortColumn === 'date' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th
                onClick={() => onSort('home_team')}
                className="px-6 py-3 text-left text-sm font-semibold cursor-pointer hover:bg-gray-700"
              >
                Home Team {sortColumn === 'home_team' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th className="px-6 py-3 text-center text-sm font-semibold">Score</th>
              <th
                onClick={() => onSort('away_team')}
                className="px-6 py-3 text-left text-sm font-semibold cursor-pointer hover:bg-gray-700"
              >
                Away Team {sortColumn === 'away_team' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th
                onClick={() => onSort('score')}
                className="px-6 py-3 text-center text-sm font-semibold cursor-pointer hover:bg-gray-700"
              >
                Total {sortColumn === 'score' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th className="px-6 py-3 text-center text-sm font-semibold">Winner</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700">
            {sortedGames.map((game) => (
              <tr key={game.id} className="hover:bg-background transition-colors">
                <td className="px-6 py-4 text-sm">{formatDate(game.date)}</td>
                <td className="px-6 py-4">
                  <div className="font-semibold">{game.home_team.abbreviation}</div>
                  <div className="text-xs text-gray-500">{game.home_team.full_name}</div>
                </td>
                <td className="px-6 py-4 text-center">
                  <span className={game.home_team_score > game.visitor_team_score ? 'font-bold' : ''}>
                    {game.home_team_score}
                  </span>
                  {' - '}
                  <span className={game.visitor_team_score > game.home_team_score ? 'font-bold' : ''}>
                    {game.visitor_team_score}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <div className="font-semibold">{game.visitor_team.abbreviation}</div>
                  <div className="text-xs text-gray-500">{game.visitor_team.full_name}</div>
                </td>
                <td className="px-6 py-4 text-center text-sm">{game.total_points}</td>
                <td className="px-6 py-4 text-center">
                  {game.winner === 'home' && (
                    <span className="text-xs px-2 py-1 bg-green-900/40 text-green-500 rounded">
                      {game.home_team.abbreviation}
                    </span>
                  )}
                  {game.winner === 'away' && (
                    <span className="text-xs px-2 py-1 bg-blue-900/40 text-blue-500 rounded">
                      {game.visitor_team.abbreviation}
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile Card View */}
      <div className="md:hidden p-4 space-y-4">
        {sortedGames.map((game) => (
          <div key={game.id} className="bg-background p-4 rounded-lg border border-gray-600 space-y-3">
            <div className="flex justify-between items-start">
              <div className="text-sm text-gray-400">{formatDate(game.date)}</div>
              {game.winner === 'home' && (
                <span className="text-xs px-2 py-1 bg-green-900/40 text-green-500 rounded">
                  {game.home_team.abbreviation}
                </span>
              )}
              {game.winner === 'away' && (
                <span className="text-xs px-2 py-1 bg-blue-900/40 text-blue-500 rounded">
                  {game.visitor_team.abbreviation}
                </span>
              )}
            </div>

            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="font-bold text-lg">{game.home_team.abbreviation}</div>
                <div className="text-xs text-gray-500 truncate">{game.home_team.full_name}</div>
              </div>

              <div className="px-3 text-center">
                <div className={`text-2xl font-bold ${game.home_team_score > game.visitor_team_score ? 'text-primary' : ''}`}>
                  {game.home_team_score}
                </div>
              </div>

              <div className="text-center text-gray-500 font-bold px-2">-</div>

              <div className="px-3 text-center">
                <div className={`text-2xl font-bold ${game.visitor_team_score > game.home_team_score ? 'text-primary' : ''}`}>
                  {game.visitor_team_score}
                </div>
              </div>

              <div className="flex-1 text-right">
                <div className="font-bold text-lg">{game.visitor_team.abbreviation}</div>
                <div className="text-xs text-gray-500 truncate">{game.visitor_team.full_name}</div>
              </div>
            </div>

            <div className="text-center text-sm text-gray-400 pt-2 border-t border-gray-700">
              Total Points: {game.total_points}
            </div>
          </div>
        ))}
      </div>
    </>
  )
}
