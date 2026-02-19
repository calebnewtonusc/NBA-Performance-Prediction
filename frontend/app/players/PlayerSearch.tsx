'use client'

import { Player } from '@/lib/api-client'

const FEATURED_PLAYERS = [
  { name: 'LeBron James', id: 237 },
  { name: 'Stephen Curry', id: 124 },
  { name: 'Kevin Durant', id: 140 },
  { name: 'Giannis Antetokounmpo', id: 15 },
  { name: 'Luka Doncic', id: 154 },
  { name: 'Joel Embiid', id: 162 },
]

interface PlayerSearchProps {
  searchQuery: string
  loading: boolean
  searchResults: Player[]
  selectedPlayer: Player | null
  recentSearches: string[]
  onQueryChange: (q: string) => void
  onSearch: (e: React.FormEvent) => void
  onFeaturedClick: (name: string) => void
}

export function PlayerSearch({
  searchQuery,
  loading,
  searchResults,
  selectedPlayer,
  recentSearches,
  onQueryChange,
  onSearch,
  onFeaturedClick,
}: PlayerSearchProps) {
  return (
    <div className="bg-secondary p-6 rounded-lg border border-gray-700">
      <h2 className="text-2xl font-bold mb-4">Search Players</h2>
      <form onSubmit={onSearch} className="flex gap-4">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => onQueryChange(e.target.value)}
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

      {recentSearches.length > 0 && !loading && searchResults.length === 0 && (
        <div className="mt-4">
          <p className="text-sm text-gray-400 mb-2">Recent Searches:</p>
          <div className="flex flex-wrap gap-2">
            {recentSearches.map((search) => (
              <button
                key={search}
                onClick={() => onFeaturedClick(search)}
                className="px-3 py-1.5 bg-background border border-gray-600 rounded-full text-sm hover:border-primary hover:text-primary transition-colors"
              >
                {search}
              </button>
            ))}
          </div>
        </div>
      )}

      {!loading && searchResults.length === 0 && !selectedPlayer && (
        <div className="mt-6 pt-6 border-t border-gray-700">
          <p className="text-sm text-gray-400 mb-3">Popular Players:</p>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {FEATURED_PLAYERS.map((player) => (
              <button
                key={player.id}
                onClick={() => onFeaturedClick(player.name)}
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
  )
}
