'use client'

import { InfoTooltip } from '@/components/InfoTooltip'

const NBA_TEAMS = [
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

interface MatchupFormProps {
  homeTeam: string
  awayTeam: string
  loading: boolean
  comparing: boolean
  error: string | null
  onHomeChange: (team: string) => void
  onAwayChange: (team: string) => void
  onPredict: (e: React.FormEvent) => void
  onCompareAll: () => void
}

export function MatchupForm({
  homeTeam,
  awayTeam,
  loading,
  comparing,
  error,
  onHomeChange,
  onAwayChange,
  onPredict,
  onCompareAll,
}: MatchupFormProps) {
  return (
    <div className="bg-secondary p-4 sm:p-6 rounded-lg border border-gray-700">
      <h2 className="text-xl sm:text-2xl font-bold mb-4 sm:mb-6" id="matchup-heading">
        Select Matchup
      </h2>
      <form onSubmit={onPredict} className="space-y-6" aria-labelledby="matchup-heading">
        <div>
          <label htmlFor="home-team-select" className="block text-sm font-medium mb-2 flex items-center">
            Home Team
            <InfoTooltip content="The team playing at home. Home court advantage is automatically factored into predictions." />
          </label>
          <select
            id="home-team-select"
            value={homeTeam}
            onChange={(e) => onHomeChange(e.target.value)}
            className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary"
            aria-label="Select home team"
            aria-required="true"
          >
            {NBA_TEAMS.map((team) => (
              <option key={team.abbr} value={team.abbr}>
                {team.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="away-team-select" className="block text-sm font-medium mb-2 flex items-center">
            Away Team
            <InfoTooltip content="The visiting team. Road game statistics and travel fatigue are considered in predictions." />
          </label>
          <select
            id="away-team-select"
            value={awayTeam}
            onChange={(e) => onAwayChange(e.target.value)}
            className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary"
            aria-label="Select away team"
            aria-required="true"
          >
            {NBA_TEAMS.map((team) => (
              <option key={team.abbr} value={team.abbr}>
                {team.name}
              </option>
            ))}
          </select>
        </div>

        <div className="bg-blue-500/10 border border-blue-500 rounded-lg p-4" role="note" aria-live="polite">
          <p className="text-sm text-blue-400">
            Stats are automatically fetched from live NBA data sources
          </p>
        </div>

        {homeTeam === awayTeam && (
          <div className="bg-yellow-500/10 border border-yellow-500 rounded-lg p-4" role="alert" aria-live="polite">
            <p className="text-sm text-yellow-400 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              Please select different teams for home and away
            </p>
          </div>
        )}

        <button
          type="submit"
          disabled={loading || homeTeam === awayTeam}
          className="w-full bg-primary hover:bg-red-600 text-white font-bold py-3 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          aria-label={loading ? 'Loading prediction' : 'Get game prediction'}
          aria-busy={loading}
        >
          {loading ? 'Fetching stats and predicting...' : 'Get Prediction'}
        </button>
      </form>

      <button
        type="button"
        onClick={onCompareAll}
        disabled={comparing || loading || homeTeam === awayTeam}
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed mt-3 flex items-center justify-center gap-2"
        aria-label={comparing ? 'Comparing models' : 'Compare all models'}
        aria-busy={comparing}
      >
        {comparing ? (
          <>
            <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Comparing models...
          </>
        ) : (
          <>
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
              <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
            </svg>
            Compare All Models
          </>
        )}
      </button>

      {error && (
        <div
          className="mt-4 p-4 bg-red-500/10 border border-red-500 rounded-lg text-red-400"
          role="alert"
          aria-live="assertive"
        >
          {error}
        </div>
      )}
    </div>
  )
}
