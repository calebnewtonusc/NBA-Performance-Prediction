/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#FF3B30',
        background: '#000000',
        secondary: '#1c1c1e',
        surface: '#2c2c2e',
        'surface-elevated': '#3a3a3c',
        // iOS system colors (for accent consistency)
        'ios-blue': '#0A84FF',
        'ios-green': '#30D158',
        'ios-purple': '#BF5AF2',
        'ios-yellow': '#FF9F0A',
        // NBA team color utilities
        'nba-gold': '#FDB927',
        'nba-green': '#007A33',
        'nba-red': '#CE1141',
        'nba-blue': '#006BB6',
        'nba-purple': '#552583',
      },
      fontFamily: {
        sans: [
          '-apple-system',
          'BlinkMacSystemFont',
          'SF Pro Display',
          'SF Pro Text',
          'Helvetica Neue',
          'Arial',
          'sans-serif',
        ],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shimmer': 'skeleton-shimmer 1.8s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-4px)' },
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
      boxShadow: {
        'apple': '0 1px 12px rgba(0,0,0,0.4)',
        'apple-lg': '0 6px 24px rgba(0,0,0,0.5)',
        'nba': '0 1px 12px rgba(255,59,48,0.25)',
        'card': '0 1px 12px rgba(0,0,0,0.4)',
        'card-hover': '0 6px 24px rgba(0,0,0,0.5)',
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.5rem',
      },
    },
  },
  plugins: [],
}
