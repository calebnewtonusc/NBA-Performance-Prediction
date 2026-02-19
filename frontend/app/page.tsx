import type { Metadata } from 'next'
import HomeClient from './HomeClient'

export const metadata: Metadata = {
  title: 'NBA Performance Prediction | ML-Powered Game Forecasts',
  description: 'Use machine learning to predict NBA game outcomes, analyze player performance, and explore historical game data.',
}

export default function Home() {
  return <HomeClient />
}
