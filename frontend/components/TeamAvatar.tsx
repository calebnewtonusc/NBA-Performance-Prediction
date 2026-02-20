'use client'

import { getTeamColors, getTeamInfo, hexToRgba } from '@/lib/nba-teams'

interface TeamAvatarProps {
  abbr: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
  showName?: boolean
  className?: string
}

const SIZE_MAP = {
  sm: { outer: 32, inner: 28, text: 'text-xs', font: 11 },
  md: { outer: 48, inner: 42, text: 'text-sm', font: 15 },
  lg: { outer: 64, inner: 56, text: 'text-base', font: 19 },
  xl: { outer: 96, inner: 84, text: 'text-xl', font: 28 },
}

export function TeamAvatar({ abbr, size = 'md', showName = false, className = '' }: TeamAvatarProps) {
  const colors = getTeamColors(abbr)
  const info = getTeamInfo(abbr)
  const { outer, inner, text, font } = SIZE_MAP[size]

  const displayText = abbr.slice(0, 3).toUpperCase()

  return (
    <div className={`flex flex-col items-center gap-1 ${className}`}>
      <div
        style={{
          width: outer,
          height: outer,
          borderRadius: outer * 0.25,
          background: `linear-gradient(135deg, ${colors.primary}, ${colors.secondary})`,
          border: `2px solid ${hexToRgba(colors.primary, 0.5)}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: `0 0 12px ${hexToRgba(colors.primary, 0.3)}`,
          flexShrink: 0,
        }}
      >
        <span
          style={{
            fontSize: font,
            fontWeight: 900,
            color: colors.text || '#FFFFFF',
            letterSpacing: '-0.03em',
            fontFamily: 'system-ui, -apple-system, sans-serif',
            lineHeight: 1,
          }}
        >
          {displayText}
        </span>
      </div>
      {showName && info && (
        <div className="text-center">
          <div className={`${text} font-bold text-white leading-tight`}>{info.city}</div>
          <div className="text-xs text-gray-400 leading-tight">{info.name}</div>
        </div>
      )}
    </div>
  )
}

// Player avatar with initials - styled with team colors
interface PlayerAvatarProps {
  firstName: string
  lastName: string
  teamAbbr?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
  className?: string
}

export function PlayerAvatar({
  firstName,
  lastName,
  teamAbbr,
  size = 'md',
  className = '',
}: PlayerAvatarProps) {
  const colors = teamAbbr ? getTeamColors(teamAbbr) : null
  const { outer, font } = SIZE_MAP[size]

  const initials = `${firstName?.[0] || ''}${lastName?.[0] || ''}`.toUpperCase()

  const bg = colors
    ? `linear-gradient(135deg, ${colors.primary}, ${colors.secondary})`
    : 'linear-gradient(135deg, #374151, #1F2937)'
  const border = colors ? hexToRgba(colors.primary, 0.5) : '#4B5563'
  const shadow = colors ? `0 0 12px ${hexToRgba(colors.primary, 0.3)}` : 'none'
  const textColor = colors?.text || '#FFFFFF'

  return (
    <div
      className={`flex-shrink-0 ${className}`}
      style={{
        width: outer,
        height: outer,
        borderRadius: '50%',
        background: bg,
        border: `2px solid ${border}`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        boxShadow: shadow,
      }}
    >
      <span
        style={{
          fontSize: font,
          fontWeight: 800,
          color: textColor,
          letterSpacing: '-0.02em',
          fontFamily: 'system-ui, -apple-system, sans-serif',
        }}
      >
        {initials}
      </span>
    </div>
  )
}
