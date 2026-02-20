'use client'

import { PerformanceMetrics } from '@/lib/api-client'
import { InfoTooltip } from '@/components/InfoTooltip'
import { AnimatedCounter } from '@/components/AnimatedCounter'
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

interface OverallPerformanceSectionProps {
  performance: PerformanceMetrics
}

const METRIC_CONFIG = [
  { key: 'accuracy', label: 'Accuracy', color: '#10B981', description: 'Percentage of correct predictions out of all predictions made. Higher is better.' },
  { key: 'precision', label: 'Precision', color: '#3B82F6', description: 'Of all positive predictions, how many were correct. Measures prediction reliability.' },
  { key: 'recall', label: 'Recall', color: '#F59E0B', description: 'Of all actual positives, how many were correctly identified. Measures completeness.' },
  { key: 'f1_score', label: 'F1 Score', color: '#8B5CF6', description: 'Harmonic mean of precision and recall. Balanced measure of model performance.' },
]

function MetricCard({
  label,
  value,
  color,
  tooltip,
  isHighlight = false,
}: {
  label: string
  value: number
  color: string
  tooltip: string
  isHighlight?: boolean
}) {
  const pct = value * 100
  return (
    <div
      className="p-4 rounded-xl border"
      style={{
        backgroundColor: `${color}0a`,
        borderColor: `${color}25`,
      }}
    >
      <div className="flex items-center gap-1.5 mb-2">
        <span className="text-xs font-bold uppercase tracking-widest" style={{ color }}>
          {label}
        </span>
        <InfoTooltip content={tooltip} />
      </div>
      <div
        className="text-3xl font-black"
        style={{ color: isHighlight ? color : '#FFFFFF' }}
      >
        <AnimatedCounter value={pct} decimals={1} suffix="%" duration={1000} />
      </div>
      {/* Mini bar */}
      <div className="mt-2 h-1 bg-gray-700 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-1000"
          style={{ width: `${pct}%`, backgroundColor: color }}
        />
      </div>
    </div>
  )
}

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload || !payload.length) return null
  const entry = payload[0]
  const config = METRIC_CONFIG.find((m) => m.label === label)
  const color = config?.color || '#FF6B6B'

  return (
    <div
      className="rounded-xl border p-3 shadow-xl"
      style={{ backgroundColor: '#1a1f2e', borderColor: color, minWidth: 140 }}
    >
      <div className="flex items-center gap-2 mb-1">
        <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: color }} />
        <span className="text-xs font-bold text-white uppercase tracking-wide">{label}</span>
      </div>
      <div className="text-2xl font-black" style={{ color }}>
        {entry.value.toFixed(1)}%
      </div>
    </div>
  )
}

export default function OverallPerformanceSection({ performance }: OverallPerformanceSectionProps) {
  const chartData = METRIC_CONFIG.map((m) => ({
    name: m.label,
    value: (performance[m.key as keyof PerformanceMetrics] as number) * 100,
    color: m.color,
  }))

  const totalPredictions = performance.predictions_count
  const correctPct = totalPredictions > 0
    ? (performance.correct_predictions / totalPredictions) * 100
    : 0

  return (
    <div className="space-y-6">
      <h2 className="text-lg font-bold text-white">Overall Performance</h2>

      {/* Metric cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {METRIC_CONFIG.map((m, i) => (
          <MetricCard
            key={m.key}
            label={m.label}
            value={(performance[m.key as keyof PerformanceMetrics] as number)}
            color={m.color}
            tooltip={m.description}
            isHighlight={i === 0}
          />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Prediction count stats */}
        <div className="bg-secondary rounded-2xl border border-gray-700/50 p-5">
          <h3 className="text-sm font-bold text-white uppercase tracking-widest mb-4">
            Prediction Stats
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center py-2 border-b border-gray-700/30">
              <span className="text-sm text-gray-400">Total Predictions</span>
              <span className="text-xl font-black text-white">
                <AnimatedCounter value={performance.predictions_count} duration={800} />
              </span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-gray-700/30">
              <span className="text-sm text-gray-400">Correct</span>
              <span className="text-xl font-black text-green-400">
                <AnimatedCounter value={performance.correct_predictions} duration={900} />
              </span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-gray-700/30">
              <span className="text-sm text-gray-400">Incorrect</span>
              <span className="text-xl font-black text-red-400">
                <AnimatedCounter value={performance.incorrect_predictions} duration={1000} />
              </span>
            </div>

            {/* Correct/incorrect bar */}
            <div className="pt-2">
              <div className="flex justify-between text-xs text-gray-500 mb-1.5">
                <span>Correct</span>
                <span>{correctPct.toFixed(1)}%</span>
                <span>Incorrect</span>
              </div>
              <div className="h-3 bg-gray-700 rounded-full overflow-hidden flex">
                <div
                  className="h-full bg-green-500 rounded-l-full transition-all duration-1000"
                  style={{ width: `${correctPct}%` }}
                />
                <div
                  className="h-full bg-red-500 rounded-r-full transition-all duration-1000"
                  style={{ width: `${100 - correctPct}%` }}
                />
              </div>
            </div>

            {performance.recent_accuracy !== undefined && (
              <div className="pt-2 border-t border-gray-700/30">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-400 flex items-center gap-1">
                    Recent Accuracy
                    <InfoTooltip content="Accuracy measured over the most recent predictions." />
                  </span>
                  <span className="text-xl font-black text-primary">
                    <AnimatedCounter
                      value={performance.recent_accuracy * 100}
                      decimals={1}
                      suffix="%"
                      duration={1100}
                    />
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Bar chart */}
        <div className="bg-secondary rounded-2xl border border-gray-700/50 p-5">
          <h3 className="text-sm font-bold text-white uppercase tracking-widest mb-4">
            Metrics Comparison
          </h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={chartData} margin={{ top: 10, right: 10, left: -15, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
              <XAxis
                dataKey="name"
                stroke="#4B5563"
                tick={{ fontWeight: 600, fontSize: 11, fill: '#9CA3AF' }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                stroke="#374151"
                tick={{ fontSize: 10, fill: '#6B7280' }}
                axisLine={false}
                tickLine={false}
                domain={[0, 100]}
                tickFormatter={(v) => `${v}%`}
              />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
              <Bar dataKey="value" radius={[6, 6, 0, 0]} maxBarSize={48}>
                {chartData.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
