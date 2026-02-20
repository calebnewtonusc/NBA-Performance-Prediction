'use client'

import { ModelInfo } from '@/lib/api-client'
import { AnimatedCounter } from '@/components/AnimatedCounter'
import { StatCardSkeleton } from '@/components/SkeletonLoader'
import { Brain, CheckCircle2, Clock } from 'lucide-react'

interface ModelsGridProps {
  models: ModelInfo[]
  formatTimestamp: (timestamp: string) => string
}

const MODEL_COLORS: Record<string, { color: string; bg: string; label: string }> = {
  game_forest: { color: '#10B981', bg: '#10B98115', label: 'Random Forest' },
  game_logistic: { color: '#3B82F6', bg: '#3B82F615', label: 'Logistic Reg.' },
  game_tree: { color: '#F59E0B', bg: '#F59E0B15', label: 'Decision Tree' },
  player_lasso: { color: '#8B5CF6', bg: '#8B5CF615', label: 'Lasso' },
  player_linear: { color: '#EC4899', bg: '#EC489915', label: 'Linear Reg.' },
  player_ridge: { color: '#06B6D4', bg: '#06B6D415', label: 'Ridge Reg.' },
}

function getModelStyle(name: string) {
  return (
    MODEL_COLORS[name] ||
    MODEL_COLORS[Object.keys(MODEL_COLORS).find((k) => name.includes(k.split('_')[1] || '')) || ''] || {
      color: '#FF6B6B',
      bg: '#FF6B6B15',
      label: name,
    }
  )
}

function AccuracyBar({ value, color }: { value: number; color: string }) {
  return (
    <div className="relative">
      <div className="flex justify-between items-center mb-1">
        <span className="text-xs text-gray-500">0%</span>
        <span className="text-xs font-bold" style={{ color }}>
          {(value * 100).toFixed(1)}%
        </span>
        <span className="text-xs text-gray-500">100%</span>
      </div>
      <div className="h-1.5 bg-gray-700 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-1000"
          style={{
            width: `${value * 100}%`,
            backgroundColor: color,
            boxShadow: `0 0 6px ${color}60`,
          }}
        />
      </div>
    </div>
  )
}

export default function ModelsGrid({ models, formatTimestamp }: ModelsGridProps) {
  if (!models || models.length === 0) {
    return (
      <div>
        <h2 className="text-lg font-bold text-white mb-4">Available Models</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <StatCardSkeleton />
          <StatCardSkeleton />
          <StatCardSkeleton />
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center gap-2 mb-4">
        <Brain className="w-5 h-5 text-primary" />
        <h2 className="text-lg font-bold text-white">Available Models</h2>
        <div className="ml-auto flex items-center gap-1.5">
          <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
          <span className="text-xs font-medium text-green-400">{models.length} loaded</span>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {models.map((model) => {
          const style = getModelStyle(model.name)
          const accuracy = model.metrics?.accuracy

          return (
            <div
              key={`${model.name}-${model.version}`}
              className="rounded-xl border overflow-hidden transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg"
              style={{
                backgroundColor: style.bg,
                borderColor: `${style.color}30`,
              }}
            >
              {/* Card header */}
              <div
                className="px-5 py-4 border-b"
                style={{ borderColor: `${style.color}15` }}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <div
                      className="text-xs font-bold uppercase tracking-widest mb-1"
                      style={{ color: style.color }}
                    >
                      {style.label}
                    </div>
                    <h3 className="text-sm font-black text-white leading-tight">{model.name}</h3>
                    <div className="flex items-center gap-1 mt-1">
                      <span
                        className="text-xs px-1.5 py-0.5 rounded font-semibold"
                        style={{
                          backgroundColor: `${style.color}20`,
                          color: style.color,
                        }}
                      >
                        v{model.version}
                      </span>
                    </div>
                  </div>
                  <div
                    className="w-8 h-8 rounded-xl flex items-center justify-center"
                    style={{ backgroundColor: `${style.color}20` }}
                  >
                    <CheckCircle2 className="w-4 h-4" style={{ color: style.color }} />
                  </div>
                </div>
              </div>

              {/* Metrics */}
              <div className="px-5 py-4 space-y-3">
                {model.metrics ? (
                  <>
                    <AccuracyBar value={model.metrics.accuracy} color={style.color} />
                    <div className="grid grid-cols-2 gap-3 text-sm">
                      <div>
                        <div className="text-xs text-gray-500 mb-0.5">Precision</div>
                        <div className="font-bold text-white">
                          <AnimatedCounter
                            value={model.metrics.precision * 100}
                            decimals={1}
                            suffix="%"
                            duration={900}
                          />
                        </div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-500 mb-0.5">F1 Score</div>
                        <div className="font-bold text-white">
                          <AnimatedCounter
                            value={model.metrics.f1_score * 100}
                            decimals={1}
                            suffix="%"
                            duration={1000}
                          />
                        </div>
                      </div>
                    </div>
                  </>
                ) : (
                  <div className="text-xs text-gray-500 italic">No metrics available</div>
                )}

                {model.last_used && (
                  <div className="flex items-center gap-1.5 pt-1 border-t border-gray-700/30">
                    <Clock className="w-3 h-3 text-gray-600" />
                    <span className="text-xs text-gray-500">
                      {formatTimestamp(model.last_used)}
                    </span>
                  </div>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
