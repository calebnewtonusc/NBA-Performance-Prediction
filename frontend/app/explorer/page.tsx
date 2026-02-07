'use client'

import { useState } from 'react'
import { apiClient, Game, TeamStats } from '@/lib/api-client'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from '@/components/LazyChart'

const NBA_TEAMS = [
  { name: 'All Teams', abbr: '' },
  { name: 'Atlanta Hawks', abbr: 'ATL' },
  { name: 'Boston Celtics', abbr: 'BOS' },
  { name: 'Brooklyn Nets', abbr: 'BKN' },
  { name: 'Charlotte Hornets', abbr: 'CHA' },
  { name: 'Chicago Bulls', abbr: 'CHI' },
  { name: 'Cleveland Cavaliers', abbr: 'CLE' },
  { name: 'Dallas Mavericks', abbr: 'DAL' },
  { name: 'Denver Nuggets', abbr: 'DEN' },
  { name: 'Detroit Pistons', abbr: 'DET' },
  { name: 'Golden State Warriors', abbr: 'GSW' },
  { name: 'Houston Rockets', abbr: 'HOU' },
  { name: 'Indiana Pacers', abbr: 'IND' },
  { name: 'LA Clippers', abbr: 'LAC' },
  { name: 'Los Angeles Lakers', abbr: 'LAL' },
  { name: 'Memphis Grizzlies', abbr: 'MEM' },
  { name: 'Miami Heat', abbr: 'MIA' },
  { name: 'Milwaukee Bucks', abbr: 'MIL' },
  { name: 'Minnesota Timberwolves', abbr: 'MIN' },
  { name: 'New Orleans Pelicans', abbr: 'NOP' },
  { name: 'New York Knicks', abbr: 'NYK' },
  { name: 'Oklahoma City Thunder', abbr: 'OKC' },
  { name: 'Orlando Magic', abbr: 'ORL' },
  { name: 'Philadelphia 76ers', abbr: 'PHI' },
  { name: 'Phoenix Suns', abbr: 'PHX' },
  { name: 'Portland Trail Blazers', abbr: 'POR' },
  { name: 'Sacramento Kings', abbr: 'SAC' },
  { name: 'San Antonio Spurs', abbr: 'SAS' },
  { name: 'Toronto Raptors', abbr: 'TOR' },
  { name: 'Utah Jazz', abbr: 'UTA' },
  { name: 'Washington Wizards', abbr: 'WAS' },
]

export default function Explorer() {
  const [selectedTeam, setSelectedTeam] = useState('')
  const [selectedSeason, setSelectedSeason] = useState('2024')
  const [games, setGames] = useState<Game[]>([])
  const [teamStats, setTeamStats] = useState<TeamStats | null>(null)
  const [sortColumn, setSortColumn] = useState<string>('date')
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const seasons = ['2024', '2023', '2022', '2021', '2020']

  const handleLoadData = async () => {
    setLoading(true)
    setError(null)

    try {
      const filters = {
        team: selectedTeam || undefined,
        season: selectedSeason,
        limit: 100,
      }

      const gamesData = await apiClient.getGames(filters)
      setGames(gamesData)

      // Load team stats if a specific team is selected
      if (selectedTeam) {
        const stats = await apiClient.getTeamStats(selectedTeam, selectedSeason)
        setTeamStats(stats)
      } else {
        setTeamStats(null)
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  const handleSort = (column: string) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortColumn(column)
      setSortDirection('desc')
    }
  }

  const getSortedGames = () => {
    if (!games.length) return []

    const sorted = [...games].sort((a, b) => {
      let aValue: any, bValue: any

      switch (sortColumn) {
        case 'date':
          aValue = new Date(a.date).getTime()
          bValue = new Date(b.date).getTime()
          break
        case 'home_team':
          aValue = a.home_team.abbreviation
          bValue = b.home_team.abbreviation
          break
        case 'away_team':
          aValue = a.visitor_team.abbreviation
          bValue = b.visitor_team.abbreviation
          break
        case 'score':
          aValue = a.total_points || 0
          bValue = b.total_points || 0
          break
        default:
          return 0
      }

      if (sortDirection === 'asc') {
        return aValue > bValue ? 1 : -1
      } else {
        return aValue < bValue ? 1 : -1
      }
    })

    return sorted
  }

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString()
  }

  const sortedGames = getSortedGames()

  return (
    <div className="max-w-6xl mx-auto space-y-8" role="main" aria-labelledby="page-title">
      <div>
        <h1 className="text-4xl font-bold" id="page-title">Data Explorer</h1>
        <p className="text-gray-400 mt-2">
          Explore historical NBA game data and team statistics
        </p>
      </div>

      {/* Filters */}
      <div className="bg-secondary p-6 rounded-lg border border-gray-700">
        <h2 className="text-2xl font-bold mb-4">Filters</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label htmlFor="team-select" className="block text-sm text-gray-400 mb-2">
              Team
            </label>
            <select
              id="team-select"
              value={selectedTeam}
              onChange={(e) => setSelectedTeam(e.target.value)}
              className="w-full px-4 py-3 bg-background border border-gray-600 rounded-lg focus:ring-2 focus:ring-primary"
              aria-label="Select team"
            >
              {NBA_TEAMS.map((team) => (
                <option key={team.abbr} value={team.abbr}>
                  {team.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="season-select" className="block text-sm text-gray-400 mb-2">
              Season
            </label>
            <select
              id="season-select"
              value={selectedSeason}
              onChange={(e) => setSelectedSeason(e.target.value)}
              className="w-full px-4 py-3 bg-background border border-gray-600 rounded-lg focus:ring-2 focus:ring-primary"
              aria-label="Select season"
            >
              {seasons.map((season) => (
                <option key={season} value={season}>
                  {season}-{parseInt(season.slice(2)) + 1}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-end">
            <button
              onClick={handleLoadData}
              disabled={loading}
              className="w-full px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary/80 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Loading...' : 'Load Data'}
            </button>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-900/20 border border-red-500 rounded-lg p-4" role="alert">
          <p className="text-red-400">{error}</p>
        </div>
      )}

      {/* Team Stats (if team selected) */}
      {teamStats && (
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
      )}

      {/* Games Table */}
      {games.length > 0 && (
        <div className="bg-secondary rounded-lg border border-gray-700 overflow-hidden">
          <div className="p-6 border-b border-gray-700">
            <h2 className="text-2xl font-bold">Games ({games.length})</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-background">
                <tr>
                  <th
                    onClick={() => handleSort('date')}
                    className="px-6 py-3 text-left text-sm font-semibold cursor-pointer hover:bg-gray-700"
                  >
                    Date {sortColumn === 'date' && (sortDirection === 'asc' ? '↑' : '↓')}
                  </th>
                  <th
                    onClick={() => handleSort('home_team')}
                    className="px-6 py-3 text-left text-sm font-semibold cursor-pointer hover:bg-gray-700"
                  >
                    Home Team {sortColumn === 'home_team' && (sortDirection === 'asc' ? '↑' : '↓')}
                  </th>
                  <th className="px-6 py-3 text-center text-sm font-semibold">Score</th>
                  <th
                    onClick={() => handleSort('away_team')}
                    className="px-6 py-3 text-left text-sm font-semibold cursor-pointer hover:bg-gray-700"
                  >
                    Away Team {sortColumn === 'away_team' && (sortDirection === 'asc' ? '↑' : '↓')}
                  </th>
                  <th
                    onClick={() => handleSort('score')}
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
        </div>
      )}

      {/* Empty State */}
      {!loading && games.length === 0 && !error && (
        <div className="bg-secondary p-12 rounded-lg border border-gray-700 text-center">
          <p className="text-xl text-gray-400">
            Select filters and click "Load Data" to explore games
          </p>
        </div>
      )}
    </div>
  )
}
