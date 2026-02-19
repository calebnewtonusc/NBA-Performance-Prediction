'use client'

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

const SEASONS = ['2024', '2023', '2022', '2021', '2020']

interface ExplorerFiltersProps {
  selectedTeam: string
  selectedSeason: string
  loading: boolean
  onTeamChange: (team: string) => void
  onSeasonChange: (season: string) => void
  onLoadData: () => void
}

export function ExplorerFilters({
  selectedTeam,
  selectedSeason,
  loading,
  onTeamChange,
  onSeasonChange,
  onLoadData,
}: ExplorerFiltersProps) {
  return (
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
            onChange={(e) => onTeamChange(e.target.value)}
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
            onChange={(e) => onSeasonChange(e.target.value)}
            className="w-full px-4 py-3 bg-background border border-gray-600 rounded-lg focus:ring-2 focus:ring-primary"
            aria-label="Select season"
          >
            {SEASONS.map((season) => (
              <option key={season} value={season}>
                {season}-{parseInt(season.slice(2)) + 1}
              </option>
            ))}
          </select>
        </div>

        <div className="flex items-end">
          <button
            onClick={onLoadData}
            disabled={loading}
            className="w-full px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary/80 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Loading...' : 'Load Data'}
          </button>
        </div>
      </div>
    </div>
  )
}
