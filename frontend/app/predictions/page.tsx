import type { Metadata } from 'next'
import PredictionsClient from './PredictionsClient'

export const metadata: Metadata = {
  title: 'Game Predictions | NBA Performance Prediction',
  description: 'Predict NBA game outcomes using live team statistics and machine learning models. Compare predictions across multiple models.',
}

export default function Predictions() {
  return <PredictionsClient />
}
