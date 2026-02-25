// NBA Team Colors and Branding System
// Each team has primary, secondary, and accent colors from their official brand guidelines

export interface TeamColors {
  primary: string
  secondary: string
  accent: string
  text: string
  gradient: string
  border: string
}

export interface NBATeam {
  name: string
  abbr: string
  city: string
  colors: TeamColors
  conference: 'East' | 'West'
  division: string
}

export const NBA_TEAMS: Record<string, NBATeam> = {
  ATL: {
    name: 'Hawks',
    abbr: 'ATL',
    city: 'Atlanta',
    conference: 'East',
    division: 'Southeast',
    colors: {
      primary: '#C1D32F',
      secondary: '#E03A3E',
      accent: '#26282A',
      text: '#FFFFFF',
      gradient: 'from-red-600 to-yellow-400',
      border: '#E03A3E',
    },
  },
  BOS: {
    name: 'Celtics',
    abbr: 'BOS',
    city: 'Boston',
    conference: 'East',
    division: 'Atlantic',
    colors: {
      primary: '#007A33',
      secondary: '#BA9653',
      accent: '#963821',
      text: '#FFFFFF',
      gradient: 'from-green-700 to-green-500',
      border: '#007A33',
    },
  },
  BKN: {
    name: 'Nets',
    abbr: 'BKN',
    city: 'Brooklyn',
    conference: 'East',
    division: 'Atlantic',
    colors: {
      primary: '#000000',
      secondary: '#FFFFFF',
      accent: '#707271',
      text: '#FFFFFF',
      gradient: 'from-gray-900 to-gray-700',
      border: '#FFFFFF',
    },
  },
  CHA: {
    name: 'Hornets',
    abbr: 'CHA',
    city: 'Charlotte',
    conference: 'East',
    division: 'Southeast',
    colors: {
      primary: '#1D1160',
      secondary: '#00788C',
      accent: '#A1A1A4',
      text: '#FFFFFF',
      gradient: 'from-purple-900 to-teal-600',
      border: '#00788C',
    },
  },
  CHI: {
    name: 'Bulls',
    abbr: 'CHI',
    city: 'Chicago',
    conference: 'East',
    division: 'Central',
    colors: {
      primary: '#CE1141',
      secondary: '#000000',
      accent: '#CE1141',
      text: '#FFFFFF',
      gradient: 'from-red-700 to-red-900',
      border: '#CE1141',
    },
  },
  CLE: {
    name: 'Cavaliers',
    abbr: 'CLE',
    city: 'Cleveland',
    conference: 'East',
    division: 'Central',
    colors: {
      primary: '#860038',
      secondary: '#FDBB30',
      accent: '#002D62',
      text: '#FFFFFF',
      gradient: 'from-red-900 to-yellow-600',
      border: '#FDBB30',
    },
  },
  DAL: {
    name: 'Mavericks',
    abbr: 'DAL',
    city: 'Dallas',
    conference: 'West',
    division: 'Southwest',
    colors: {
      primary: '#00538C',
      secondary: '#002B5E',
      accent: '#B8C4CA',
      text: '#FFFFFF',
      gradient: 'from-blue-700 to-blue-900',
      border: '#00538C',
    },
  },
  DEN: {
    name: 'Nuggets',
    abbr: 'DEN',
    city: 'Denver',
    conference: 'West',
    division: 'Northwest',
    colors: {
      primary: '#0E2240',
      secondary: '#FEC524',
      accent: '#8B2131',
      text: '#FFFFFF',
      gradient: 'from-blue-900 to-yellow-500',
      border: '#FEC524',
    },
  },
  DET: {
    name: 'Pistons',
    abbr: 'DET',
    city: 'Detroit',
    conference: 'East',
    division: 'Central',
    colors: {
      primary: '#C8102E',
      secondary: '#1D42BA',
      accent: '#BEC0C2',
      text: '#FFFFFF',
      gradient: 'from-red-700 to-blue-700',
      border: '#C8102E',
    },
  },
  GSW: {
    name: 'Warriors',
    abbr: 'GSW',
    city: 'Golden State',
    conference: 'West',
    division: 'Pacific',
    colors: {
      primary: '#1D428A',
      secondary: '#FFC72C',
      accent: '#1D428A',
      text: '#FFFFFF',
      gradient: 'from-blue-800 to-yellow-400',
      border: '#FFC72C',
    },
  },
  HOU: {
    name: 'Rockets',
    abbr: 'HOU',
    city: 'Houston',
    conference: 'West',
    division: 'Southwest',
    colors: {
      primary: '#CE1141',
      secondary: '#000000',
      accent: '#C4CED4',
      text: '#FFFFFF',
      gradient: 'from-red-700 to-red-900',
      border: '#CE1141',
    },
  },
  IND: {
    name: 'Pacers',
    abbr: 'IND',
    city: 'Indiana',
    conference: 'East',
    division: 'Central',
    colors: {
      primary: '#002D62',
      secondary: '#FDBB30',
      accent: '#BEC0C2',
      text: '#FFFFFF',
      gradient: 'from-blue-900 to-yellow-500',
      border: '#FDBB30',
    },
  },
  LAC: {
    name: 'Clippers',
    abbr: 'LAC',
    city: 'LA',
    conference: 'West',
    division: 'Pacific',
    colors: {
      primary: '#C8102E',
      secondary: '#1D428A',
      accent: '#BEC0C2',
      text: '#FFFFFF',
      gradient: 'from-red-700 to-blue-800',
      border: '#C8102E',
    },
  },
  LAL: {
    name: 'Lakers',
    abbr: 'LAL',
    city: 'Los Angeles',
    conference: 'West',
    division: 'Pacific',
    colors: {
      primary: '#552583',
      secondary: '#FDB927',
      accent: '#000000',
      text: '#FFFFFF',
      gradient: 'from-purple-800 to-yellow-500',
      border: '#FDB927',
    },
  },
  MEM: {
    name: 'Grizzlies',
    abbr: 'MEM',
    city: 'Memphis',
    conference: 'West',
    division: 'Southwest',
    colors: {
      primary: '#5D76A9',
      secondary: '#12173F',
      accent: '#F5B112',
      text: '#FFFFFF',
      gradient: 'from-blue-600 to-blue-900',
      border: '#5D76A9',
    },
  },
  MIA: {
    name: 'Heat',
    abbr: 'MIA',
    city: 'Miami',
    conference: 'East',
    division: 'Southeast',
    colors: {
      primary: '#98002E',
      secondary: '#F9A01B',
      accent: '#000000',
      text: '#FFFFFF',
      gradient: 'from-red-900 to-orange-500',
      border: '#F9A01B',
    },
  },
  MIL: {
    name: 'Bucks',
    abbr: 'MIL',
    city: 'Milwaukee',
    conference: 'East',
    division: 'Central',
    colors: {
      primary: '#00471B',
      secondary: '#EEE1C6',
      accent: '#0077C0',
      text: '#FFFFFF',
      gradient: 'from-green-900 to-green-700',
      border: '#00471B',
    },
  },
  MIN: {
    name: 'Timberwolves',
    abbr: 'MIN',
    city: 'Minnesota',
    conference: 'West',
    division: 'Northwest',
    colors: {
      primary: '#0C2340',
      secondary: '#236192',
      accent: '#9EA1A2',
      text: '#FFFFFF',
      gradient: 'from-blue-900 to-blue-600',
      border: '#236192',
    },
  },
  NOP: {
    name: 'Pelicans',
    abbr: 'NOP',
    city: 'New Orleans',
    conference: 'West',
    division: 'Southwest',
    colors: {
      primary: '#0C2340',
      secondary: '#C8102E',
      accent: '#85714D',
      text: '#FFFFFF',
      gradient: 'from-blue-900 to-red-700',
      border: '#C8102E',
    },
  },
  NYK: {
    name: 'Knicks',
    abbr: 'NYK',
    city: 'New York',
    conference: 'East',
    division: 'Atlantic',
    colors: {
      primary: '#006BB6',
      secondary: '#F58426',
      accent: '#BEC0C2',
      text: '#FFFFFF',
      gradient: 'from-blue-700 to-orange-500',
      border: '#F58426',
    },
  },
  OKC: {
    name: 'Thunder',
    abbr: 'OKC',
    city: 'Oklahoma City',
    conference: 'West',
    division: 'Northwest',
    colors: {
      primary: '#007AC1',
      secondary: '#EF3B24',
      accent: '#002D62',
      text: '#FFFFFF',
      gradient: 'from-blue-600 to-orange-500',
      border: '#007AC1',
    },
  },
  ORL: {
    name: 'Magic',
    abbr: 'ORL',
    city: 'Orlando',
    conference: 'East',
    division: 'Southeast',
    colors: {
      primary: '#0077C0',
      secondary: '#C4CED4',
      accent: '#000000',
      text: '#FFFFFF',
      gradient: 'from-blue-700 to-blue-500',
      border: '#0077C0',
    },
  },
  PHI: {
    name: '76ers',
    abbr: 'PHI',
    city: 'Philadelphia',
    conference: 'East',
    division: 'Atlantic',
    colors: {
      primary: '#006BB6',
      secondary: '#ED174C',
      accent: '#002B5C',
      text: '#FFFFFF',
      gradient: 'from-blue-700 to-red-600',
      border: '#ED174C',
    },
  },
  PHX: {
    name: 'Suns',
    abbr: 'PHX',
    city: 'Phoenix',
    conference: 'West',
    division: 'Pacific',
    colors: {
      primary: '#1D1160',
      secondary: '#E56020',
      accent: '#63717A',
      text: '#FFFFFF',
      gradient: 'from-purple-900 to-orange-600',
      border: '#E56020',
    },
  },
  POR: {
    name: 'Trail Blazers',
    abbr: 'POR',
    city: 'Portland',
    conference: 'West',
    division: 'Northwest',
    colors: {
      primary: '#E03A3E',
      secondary: '#000000',
      accent: '#BAC3C9',
      text: '#FFFFFF',
      gradient: 'from-red-600 to-red-900',
      border: '#E03A3E',
    },
  },
  SAC: {
    name: 'Kings',
    abbr: 'SAC',
    city: 'Sacramento',
    conference: 'West',
    division: 'Pacific',
    colors: {
      primary: '#5A2D81',
      secondary: '#63727A',
      accent: '#000000',
      text: '#FFFFFF',
      gradient: 'from-purple-800 to-purple-600',
      border: '#5A2D81',
    },
  },
  SAS: {
    name: 'Spurs',
    abbr: 'SAS',
    city: 'San Antonio',
    conference: 'West',
    division: 'Southwest',
    colors: {
      primary: '#C4CED4',
      secondary: '#000000',
      accent: '#00B2A9',
      text: '#000000',
      gradient: 'from-gray-400 to-gray-700',
      border: '#C4CED4',
    },
  },
  TOR: {
    name: 'Raptors',
    abbr: 'TOR',
    city: 'Toronto',
    conference: 'East',
    division: 'Atlantic',
    colors: {
      primary: '#CE1141',
      secondary: '#000000',
      accent: '#A1A1A4',
      text: '#FFFFFF',
      gradient: 'from-red-700 to-red-900',
      border: '#CE1141',
    },
  },
  UTA: {
    name: 'Jazz',
    abbr: 'UTA',
    city: 'Utah',
    conference: 'West',
    division: 'Northwest',
    colors: {
      primary: '#002B5C',
      secondary: '#00471B',
      accent: '#F9A01B',
      text: '#FFFFFF',
      gradient: 'from-blue-900 to-green-800',
      border: '#00471B',
    },
  },
  WAS: {
    name: 'Wizards',
    abbr: 'WAS',
    city: 'Washington',
    conference: 'East',
    division: 'Southeast',
    colors: {
      primary: '#002B5C',
      secondary: '#E31837',
      accent: '#C4CED4',
      text: '#FFFFFF',
      gradient: 'from-blue-900 to-red-700',
      border: '#E31837',
    },
  },
}

export function getTeamColors(abbr: string): TeamColors {
  return (
    NBA_TEAMS[abbr]?.colors || {
      primary: '#FF6B6B',
      secondary: '#374151',
      accent: '#6B7280',
      text: '#FFFFFF',
      gradient: 'from-gray-700 to-gray-900',
      border: '#FF6B6B',
    }
  )
}

export function getTeamInfo(abbr: string): NBATeam | undefined {
  return NBA_TEAMS[abbr]
}

export function getTeamInitials(abbr: string): string {
  return abbr.slice(0, 2)
}

// Convert hex to rgba for opacity usage
export function hexToRgba(hex: string, alpha: number): string {
  const r = parseInt(hex.slice(1, 3), 16)
  const g = parseInt(hex.slice(3, 5), 16)
  const b = parseInt(hex.slice(5, 7), 16)
  return `rgba(${r}, ${g}, ${b}, ${alpha})`
}

export const NBA_TEAMS_LIST = [
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
