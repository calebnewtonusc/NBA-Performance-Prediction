'use client'

import { PredictionResponse } from '@/lib/api-client'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from '@/components/LazyChart'
import { WinProbabilityGauge } from '@/components/WinProbabilityGauge'
import { TeamMatchupComparison } from '@/components/TeamMatchupComparison'
import { AnimatedCounter } from '@/components/AnimatedCounter'
import { getTeamColors, getTeamInfo, hexToRgba } from '@/lib/nba-teams'
import { Share2, Download, Trophy } from 'lucide-react'

interface PredictionResultProps {
  prediction: PredictionResponse
  homeTeam: string
  awayTeam: string
  predictionHistory: any[]
  onShare: () => void
  onExportCSV: () => void
}

function CustomBarTooltip({ active, payload, homeTeam, awayTeam, homeColors, awayColors }: any) {
  if (!active || !payload || !payload.length) return null
  const entry = payload[0]
  const isHome = entry.payload.team === homeTeam
  const colors = isHome ? homeColors : awayColors
  const teamInfo = getTeamInfo(isHome ? homeTeam : awayTeam)

  return (
    <div
      className="rounded-xl border p-3 shadow-xl"
      style={{
        backgroundColor: '#1a1f2e',
        borderColor: colors.primary,
        minWidth: 140,
      }}
    >
      <div className="flex items-center gap-2 mb-2">
        <div
          className="w-3 h-3 rounded-sm"
          style={{ backgroundColor: colors.primary }}
        />
        <span className="text-xs font-bold text-white">
          {isHome ? homeTeam : awayTeam}
        </span>
      </div>
      <div className="text-xl font-black" style={{ color: colors.primary }}>
        <AnimatedCounter value={entry.value * 100} decimals={1} suffix="%" duration={600} />
      </div>
      <div className="text-xs text-gray-400 mt-0.5">Win Probability</div>
    </div>
  )
}

export function PredictionResult({
  prediction,
  homeTeam,
  awayTeam,
  predictionHistory,
  onShare,
  onExportCSV,
}: PredictionResultProps) {
  const winner = prediction.prediction as 'home' | 'away'
  const winnerTeam = winner === 'home' ? homeTeam : awayTeam
  const loserTeam = winner === 'home' ? awayTeam : homeTeam
  const winnerColors = getTeamColors(winnerTeam)
  const loserColors = getTeamColors(loserTeam)
  const homeColors = getTeamColors(homeTeam)
  const awayColors = getTeamColors(awayTeam)

  const chartData = [
    { team: homeTeam, probability: prediction.home_win_probability },
    { team: awayTeam, probability: prediction.away_win_probability },
  ]

  return (
    <div className="space-y-6" role="region" aria-labelledby="results-heading" aria-live="polite">
      {/* Winner headline */}
      <div className="text-center space-y-3">
        <div className="flex items-center justify-center gap-2 mb-1">
          <Trophy className="w-4 h-4" style={{ color: winnerColors.primary }} />
          <span className="text-xs font-bold uppercase tracking-widest text-gray-400">
            Predicted Winner
          </span>
        </div>
        <div
          className="text-5xl sm:text-6xl font-black break-words"
          style={{
            color: winnerColors.primary,
            textShadow: `0 0 40px ${hexToRgba(winnerColors.primary, 0.4)}`,
          }}
          aria-label={`Predicted winner: ${winnerTeam}`}
        >
          {winnerTeam}
        </div>
        <div className="flex items-center justify-center gap-3 flex-wrap">
          <span
            className="text-base font-bold px-4 py-1.5 rounded-full"
            style={{
              backgroundColor: hexToRgba(winnerColors.primary, 0.15),
              color: winnerColors.primary,
              border: `1px solid ${hexToRgba(winnerColors.primary, 0.4)}`,
            }}
          >
            {winner === 'home' ? 'Home' : 'Away'} Victory
          </span>
          <span className="text-gray-300 font-bold text-lg">
            <AnimatedCounter
              value={prediction.confidence * 100}
              decimals={1}
              suffix="% confidence"
              duration={1000}
            />
          </span>
        </div>
      </div>

      {/* Win Probability Gauge */}
      <div className="flex justify-center pt-2 border-t border-gray-700/50">
        <WinProbabilityGauge
          homeTeam={homeTeam}
          awayTeam={awayTeam}
          homeWinProbability={prediction.home_win_probability}
          awayWinProbability={prediction.away_win_probability}
          winner={winner}
        />
      </div>

      {/* Bar chart with team colors */}
      <div className="pt-4 border-t border-gray-700/50">
        <h3 className="text-sm font-bold text-gray-400 uppercase tracking-widest mb-4">
          Win Probability Breakdown
        </h3>
        <ResponsiveContainer width="100%" height={160}>
          <BarChart data={chartData} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
            <XAxis
              dataKey="team"
              stroke="#6B7280"
              tick={{ fontWeight: 700, fontSize: 12 }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              stroke="#4B5563"
              tick={{ fontSize: 11, fill: '#6B7280' }}
              axisLine={false}
              tickLine={false}
              tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
              domain={[0, 1]}
            />
            <Tooltip
              content={
                <CustomBarTooltip
                  homeTeam={homeTeam}
                  awayTeam={awayTeam}
                  homeColors={homeColors}
                  awayColors={awayColors}
                />
              }
              cursor={{ fill: 'rgba(255,255,255,0.03)' }}
            />
            <Bar dataKey="probability" radius={[6, 6, 0, 0]} maxBarSize={60}>
              {chartData.map((entry) => {
                const isHome = entry.team === homeTeam
                const col = isHome ? homeColors.primary : awayColors.primary
                return <Cell key={entry.team} fill={col} />
              })}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Team probability cards */}
      <div className="grid grid-cols-2 gap-3">
        <div
          className="p-4 rounded-xl border"
          style={{
            backgroundColor: hexToRgba(homeColors.primary, 0.08),
            borderColor: hexToRgba(homeColors.primary, 0.3),
          }}
        >
          <div className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-1">Home</div>
          <div className="text-base font-black text-white mb-1">{homeTeam}</div>
          <div className="text-2xl font-black" style={{ color: homeColors.primary }}>
            <AnimatedCounter
              value={prediction.home_win_probability * 100}
              decimals={1}
              suffix="%"
              duration={1000}
            />
          </div>
          <div className="text-xs text-gray-500 mt-0.5">to win</div>
          {winner === 'home' && (
            <div
              className="mt-2 text-xs font-bold px-2 py-0.5 rounded inline-block"
              style={{ backgroundColor: hexToRgba(homeColors.primary, 0.2), color: homeColors.primary }}
            >
              PICK
            </div>
          )}
        </div>

        <div
          className="p-4 rounded-xl border"
          style={{
            backgroundColor: hexToRgba(awayColors.primary, 0.08),
            borderColor: hexToRgba(awayColors.primary, 0.3),
          }}
        >
          <div className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-1">Away</div>
          <div className="text-base font-black text-white mb-1">{awayTeam}</div>
          <div className="text-2xl font-black" style={{ color: awayColors.primary }}>
            <AnimatedCounter
              value={prediction.away_win_probability * 100}
              decimals={1}
              suffix="%"
              duration={1000}
            />
          </div>
          <div className="text-xs text-gray-500 mt-0.5">to win</div>
          {winner === 'away' && (
            <div
              className="mt-2 text-xs font-bold px-2 py-0.5 rounded inline-block"
              style={{ backgroundColor: hexToRgba(awayColors.primary, 0.2), color: awayColors.primary }}
            >
              PICK
            </div>
          )}
        </div>
      </div>

      {/* Matchup comparison */}
      <div className="pt-4 border-t border-gray-700/50">
        <h3 className="text-sm font-bold text-gray-400 uppercase tracking-widest mb-3">
          Head-to-Head
        </h3>
        <TeamMatchupComparison
          homeTeam={homeTeam}
          awayTeam={awayTeam}
          stats={[
            {
              label: 'Win %',
              home: prediction.home_win_probability,
              away: prediction.away_win_probability,
              format: 'pct',
              higherIsBetter: true,
            },
            {
              label: 'Confidence',
              home: winner === 'home' ? prediction.confidence : 1 - prediction.confidence,
              away: winner === 'away' ? prediction.confidence : 1 - prediction.confidence,
              format: 'pct',
              higherIsBetter: true,
            },
          ]}
        />
      </div>

      {/* Action buttons */}
      <div className="flex gap-3 pt-2 border-t border-gray-700/50">
        <button
          onClick={onShare}
          className="flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl font-bold text-sm transition-all duration-200 hover:-translate-y-0.5"
          style={{
            backgroundColor: hexToRgba('#3B82F6', 0.15),
            border: '1px solid rgba(59,130,246,0.3)',
            color: '#60A5FA',
          }}
        >
          <Share2 className="w-4 h-4" />
          Share
        </button>

        {predictionHistory.length > 0 && (
          <button
            onClick={onExportCSV}
            className="flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl font-bold text-sm transition-all duration-200 hover:-translate-y-0.5"
            style={{
              backgroundColor: hexToRgba('#10B981', 0.15),
              border: '1px solid rgba(16,185,129,0.3)',
              color: '#34D399',
            }}
          >
            <Download className="w-4 h-4" />
            Export {predictionHistory.length} CSV
          </button>
        )}
      </div>
    </div>
  )
}
