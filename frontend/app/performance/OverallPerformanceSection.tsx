'use client'

import { PerformanceMetrics } from '@/lib/api-client'
import { InfoTooltip } from '@/components/InfoTooltip'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from '@/components/LazyChart'

interface OverallPerformanceSectionProps {
  performance: PerformanceMetrics
}

export default function OverallPerformanceSection({ performance }: OverallPerformanceSectionProps) {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Overall Performance</h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-secondary p-6 rounded-lg border border-gray-700">
          <h3 className="text-xl font-semibold mb-4">Current Metrics</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-400 flex items-center">
                Accuracy:
                <InfoTooltip content="Percentage of correct predictions out of all predictions made. Higher is better." />
              </span>
              <span className="text-2xl font-bold text-green-500">
                {(performance.accuracy * 100).toFixed(1)}%
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-400 flex items-center">
                Precision:
                <InfoTooltip content="Of all positive predictions, how many were correct. Measures prediction reliability." />
              </span>
              <span className="text-xl font-semibold">
                {(performance.precision * 100).toFixed(1)}%
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-400 flex items-center">
                Recall:
                <InfoTooltip content="Of all actual positives, how many were correctly identified. Measures completeness." />
              </span>
              <span className="text-xl font-semibold">
                {(performance.recall * 100).toFixed(1)}%
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-400 flex items-center">
                F1 Score:
                <InfoTooltip content="Harmonic mean of precision and recall. Balanced measure of model performance." />
              </span>
              <span className="text-xl font-semibold">
                {(performance.f1_score * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        </div>

        <div className="bg-secondary p-6 rounded-lg border border-gray-700">
          <h3 className="text-xl font-semibold mb-4">Prediction Statistics</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-400">Total Predictions:</span>
              <span className="text-2xl font-bold">{performance.predictions_count}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-400">Correct:</span>
              <span className="text-xl font-semibold text-green-500">
                {performance.correct_predictions}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-400">Incorrect:</span>
              <span className="text-xl font-semibold text-red-500">
                {performance.incorrect_predictions}
              </span>
            </div>
            {performance.recent_accuracy && (
              <div className="flex justify-between items-center pt-3 border-t border-gray-600">
                <span className="text-gray-400">Recent Accuracy:</span>
                <span className="text-xl font-semibold">
                  {(performance.recent_accuracy * 100).toFixed(1)}%
                </span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Metrics Chart */}
      <div className="bg-secondary p-6 rounded-lg border border-gray-700 mt-6">
        <h3 className="text-xl font-semibold mb-4">Metrics Comparison</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            data={[
              { name: 'Accuracy', value: performance.accuracy * 100 },
              { name: 'Precision', value: performance.precision * 100 },
              { name: 'Recall', value: performance.recall * 100 },
              { name: 'F1 Score', value: performance.f1_score * 100 },
            ]}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="name" stroke="#9CA3AF" />
            <YAxis stroke="#9CA3AF" domain={[0, 100]} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1F2937',
                border: '1px solid #374151',
              }}
              formatter={(value: any) => `${value.toFixed(1)}%`}
            />
            <Bar dataKey="value" fill="#3B82F6" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
