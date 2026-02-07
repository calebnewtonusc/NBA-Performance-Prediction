'use client'

// Re-export Recharts components
// Note: Direct exports for now to avoid Next.js dynamic import type issues
// These are only loaded when the predictions page is accessed
export {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
