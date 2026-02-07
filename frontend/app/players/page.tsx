'use client'

import { useState, useEffect } from 'react'
import { toast } from 'sonner'
import { apiClient, Player, PlayerStats } from '@/lib/api-client'
import { SkeletonPlayerGrid, SkeletonText } from '@/components/LoadingSkeleton'
import { InfoTooltip } from '@/components/InfoTooltip'
import { DataFreshnessIndicator } from '@/components/DataFreshnessIndicator'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from '@/components/LazyChart'

const FEATURED_PLAYERS = [
  { name: 'LeBron James', id: 237 },
  { name: 'Stephen Curry', id: 124 },
  { name: 'Kevin Durant', id: 140 },
  { name: 'Giannis Antetokounmpo', id: 15 },
  { name: 'Luka Doncic', id: 154 },
  { name: 'Joel Embiid', id: 162 },
]

export default function Players() {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<Player[]>([])
  const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null)
  const [playerStats, setPlayerStats] = useState<PlayerStats | null>(null)
  const [selectedSeason, setSelectedSeason] = useState('2024')
  const [loading, setLoading] = useState(false)
  const [statsLoading, setStatsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [recentSearches, setRecentSearches] = useState<string[]>([])
  const [dataSource, setDataSource] = useState<string | undefined>()
  const [timestamp, setTimestamp] = useState<string | undefined>()

  // Load recent searches from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('recentPlayerSearches')
    if (saved) {
      try {
        setRecentSearches(JSON.parse(saved))
      } catch (e) {
        console.error('Failed to parse recent searches', e)
      }
    }
  }, [])

  const addToRecentSearches = (query: string) => {
    const trimmed = query.trim()
    if (!trimmed) return

    // Add to front, remove duplicates, limit to 5
    const updated = [trimmed, ...recentSearches.filter(s => s.toLowerCase() !== trimmed.toLowerCase())].slice(0, 5)
    setRecentSearches(updated)
    localStorage.setItem('recentPlayerSearches', JSON.stringify(updated))
  }

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!searchQuery.trim()) {
      toast.error('Please enter a player name to search')
      return
    }

    setLoading(true)
    setError(null)
    setSearchResults([])
    setSelectedPlayer(null)
    setPlayerStats(null)

    try {
      const response = await apiClient.searchPlayers(searchQuery, 20)
      setSearchResults(response.players)
      setDataSource(response.dataSource)
      setTimestamp(response.timestamp)

      if (response.players.length === 0) {
        toast.info('No players found', {
          description: 'Try searching by first name, last name, or team'
        })
        setError('No players found matching your search')
      } else {
        // Add to recent searches on successful search
        addToRecentSearches(searchQuery)

        toast.success(`Found ${response.players.length} player(s)`, {
          description: `Showing results for "${searchQuery}"`
        })
      }
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to search players'
      setError(errorMessage)
      toast.error('Search failed', {
        description: errorMessage,
        action: {
          label: 'Retry',
          onClick: () => handleSearch(e)
        }
      })
    } finally {
      setLoading(false)
    }
  }

  const handleSelectPlayer = async (player: Player) => {
    setSelectedPlayer(player)
    setStatsLoading(true)
    setError(null)

    try {
      const stats = await apiClient.getPlayerStats(player.id, selectedSeason)
      setPlayerStats(stats)

      if (stats.games_played > 0) {
        toast.success(`Loaded ${player.first_name} ${player.last_name}`, {
          description: `${stats.games_played} games in ${selectedSeason}-${parseInt(selectedSeason.slice(2)) + 1} season`
        })
      }
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to load player stats'
      setError(errorMessage)
      setPlayerStats(null)
      toast.error('Failed to load stats', {
        description: errorMessage
      })
    } finally {
      setStatsLoading(false)
    }
  }

  const handleSeasonChange = async (season: string) => {
    setSelectedSeason(season)
    if (selectedPlayer) {
      setStatsLoading(true)
      setError(null)

      try {
        const stats = await apiClient.getPlayerStats(selectedPlayer.id, season)
        setPlayerStats(stats)

        if (stats.games_played === 0) {
          toast.info('No stats available', {
            description: `${selectedPlayer.first_name} ${selectedPlayer.last_name} has no recorded stats for the ${season}-${parseInt(season.slice(2)) + 1} season`
          })
        }
      } catch (err: any) {
        const errorMessage = err.message || 'Failed to load player stats'
        setError(errorMessage)
        setPlayerStats(null)
        toast.error('Failed to load stats', {
          description: errorMessage
        })
      } finally {
        setStatsLoading(false)
      }
    }
  }

  const getPlayerHeight = (player: Player) => {
    if (player.height_feet && player.height_inches) {
      return `${player.height_feet}'${player.height_inches}"`
    }
    return 'N/A'
  }

  const seasons = ['2024', '2023', '2022', '2021', '2020']

  return (
    <div className="max-w-6xl mx-auto space-y-8" role="main" aria-labelledby="page-title">
      <div>
        <h1 className="text-4xl font-bold" id="page-title">Player Stats</h1>
        <p className="text-gray-400 mt-2">
          Search for players and analyze their performance statistics
        </p>
      </div>

      {/* Search Section */}
      <div className="bg-secondary p-6 rounded-lg border border-gray-700">
        <div className="flex items-center gap-2 mb-4">
          <h2 className="text-2xl font-bold">Search Players</h2>
          <InfoTooltip content="Search by first name, last name, or team. Typos are automatically corrected using fuzzy matching." />
        </div>
        <form onSubmit={handleSearch} className="flex gap-4">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Enter player name (e.g., LeBron James)"
            className="flex-1 px-4 py-3 bg-background border border-gray-600 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary"
            aria-label="Player search"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary/80 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </form>

        {/* Recent Searches */}
        {recentSearches.length > 0 && !loading && searchResults.length === 0 && (
          <div className="mt-4">
            <p className="text-sm text-gray-400 mb-2">Recent Searches:</p>
            <div className="flex flex-wrap gap-2">
              {recentSearches.map((search, index) => (
                <button
                  key={index}
                  onClick={() => {
                    setSearchQuery(search)
                    handleSearch(new Event('submit') as any)
                  }}
                  className="px-3 py-1.5 bg-background border border-gray-600 rounded-full text-sm hover:border-primary hover:text-primary transition-colors"
                >
                  {search}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Featured Players */}
        {!loading && searchResults.length === 0 && !selectedPlayer && (
          <div className="mt-6 pt-6 border-t border-gray-700">
            <p className="text-sm text-gray-400 mb-3">Popular Players:</p>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {FEATURED_PLAYERS.map((player) => (
                <button
                  key={player.id}
                  onClick={() => {
                    setSearchQuery(player.name)
                    handleSearch(new Event('submit') as any)
                  }}
                  className="p-3 bg-background border border-gray-600 rounded-lg hover:border-primary hover:bg-background/80 transition-all text-left"
                >
                  <span className="text-sm font-medium">{player.name}</span>
                </button>
              ))}
            </div>

            <p className="text-xs text-gray-500 mt-4 flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
              Tip: Try searching by first name, last name, or team
            </p>
          </div>
        )}
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-900/20 border border-red-500 rounded-lg p-4" role="alert">
          <p className="text-red-400">{error}</p>
        </div>
      )}

      {/* Search Results */}
      {searchResults.length > 0 && (
        <div className="bg-secondary p-6 rounded-lg border border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold">Search Results ({searchResults.length})</h2>
            <DataFreshnessIndicator dataSource={dataSource} timestamp={timestamp} />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-h-96 overflow-y-auto">
            {searchResults.map((player) => (
              <button
                key={player.id}
                onClick={() => handleSelectPlayer(player)}
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
      )}

      {/* Selected Player Details */}
      {selectedPlayer && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Player Info */}
          <div className="bg-secondary p-6 rounded-lg border border-gray-700">
            <h2 className="text-2xl font-bold mb-4">Player Information</h2>
            <div className="space-y-3">
              <div>
                <p className="text-sm text-gray-400">Full Name</p>
                <p className="text-xl font-semibold">
                  {selectedPlayer.first_name} {selectedPlayer.last_name}
                </p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-400">Position</p>
                  <p className="text-lg font-semibold">{selectedPlayer.position || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Team</p>
                  <p className="text-lg font-semibold">
                    {selectedPlayer.team?.abbreviation || 'FA'}
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-400">Height</p>
                  <p className="text-lg font-semibold">{getPlayerHeight(selectedPlayer)}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Weight</p>
                  <p className="text-lg font-semibold">
                    {selectedPlayer.weight_pounds ? `${selectedPlayer.weight_pounds} lbs` : 'N/A'}
                  </p>
                </div>
              </div>
              {selectedPlayer.team && (
                <div>
                  <p className="text-sm text-gray-400">Team Details</p>
                  <p className="text-base">
                    {selectedPlayer.team.full_name}
                  </p>
                  <p className="text-sm text-gray-500">
                    {selectedPlayer.team.conference} Conference | {selectedPlayer.team.division} Division
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Season Selector & Stats */}
          <div className="bg-secondary p-6 rounded-lg border border-gray-700">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold">Season Statistics</h2>
              <select
                value={selectedSeason}
                onChange={(e) => handleSeasonChange(e.target.value)}
                className="px-3 py-2 bg-background border border-gray-600 rounded focus:ring-2 focus:ring-primary"
                aria-label="Select season"
              >
                {seasons.map((season) => (
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
        </div>
      )}

      {/* Stats Chart */}
      {selectedPlayer && playerStats && playerStats.games_played > 0 && playerStats.averages && (
        <div className="bg-secondary p-6 rounded-lg border border-gray-700">
          <h2 className="text-2xl font-bold mb-4">Season Averages Breakdown</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={[
                { name: 'Points', value: playerStats.averages.pts || 0 },
                { name: 'Rebounds', value: playerStats.averages.reb || 0 },
                { name: 'Assists', value: playerStats.averages.ast || 0 },
                { name: 'Steals', value: playerStats.averages.stl || 0 },
                { name: 'Blocks', value: playerStats.averages.blk || 0 },
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
                formatter={(value: any) => value.toFixed(1)}
              />
              <Bar dataKey="value" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
