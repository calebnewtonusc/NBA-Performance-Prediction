'use client'

import { InfoTooltip } from '@/components/InfoTooltip'
import { TeamAvatar } from '@/components/TeamAvatar'
import { getTeamColors, NBA_TEAMS_LIST, hexToRgba } from '@/lib/nba-teams'
import { Loader2, ClipboardList, Zap } from 'lucide-react'

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
  const homeColors = getTeamColors(homeTeam)
  const awayColors = getTeamColors(awayTeam)
  const sameTeam = homeTeam === awayTeam

  return (
    <div className="bg-secondary rounded-2xl border border-gray-700/50 overflow-hidden">
      {/* Header */}
      <div className="px-6 py-5 border-b border-gray-700/50">
        <h2 className="text-xl font-bold text-white" id="matchup-heading">
          Select Matchup
        </h2>
        <p className="text-sm text-gray-400 mt-0.5">
          Choose home and away teams. Live stats fetched automatically
        </p>
      </div>

      <form onSubmit={onPredict} className="p-6 space-y-6" aria-labelledby="matchup-heading">
        {/* Matchup preview */}
        <div
          className="flex items-center justify-between p-4 rounded-xl"
          style={{
            background: `linear-gradient(135deg, ${hexToRgba(homeColors.primary, 0.08)}, #0E1117, ${hexToRgba(awayColors.primary, 0.08)})`,
            border: `1px solid ${hexToRgba('#6B7280', 0.3)}`,
          }}
        >
          <div className="flex flex-col items-center gap-2">
            <TeamAvatar abbr={homeTeam} size="lg" />
            <span className="text-xs font-bold text-gray-400 uppercase tracking-wider">Home</span>
          </div>

          <div className="text-center">
            <div className="text-2xl font-black text-gray-600">VS</div>
          </div>

          <div className="flex flex-col items-center gap-2">
            <TeamAvatar abbr={awayTeam} size="lg" />
            <span className="text-xs font-bold text-gray-400 uppercase tracking-wider">Away</span>
          </div>
        </div>

        {/* Home Team Select */}
        <div>
          <label
            htmlFor="home-team-select"
            className="block text-xs font-bold uppercase tracking-widest mb-2 flex items-center gap-2"
            style={{ color: homeColors.primary }}
          >
            Home Team
            <InfoTooltip content="The team playing at home. Home court advantage is automatically factored into predictions." />
          </label>
          <div className="relative">
            <div
              className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 rounded flex items-center justify-center text-xs font-black"
              style={{
                backgroundColor: hexToRgba(homeColors.primary, 0.2),
                color: homeColors.primary,
              }}
            >
              {homeTeam.slice(0, 2)}
            </div>
            <select
              id="home-team-select"
              value={homeTeam}
              onChange={(e) => onHomeChange(e.target.value)}
              className="w-full bg-background border rounded-xl pl-10 pr-4 py-3 text-white font-semibold focus:outline-none transition-colors appearance-none"
              style={{
                borderColor: hexToRgba(homeColors.primary, 0.4),
                boxShadow: `0 0 0 0px ${homeColors.primary}`,
              }}
              onFocus={(e) => {
                e.target.style.borderColor = homeColors.primary
                e.target.style.boxShadow = `0 0 0 2px ${hexToRgba(homeColors.primary, 0.2)}`
              }}
              onBlur={(e) => {
                e.target.style.borderColor = hexToRgba(homeColors.primary, 0.4)
                e.target.style.boxShadow = 'none'
              }}
              aria-label="Select home team"
              aria-required="true"
            >
              {NBA_TEAMS_LIST.map((team) => (
                <option key={team.abbr} value={team.abbr}>
                  {team.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Away Team Select */}
        <div>
          <label
            htmlFor="away-team-select"
            className="block text-xs font-bold uppercase tracking-widest mb-2 flex items-center gap-2"
            style={{ color: awayColors.primary }}
          >
            Away Team
            <InfoTooltip content="The visiting team. Road game statistics and travel fatigue are considered in predictions." />
          </label>
          <div className="relative">
            <div
              className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 rounded flex items-center justify-center text-xs font-black"
              style={{
                backgroundColor: hexToRgba(awayColors.primary, 0.2),
                color: awayColors.primary,
              }}
            >
              {awayTeam.slice(0, 2)}
            </div>
            <select
              id="away-team-select"
              value={awayTeam}
              onChange={(e) => onAwayChange(e.target.value)}
              className="w-full bg-background border rounded-xl pl-10 pr-4 py-3 text-white font-semibold focus:outline-none transition-colors appearance-none"
              style={{
                borderColor: hexToRgba(awayColors.primary, 0.4),
              }}
              onFocus={(e) => {
                e.target.style.borderColor = awayColors.primary
                e.target.style.boxShadow = `0 0 0 2px ${hexToRgba(awayColors.primary, 0.2)}`
              }}
              onBlur={(e) => {
                e.target.style.borderColor = hexToRgba(awayColors.primary, 0.4)
                e.target.style.boxShadow = 'none'
              }}
              aria-label="Select away team"
              aria-required="true"
            >
              {NBA_TEAMS_LIST.map((team) => (
                <option key={team.abbr} value={team.abbr}>
                  {team.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Info note */}
        <div className="bg-blue-500/8 border border-blue-500/20 rounded-xl p-3">
          <p className="text-xs text-blue-400 font-medium">
            Live NBA stats are fetched automatically for the selected matchup
          </p>
        </div>

        {/* Same team warning */}
        {sameTeam && (
          <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-3" role="alert">
            <p className="text-xs text-yellow-400 font-semibold flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              Select different teams for home and away
            </p>
          </div>
        )}

        {/* Predict button */}
        <button
          type="submit"
          disabled={loading || sameTeam}
          className="w-full flex items-center justify-center gap-2.5 py-3.5 px-4 rounded-xl font-bold text-white transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed hover:-translate-y-0.5"
          style={{
            background: sameTeam
              ? '#374151'
              : `linear-gradient(135deg, #FF6B6B, #EF4444)`,
            boxShadow: sameTeam ? 'none' : '0 4px 16px rgba(255,107,107,0.3)',
          }}
          aria-label={loading ? 'Loading prediction' : 'Get game prediction'}
          aria-busy={loading}
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Fetching stats and predicting...
            </>
          ) : (
            <>
              <Zap className="w-4 h-4" />
              Get Prediction
            </>
          )}
        </button>
      </form>

      {/* Compare all models button */}
      <div className="px-6 pb-6">
        <button
          type="button"
          onClick={onCompareAll}
          disabled={comparing || loading || sameTeam}
          className="w-full flex items-center justify-center gap-2.5 py-3 px-4 rounded-xl font-bold text-sm transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed hover:-translate-y-0.5"
          style={{
            backgroundColor: 'rgba(59,130,246,0.12)',
            border: '1px solid rgba(59,130,246,0.25)',
            color: '#60A5FA',
          }}
          aria-label={comparing ? 'Comparing models' : 'Compare all models'}
          aria-busy={comparing}
        >
          {comparing ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Comparing models...
            </>
          ) : (
            <>
              <ClipboardList className="w-4 h-4" />
              Compare All Models
            </>
          )}
        </button>
      </div>

      {error && (
        <div
          className="mx-6 mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-sm"
          role="alert"
          aria-live="assertive"
        >
          {error}
        </div>
      )}
    </div>
  )
}
