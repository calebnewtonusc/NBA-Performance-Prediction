'use client'

import { Game } from '@/lib/api-client'
import { getTeamColors, hexToRgba } from '@/lib/nba-teams'
import { ChevronUp, ChevronDown } from 'lucide-react'

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
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

function SortIcon({ column, sortColumn, sortDirection }: { column: string; sortColumn: string; sortDirection: string }) {
  if (sortColumn !== column) return <span className="text-gray-600 ml-1">↕</span>
  return sortDirection === 'asc'
    ? <ChevronUp className="inline w-3 h-3 ml-1 text-primary" />
    : <ChevronDown className="inline w-3 h-3 ml-1 text-primary" />
}

function TeamBadge({ abbr, full }: { abbr: string; full: string }) {
  const colors = getTeamColors(abbr)
  return (
    <div>
      <span
        className="text-xs font-black px-1.5 py-0.5 rounded mr-1"
        style={{
          backgroundColor: hexToRgba(colors.primary, 0.15),
          color: colors.primary,
        }}
      >
        {abbr}
      </span>
      <span className="text-xs text-gray-500 hidden xl:inline">{full.split(' ').slice(-1)[0]}</span>
    </div>
  )
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
  const start = (currentPage - 1) * pageSize + 1
  const end = Math.min(currentPage * pageSize, totalGames)

  return (
    <>
      <div className="px-5 py-4 border-b border-gray-700/50 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div>
          <h2 className="text-base font-bold text-white">Games</h2>
          <p className="text-xs text-gray-500 mt-0.5">
            {totalGames > 0 ? `Showing ${start}–${end} of ${totalGames}` : 'No results'}
          </p>
        </div>
        <select
          value={pageSize}
          onChange={(e) => onPageSizeChange(Number(e.target.value))}
          className="px-3 py-1.5 bg-background border border-gray-600 rounded-lg text-sm font-semibold text-white focus:ring-2 focus:ring-primary focus:outline-none"
          aria-label="Results per page"
        >
          <option value={10}>10 per page</option>
          <option value={25}>25 per page</option>
          <option value={50}>50 per page</option>
          <option value={100}>100 per page</option>
        </select>
      </div>

      {/* Desktop Table */}
      <div className="hidden md:block overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr style={{ backgroundColor: 'rgba(17,24,39,0.6)' }}>
              {[
                { col: 'date', label: 'Date' },
                { col: 'home_team', label: 'Home' },
                { col: null, label: 'Score' },
                { col: 'away_team', label: 'Away' },
                { col: 'score', label: 'Total' },
                { col: null, label: 'Winner' },
              ].map(({ col, label }) => (
                <th
                  key={label}
                  onClick={col ? () => onSort(col) : undefined}
                  className={`px-5 py-3 text-left text-xs font-bold uppercase tracking-widest text-gray-500 ${col ? 'cursor-pointer hover:text-gray-300 transition-colors' : ''}`}
                >
                  {label}
                  {col && (
                    <SortIcon
                      column={col}
                      sortColumn={sortColumn}
                      sortDirection={sortDirection}
                    />
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700/30">
            {sortedGames.map((game) => {
              const homeColors = getTeamColors(game.home_team.abbreviation)
              const awayColors = getTeamColors(game.visitor_team.abbreviation)
              const homeWon = game.home_team_score > game.visitor_team_score

              return (
                <tr
                  key={game.id}
                  className="hover:bg-white/2 transition-colors"
                >
                  <td className="px-5 py-3 text-xs text-gray-400 font-medium whitespace-nowrap">
                    {formatDate(game.date)}
                  </td>
                  <td className="px-5 py-3">
                    <TeamBadge abbr={game.home_team.abbreviation} full={game.home_team.full_name} />
                  </td>
                  <td className="px-5 py-3 text-center whitespace-nowrap">
                    <span
                      className="font-black text-base"
                      style={{ color: homeWon ? homeColors.primary : '#9CA3AF' }}
                    >
                      {game.home_team_score}
                    </span>
                    <span className="text-gray-600 mx-1.5 font-medium">—</span>
                    <span
                      className="font-black text-base"
                      style={{ color: !homeWon ? awayColors.primary : '#9CA3AF' }}
                    >
                      {game.visitor_team_score}
                    </span>
                  </td>
                  <td className="px-5 py-3">
                    <TeamBadge abbr={game.visitor_team.abbreviation} full={game.visitor_team.full_name} />
                  </td>
                  <td className="px-5 py-3 text-center text-sm font-medium text-gray-400">
                    {game.total_points}
                  </td>
                  <td className="px-5 py-3 text-center">
                    {game.winner === 'home' && (
                      <span
                        className="text-xs px-2 py-0.5 rounded-full font-bold"
                        style={{
                          backgroundColor: hexToRgba(homeColors.primary, 0.15),
                          color: homeColors.primary,
                          border: `1px solid ${hexToRgba(homeColors.primary, 0.3)}`,
                        }}
                      >
                        {game.home_team.abbreviation}
                      </span>
                    )}
                    {game.winner === 'away' && (
                      <span
                        className="text-xs px-2 py-0.5 rounded-full font-bold"
                        style={{
                          backgroundColor: hexToRgba(awayColors.primary, 0.15),
                          color: awayColors.primary,
                          border: `1px solid ${hexToRgba(awayColors.primary, 0.3)}`,
                        }}
                      >
                        {game.visitor_team.abbreviation}
                      </span>
                    )}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {/* Mobile Card View */}
      <div className="md:hidden p-4 space-y-3">
        {sortedGames.map((game) => {
          const homeColors = getTeamColors(game.home_team.abbreviation)
          const awayColors = getTeamColors(game.visitor_team.abbreviation)
          const homeWon = game.home_team_score > game.visitor_team_score
          const winnerColors = homeWon ? homeColors : awayColors

          return (
            <div
              key={game.id}
              className="rounded-xl border p-4"
              style={{
                backgroundColor: 'rgba(17,24,39,0.6)',
                borderColor: 'rgba(55,65,81,0.4)',
              }}
            >
              <div className="flex justify-between items-center mb-3">
                <span className="text-xs text-gray-500">{formatDate(game.date)}</span>
                {game.winner && (
                  <span
                    className="text-xs font-bold px-2 py-0.5 rounded-full"
                    style={{
                      backgroundColor: hexToRgba(winnerColors.primary, 0.15),
                      color: winnerColors.primary,
                    }}
                  >
                    W: {homeWon ? game.home_team.abbreviation : game.visitor_team.abbreviation}
                  </span>
                )}
              </div>

              <div className="flex items-center justify-between">
                <div className="text-left">
                  <div
                    className="text-sm font-black"
                    style={{ color: homeWon ? homeColors.primary : '#9CA3AF' }}
                  >
                    {game.home_team.abbreviation}
                  </div>
                  <div className="text-xs text-gray-500">Home</div>
                </div>

                <div className="text-center">
                  <div className="text-xl font-black text-white">
                    <span style={{ color: homeWon ? homeColors.primary : '#9CA3AF' }}>
                      {game.home_team_score}
                    </span>
                    <span className="text-gray-600 mx-1.5">—</span>
                    <span style={{ color: !homeWon ? awayColors.primary : '#9CA3AF' }}>
                      {game.visitor_team_score}
                    </span>
                  </div>
                  <div className="text-xs text-gray-600 mt-0.5">
                    {game.total_points} pts total
                  </div>
                </div>

                <div className="text-right">
                  <div
                    className="text-sm font-black"
                    style={{ color: !homeWon ? awayColors.primary : '#9CA3AF' }}
                  >
                    {game.visitor_team.abbreviation}
                  </div>
                  <div className="text-xs text-gray-500">Away</div>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </>
  )
}
