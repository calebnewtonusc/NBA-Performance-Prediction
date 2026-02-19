'use client'

import { useReducer, useEffect } from 'react'
import { toast } from 'sonner'
import { apiClient, Player, PlayerStats } from '@/lib/api-client'
import { PlayerSearch } from './PlayerSearch'
import { PlayerResults } from './PlayerResults'
import { PlayerInfo } from './PlayerInfo'
import { PlayerSeasonStats } from './PlayerSeasonStats'
import { PlayerStatsChart } from './PlayerStatsChart'

// ---------------------------------------------------------------------------
// State & reducer
// ---------------------------------------------------------------------------

interface PlayersState {
  searchQuery: string
  searchResults: Player[]
  selectedPlayer: Player | null
  playerStats: PlayerStats | null
  selectedSeason: string
  loading: boolean
  statsLoading: boolean
  error: string | null
  recentSearches: string[]
  dataSource: string | undefined
  timestamp: string | undefined
}

type PlayersAction =
  | { type: 'SET_QUERY'; payload: string }
  | { type: 'SEARCH_START' }
  | { type: 'SEARCH_SUCCESS'; payload: { players: Player[]; dataSource?: string; timestamp?: string } }
  | { type: 'SEARCH_NO_RESULTS' }
  | { type: 'SEARCH_ERROR'; payload: string }
  | { type: 'SEARCH_END' }
  | { type: 'SELECT_PLAYER'; payload: Player }
  | { type: 'STATS_START' }
  | { type: 'STATS_SUCCESS'; payload: PlayerStats }
  | { type: 'STATS_ERROR'; payload: string }
  | { type: 'STATS_END' }
  | { type: 'SET_SEASON'; payload: string }
  | { type: 'SET_RECENT_SEARCHES'; payload: string[] }
  | { type: 'ADD_RECENT_SEARCH'; payload: string }

const initialState: PlayersState = {
  searchQuery: '',
  searchResults: [],
  selectedPlayer: null,
  playerStats: null,
  selectedSeason: '2024',
  loading: false,
  statsLoading: false,
  error: null,
  recentSearches: [],
  dataSource: undefined,
  timestamp: undefined,
}

function playersReducer(state: PlayersState, action: PlayersAction): PlayersState {
  switch (action.type) {
    case 'SET_QUERY':
      return { ...state, searchQuery: action.payload }
    case 'SEARCH_START':
      return {
        ...state,
        loading: true,
        error: null,
        searchResults: [],
        selectedPlayer: null,
        playerStats: null,
      }
    case 'SEARCH_SUCCESS':
      return {
        ...state,
        searchResults: action.payload.players,
        dataSource: action.payload.dataSource,
        timestamp: action.payload.timestamp,
      }
    case 'SEARCH_NO_RESULTS':
      return { ...state, error: 'No players found matching your search' }
    case 'SEARCH_ERROR':
      return { ...state, error: action.payload }
    case 'SEARCH_END':
      return { ...state, loading: false }
    case 'SELECT_PLAYER':
      return { ...state, selectedPlayer: action.payload }
    case 'STATS_START':
      return { ...state, statsLoading: true, error: null }
    case 'STATS_SUCCESS':
      return { ...state, playerStats: action.payload }
    case 'STATS_ERROR':
      return { ...state, error: action.payload, playerStats: null }
    case 'STATS_END':
      return { ...state, statsLoading: false }
    case 'SET_SEASON':
      return { ...state, selectedSeason: action.payload }
    case 'SET_RECENT_SEARCHES':
      return { ...state, recentSearches: action.payload }
    case 'ADD_RECENT_SEARCH': {
      const trimmed = action.payload.trim()
      if (!trimmed) return state
      const updated = [
        trimmed,
        ...state.recentSearches.filter((s) => s.toLowerCase() !== trimmed.toLowerCase()),
      ].slice(0, 5)
      localStorage.setItem('recentPlayerSearches', JSON.stringify(updated))
      return { ...state, recentSearches: updated }
    }
    default:
      return state
  }
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function PlayersClient() {
  const [state, dispatch] = useReducer(playersReducer, initialState)

  const {
    searchQuery,
    searchResults,
    selectedPlayer,
    playerStats,
    selectedSeason,
    loading,
    statsLoading,
    error,
    recentSearches,
    dataSource,
    timestamp,
  } = state

  // Load recent searches from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('recentPlayerSearches')
    if (saved) {
      try {
        dispatch({ type: 'SET_RECENT_SEARCHES', payload: JSON.parse(saved) })
      } catch (e) {
        console.error('Failed to parse recent searches', e)
      }
    }
  }, [])

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!searchQuery.trim()) {
      toast.error('Please enter a player name to search')
      return
    }

    dispatch({ type: 'SEARCH_START' })

    try {
      const response = await apiClient.searchPlayers(searchQuery, 20)
      dispatch({
        type: 'SEARCH_SUCCESS',
        payload: {
          players: response.players,
          dataSource: response.dataSource,
          timestamp: response.timestamp,
        },
      })

      if (response.players.length === 0) {
        dispatch({ type: 'SEARCH_NO_RESULTS' })
        toast.info('No players found', {
          description: 'Try searching by first name, last name, or team',
        })
      } else {
        dispatch({ type: 'ADD_RECENT_SEARCH', payload: searchQuery })
        toast.success(`Found ${response.players.length} player(s)`, {
          description: `Showing results for "${searchQuery}"`,
        })
      }
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to search players'
      dispatch({ type: 'SEARCH_ERROR', payload: errorMessage })
      toast.error('Search failed', {
        description: errorMessage,
        action: { label: 'Retry', onClick: () => handleSearch(e) },
      })
    } finally {
      dispatch({ type: 'SEARCH_END' })
    }
  }

  const loadPlayerStats = async (player: Player, season: string) => {
    dispatch({ type: 'STATS_START' })
    try {
      const stats = await apiClient.getPlayerStats(player.id, season)
      dispatch({ type: 'STATS_SUCCESS', payload: stats })

      if (stats.games_played > 0) {
        toast.success(`Loaded ${player.first_name} ${player.last_name}`, {
          description: `${stats.games_played} games in ${season}-${parseInt(season.slice(2)) + 1} season`,
        })
      }
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to load player stats'
      dispatch({ type: 'STATS_ERROR', payload: errorMessage })
      toast.error('Failed to load stats', { description: errorMessage })
    } finally {
      dispatch({ type: 'STATS_END' })
    }
  }

  const handleSelectPlayer = async (player: Player) => {
    dispatch({ type: 'SELECT_PLAYER', payload: player })
    await loadPlayerStats(player, selectedSeason)
  }

  const handleSeasonChange = async (season: string) => {
    dispatch({ type: 'SET_SEASON', payload: season })
    if (selectedPlayer) {
      await loadPlayerStats(selectedPlayer, season)
    }
  }

  const handleFeaturedClick = (name: string) => {
    dispatch({ type: 'SET_QUERY', payload: name })
    handleSearch(new Event('submit') as any)
  }

  const getPlayerHeight = (player: Player) => {
    if (player.height_feet && player.height_inches) {
      return `${player.height_feet}'${player.height_inches}"`
    }
    return 'N/A'
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8" role="main" aria-labelledby="page-title">
      <div>
        <h1 className="text-4xl font-bold" id="page-title">Player Stats</h1>
        <p className="text-gray-400 mt-2">
          Search for players and analyze their performance statistics
        </p>
      </div>

      <PlayerSearch
        searchQuery={searchQuery}
        loading={loading}
        searchResults={searchResults}
        selectedPlayer={selectedPlayer}
        recentSearches={recentSearches}
        onQueryChange={(q) => dispatch({ type: 'SET_QUERY', payload: q })}
        onSearch={handleSearch}
        onFeaturedClick={handleFeaturedClick}
      />

      {error && (
        <div className="bg-red-900/20 border border-red-500 rounded-lg p-4" role="alert">
          <p className="text-red-400">{error}</p>
        </div>
      )}

      <PlayerResults
        searchResults={searchResults}
        selectedPlayer={selectedPlayer}
        dataSource={dataSource}
        timestamp={timestamp}
        onSelectPlayer={handleSelectPlayer}
        getPlayerHeight={getPlayerHeight}
      />

      {selectedPlayer && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <PlayerInfo player={selectedPlayer} getPlayerHeight={getPlayerHeight} />
          <PlayerSeasonStats
            selectedSeason={selectedSeason}
            statsLoading={statsLoading}
            playerStats={playerStats}
            onSeasonChange={handleSeasonChange}
          />
        </div>
      )}

      {selectedPlayer && playerStats && playerStats.games_played > 0 && (
        <PlayerStatsChart playerStats={playerStats} />
      )}
    </div>
  )
}
