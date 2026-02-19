import type { Metadata } from 'next'
import PlayersClient from './PlayersClient'

export const metadata: Metadata = {
  title: 'Player Stats | NBA Performance Prediction',
  description: 'Search NBA players and analyze their season statistics including points, rebounds, assists, and shooting percentages.',
}

export default function Players() {
  return <PlayersClient />
}
