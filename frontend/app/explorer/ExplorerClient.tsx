'use client'

import { useReducer } from 'react'
import { toast } from 'sonner'
import { apiClient, Game, TeamStats } from '@/lib/api-client'
import { ExplorerFilters } from './ExplorerFilters'
import { ExplorerTeamStats } from './ExplorerTeamStats'
import { ExplorerGamesTable } from './ExplorerGamesTable'
import { ExplorerPagination } from './ExplorerPagination'

// ---------------------------------------------------------------------------
// State & reducer
// ---------------------------------------------------------------------------

interface ExplorerState {
  selectedTeam: string
  selectedSeason: string
  games: Game[]
  teamStats: TeamStats | null
  sortColumn: string
  sortDirection: 'asc' | 'desc'
  loading: boolean
  error: string | null
  currentPage: number
  pageSize: number
  totalGames: number
}

type ExplorerAction =
  | { type: 'SET_TEAM'; payload: string }
  | { type: 'SET_SEASON'; payload: string }
  | { type: 'LOAD_START'; resetPage: boolean }
  | { type: 'LOAD_SUCCESS'; payload: { games: Game[]; teamStats: TeamStats | null; page: number; pageSize: number } }
  | { type: 'LOAD_ERROR'; payload: string }
  | { type: 'LOAD_END' }
  | { type: 'SET_SORT'; column: string; direction: 'asc' | 'desc' }
  | { type: 'SET_PAGE_SIZE'; payload: number }

const initialState: ExplorerState = {
  selectedTeam: '',
  selectedSeason: '2024',
  games: [],
  teamStats: null,
  sortColumn: 'date',
  sortDirection: 'desc',
  loading: false,
  error: null,
  currentPage: 1,
  pageSize: 25,
  totalGames: 0,
}

function explorerReducer(state: ExplorerState, action: ExplorerAction): ExplorerState {
  switch (action.type) {
    case 'SET_TEAM':
      return { ...state, selectedTeam: action.payload }
    case 'SET_SEASON':
      return { ...state, selectedSeason: action.payload }
    case 'LOAD_START':
      return {
        ...state,
        loading: true,
        error: null,
        ...(action.resetPage ? { games: [], teamStats: null } : {}),
      }
    case 'LOAD_SUCCESS': {
      const { games, teamStats, page, pageSize } = action.payload
      return {
        ...state,
        games,
        teamStats,
        currentPage: page,
        totalGames: games.length === pageSize ? pageSize * 10 : games.length,
      }
    }
    case 'LOAD_ERROR':
      return { ...state, error: action.payload }
    case 'LOAD_END':
      return { ...state, loading: false }
    case 'SET_SORT':
      return { ...state, sortColumn: action.column, sortDirection: action.direction }
    case 'SET_PAGE_SIZE':
      return { ...state, pageSize: action.payload, currentPage: 1 }
    default:
      return state
  }
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function ExplorerClient() {
  const [state, dispatch] = useReducer(explorerReducer, initialState)

  const {
    selectedTeam,
    selectedSeason,
    games,
    teamStats,
    sortColumn,
    sortDirection,
    loading,
    error,
    currentPage,
    pageSize,
    totalGames,
  } = state

  const totalPages = Math.ceil(totalGames / pageSize)

  const handleLoadData = async (page: number = 1) => {
    dispatch({ type: 'LOAD_START', resetPage: page === 1 })

    try {
      const filters = {
        team: selectedTeam || undefined,
        season: selectedSeason,
        limit: pageSize,
        offset: (page - 1) * pageSize,
      }

      const gamesData = await apiClient.getGames(filters)
      let loadedTeamStats: TeamStats | null = null

      if (selectedTeam) {
        loadedTeamStats = await apiClient.getTeamStats(selectedTeam, selectedSeason)
        toast.success('Data loaded', {
          description: `Found ${gamesData.length} games for ${selectedTeam} in ${selectedSeason}-${parseInt(selectedSeason.slice(2)) + 1}`,
        })
      } else {
        toast.success('Data loaded', {
          description: `Showing ${gamesData.length} games from ${selectedSeason}-${parseInt(selectedSeason.slice(2)) + 1} season`,
        })
      }

      dispatch({
        type: 'LOAD_SUCCESS',
        payload: { games: gamesData, teamStats: loadedTeamStats, page, pageSize },
      })
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to load data'
      dispatch({ type: 'LOAD_ERROR', payload: errorMessage })

      toast.error('Failed to load data', {
        description: errorMessage,
        action: { label: 'Retry', onClick: () => handleLoadData(page) },
      })
    } finally {
      dispatch({ type: 'LOAD_END' })
    }
  }

  const handlePageChange = (newPage: number) => {
    handleLoadData(newPage)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const handleSort = (column: string) => {
    const newDirection =
      sortColumn === column ? (sortDirection === 'asc' ? 'desc' : 'asc') : 'desc'
    dispatch({ type: 'SET_SORT', column, direction: newDirection })
  }

  const handlePageSizeChange = (size: number) => {
    dispatch({ type: 'SET_PAGE_SIZE', payload: size })
    handleLoadData(1)
  }

  const getSortedGames = (): Game[] => {
    if (!games.length) return []

    return [...games].sort((a, b) => {
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

      return sortDirection === 'asc' ? (aValue > bValue ? 1 : -1) : aValue < bValue ? 1 : -1
    })
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

      <ExplorerFilters
        selectedTeam={selectedTeam}
        selectedSeason={selectedSeason}
        loading={loading}
        onTeamChange={(team) => dispatch({ type: 'SET_TEAM', payload: team })}
        onSeasonChange={(season) => dispatch({ type: 'SET_SEASON', payload: season })}
        onLoadData={() => handleLoadData()}
      />

      {error && (
        <div className="bg-red-900/20 border border-red-500 rounded-lg p-4" role="alert">
          <p className="text-red-400">{error}</p>
        </div>
      )}

      {teamStats && <ExplorerTeamStats teamStats={teamStats} />}

      {games.length > 0 && (
        <div className="bg-secondary rounded-lg border border-gray-700 overflow-hidden">
          <ExplorerGamesTable
            sortedGames={sortedGames}
            sortColumn={sortColumn}
            sortDirection={sortDirection}
            currentPage={currentPage}
            pageSize={pageSize}
            totalGames={totalGames}
            loading={loading}
            onSort={handleSort}
            onPageSizeChange={handlePageSizeChange}
          />
          <ExplorerPagination
            currentPage={currentPage}
            totalPages={totalPages}
            loading={loading}
            onPageChange={handlePageChange}
          />
        </div>
      )}

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
