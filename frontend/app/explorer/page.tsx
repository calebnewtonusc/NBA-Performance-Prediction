import type { Metadata } from 'next'
import ExplorerClient from './ExplorerClient'

export const metadata: Metadata = {
  title: 'Data Explorer | NBA Performance Prediction',
  description: 'Browse and filter historical NBA game data, team statistics, and season records to uncover trends and patterns.',
}

export default function Explorer() {
  return <ExplorerClient />
}
