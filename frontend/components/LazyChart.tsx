'use client'

import dynamic from 'next/dynamic'

// Lazy load Recharts components to reduce initial bundle size
export const BarChart = dynamic(
  () => import('recharts').then((mod) => mod.BarChart),
  {
    loading: () => (
      <div className="w-full h-[200px] flex items-center justify-center bg-gray-800/50 rounded-lg animate-pulse">
        <p className="text-gray-400">Loading chart...</p>
      </div>
    ),
    ssr: false,
  }
)

export const Bar = dynamic(
  () => import('recharts').then((mod) => mod.Bar),
  { ssr: false }
)

export const XAxis = dynamic(
  () => import('recharts').then((mod) => mod.XAxis),
  { ssr: false }
)

export const YAxis = dynamic(
  () => import('recharts').then((mod) => mod.YAxis),
  { ssr: false }
)

export const CartesianGrid = dynamic(
  () => import('recharts').then((mod) => mod.CartesianGrid),
  { ssr: false }
)

export const Tooltip = dynamic(
  () => import('recharts').then((mod) => mod.Tooltip),
  { ssr: false }
)

export const ResponsiveContainer = dynamic(
  () => import('recharts').then((mod) => mod.ResponsiveContainer),
  { ssr: false }
)
