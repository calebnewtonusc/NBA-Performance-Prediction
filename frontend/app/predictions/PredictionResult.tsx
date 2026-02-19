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
} from '@/components/LazyChart'

interface PredictionResultProps {
  prediction: PredictionResponse
  homeTeam: string
  awayTeam: string
  predictionHistory: any[]
  onShare: () => void
  onExportCSV: () => void
}

export function PredictionResult({
  prediction,
  homeTeam,
  awayTeam,
  predictionHistory,
  onShare,
  onExportCSV,
}: PredictionResultProps) {
  return (
    <div className="space-y-6" role="region" aria-labelledby="results-heading" aria-live="polite">
      <div className="text-center space-y-4">
        <div
          className="text-4xl sm:text-6xl font-bold text-primary break-words"
          aria-label={`Predicted winner: ${prediction.prediction === 'home' ? homeTeam : awayTeam}`}
        >
          {prediction.prediction === 'home' ? homeTeam : awayTeam}
        </div>
        <div
          className="text-lg sm:text-2xl text-gray-300"
          aria-label={`Confidence: ${(prediction.confidence * 100).toFixed(1)} percent`}
        >
          Wins with {(prediction.confidence * 100).toFixed(1)}% confidence
        </div>
        <div className="inline-block px-3 sm:px-4 py-2 bg-primary/20 rounded-lg">
          <span className="text-base sm:text-lg font-medium">
            {prediction.prediction === 'home' ? 'Home' : 'Away'} Victory Predicted
          </span>
        </div>
      </div>

      <div className="pt-4 sm:pt-6 border-t border-gray-700">
        <h3 className="text-base sm:text-lg font-bold mb-3 sm:mb-4">Win Probability</h3>
        <ResponsiveContainer width="100%" height={180}>
          <BarChart
            data={[
              { team: homeTeam, probability: prediction.home_win_probability },
              { team: awayTeam, probability: prediction.away_win_probability },
            ]}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="team" stroke="#9CA3AF" />
            <YAxis stroke="#9CA3AF" />
            <Tooltip
              contentStyle={{
                backgroundColor: '#262730',
                border: '1px solid #374151',
                borderRadius: '8px',
              }}
            />
            <Bar dataKey="probability" fill="#FF6B6B" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-6 border-t border-gray-700">
        <div className="bg-background p-4 rounded-lg border border-gray-600">
          <div className="text-gray-400 text-xs sm:text-sm uppercase tracking-wider">Home Team</div>
          <div className="text-lg sm:text-xl font-bold mt-1">{homeTeam}</div>
          <div className="text-primary font-bold mt-2 text-base sm:text-lg">
            {(prediction.home_win_probability * 100).toFixed(1)}% to win
          </div>
        </div>
        <div className="bg-background p-4 rounded-lg border border-gray-600">
          <div className="text-gray-400 text-xs sm:text-sm uppercase tracking-wider">Away Team</div>
          <div className="text-lg sm:text-xl font-bold mt-1">{awayTeam}</div>
          <div className="text-primary font-bold mt-2 text-base sm:text-lg">
            {(prediction.away_win_probability * 100).toFixed(1)}% to win
          </div>
        </div>
      </div>

      <div className="pt-6 border-t border-gray-700">
        <button
          onClick={onShare}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
          </svg>
          Share Prediction
        </button>
      </div>

      {predictionHistory.length > 0 && (
        <div className="pt-6 border-t border-gray-700">
          <button
            onClick={onExportCSV}
            className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
            Export {predictionHistory.length} Prediction{predictionHistory.length > 1 ? 's' : ''} to CSV
          </button>
        </div>
      )}
    </div>
  )
}
