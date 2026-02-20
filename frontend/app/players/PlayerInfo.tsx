'use client'

import { Player } from '@/lib/api-client'
import { PlayerAvatar } from '@/components/TeamAvatar'
import { getTeamColors, getTeamInfo, hexToRgba } from '@/lib/nba-teams'
import { User, Ruler, Weight, MapPin } from 'lucide-react'

interface PlayerInfoProps {
  player: Player
  getPlayerHeight: (player: Player) => string
}

function InfoRow({
  label,
  value,
  icon: Icon,
}: {
  label: string
  value: string | React.ReactNode
  icon?: React.ComponentType<{ className?: string }>
}) {
  return (
    <div className="flex items-start gap-3 py-2.5 border-b border-gray-700/40 last:border-0">
      {Icon && (
        <div className="p-1.5 bg-gray-700/50 rounded-lg mt-0.5">
          <Icon className="w-3.5 h-3.5 text-gray-400" />
        </div>
      )}
      <div className="flex-1 min-w-0">
        <div className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-0.5">
          {label}
        </div>
        <div className="text-sm font-bold text-white">{value}</div>
      </div>
    </div>
  )
}

export function PlayerInfo({ player, getPlayerHeight }: PlayerInfoProps) {
  const teamAbbr = player.team?.abbreviation
  const colors = teamAbbr ? getTeamColors(teamAbbr) : null
  const teamInfo = teamAbbr ? getTeamInfo(teamAbbr) : null

  const positionColor = (() => {
    switch (player.position) {
      case 'G': return '#3B82F6'
      case 'F': return '#10B981'
      case 'C': return '#F59E0B'
      case 'G-F': case 'F-G': return '#8B5CF6'
      case 'F-C': case 'C-F': return '#EF4444'
      default: return '#6B7280'
    }
  })()

  return (
    <div className="bg-secondary rounded-2xl border border-gray-700/50 overflow-hidden">
      {/* Player header with team color accent */}
      <div
        className="relative px-6 py-6 overflow-hidden"
        style={{
          background: colors
            ? `linear-gradient(135deg, ${hexToRgba(colors.primary, 0.15)}, #262730)`
            : '#262730',
          borderBottom: `1px solid ${colors ? hexToRgba(colors.primary, 0.2) : '#374151'}`,
        }}
      >
        {/* Ambient glow */}
        {colors && (
          <div
            className="absolute top-0 right-0 w-32 h-32 rounded-full blur-3xl opacity-10 pointer-events-none"
            style={{ background: colors.primary, transform: 'translate(30%, -30%)' }}
          />
        )}

        <div className="flex items-center gap-4 relative">
          <PlayerAvatar
            firstName={player.first_name}
            lastName={player.last_name}
            teamAbbr={teamAbbr}
            size="xl"
          />
          <div className="flex-1 min-w-0">
            <h2 className="text-xl font-black text-white leading-tight">
              {player.first_name} {player.last_name}
            </h2>
            {teamAbbr && (
              <div
                className="flex items-center gap-1.5 mt-1.5"
              >
                <div
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: colors?.primary || '#6B7280' }}
                />
                <span
                  className="text-sm font-bold"
                  style={{ color: colors?.primary || '#9CA3AF' }}
                >
                  {teamAbbr}
                </span>
                {teamInfo && (
                  <span className="text-sm text-gray-400">
                    · {teamInfo.name}
                  </span>
                )}
              </div>
            )}
            {player.position && (
              <div
                className="inline-flex items-center mt-2 px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-widest"
                style={{
                  backgroundColor: `${positionColor}20`,
                  color: positionColor,
                  border: `1px solid ${positionColor}40`,
                }}
              >
                {player.position}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Stats grid */}
      <div className="p-6">
        <h3 className="text-xs font-bold uppercase tracking-widest text-gray-500 mb-4">
          Player Details
        </h3>
        <div className="space-y-0">
          <InfoRow
            label="Full Name"
            value={`${player.first_name} ${player.last_name}`}
            icon={User}
          />
          <InfoRow
            label="Height"
            value={getPlayerHeight(player)}
            icon={Ruler}
          />
          <InfoRow
            label="Weight"
            value={player.weight_pounds ? `${player.weight_pounds} lbs` : 'N/A'}
            icon={Weight}
          />
          {player.team && (
            <InfoRow
              label="Conference / Division"
              value={`${player.team.conference} Conference · ${player.team.division} Division`}
              icon={MapPin}
            />
          )}
        </div>
      </div>

      {/* Team badge */}
      {player.team && colors && (
        <div
          className="mx-6 mb-6 p-3 rounded-xl flex items-center gap-3"
          style={{
            backgroundColor: hexToRgba(colors.primary, 0.08),
            border: `1px solid ${hexToRgba(colors.primary, 0.2)}`,
          }}
        >
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center text-xs font-black"
            style={{
              background: `linear-gradient(135deg, ${colors.primary}, ${colors.secondary})`,
              color: colors.text || '#FFFFFF',
            }}
          >
            {teamAbbr?.slice(0, 2)}
          </div>
          <div>
            <div className="text-xs font-bold text-white">{player.team.full_name}</div>
            <div className="text-xs text-gray-400">{player.team.city} · NBA</div>
          </div>
        </div>
      )}
    </div>
  )
}
