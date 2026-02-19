'use client'

import { Suspense } from 'react'
import { PredictionsInner } from './PredictionsInner'

// ---------------------------------------------------------------------------
// PredictionsContent — wraps PredictionsInner (which uses useSearchParams)
// inside a <Suspense> boundary to satisfy Next.js streaming requirements.
// ---------------------------------------------------------------------------

export function PredictionsContent() {
  return (
    <Suspense
      fallback={
        <div className="max-w-6xl mx-auto space-y-6 sm:space-y-8">
          <div>
            <h1 className="text-3xl sm:text-4xl font-bold">Game Predictions</h1>
            <p className="text-sm sm:text-base text-gray-400 mt-2">Loading...</p>
          </div>
        </div>
      }
    >
      <PredictionsInner />
    </Suspense>
  )
}
