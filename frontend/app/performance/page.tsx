import type { Metadata } from 'next'
import PerformanceClient from './PerformanceClient'

export const metadata: Metadata = {
  title: 'Model Performance | NBA Performance Prediction',
  description: 'View detailed accuracy metrics, precision, recall, F1 scores, data drift detection, and monitoring alerts for NBA prediction models.',
}

export default function Performance() {
  return <PerformanceClient />
}
