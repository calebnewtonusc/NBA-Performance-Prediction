'use client'

interface SkeletonProps {
  className?: string
}

export function Skeleton({ className = '' }: SkeletonProps) {
  return (
    <div
      className={`animate-pulse bg-gradient-to-r from-gray-700 via-gray-600 to-gray-700 bg-[length:200%_100%] rounded ${className}`}
      style={{
        animation: 'skeleton-shimmer 1.8s ease-in-out infinite',
      }}
    />
  )
}

export function StatCardSkeleton() {
  return (
    <div className="bg-secondary p-6 rounded-xl border border-gray-700/50">
      <div className="flex items-center justify-between">
        <div className="space-y-2 flex-1">
          <Skeleton className="h-3 w-20" />
          <Skeleton className="h-8 w-28" />
          <Skeleton className="h-3 w-16" />
        </div>
        <Skeleton className="h-12 w-12 rounded-xl" />
      </div>
    </div>
  )
}

export function PlayerCardSkeleton() {
  return (
    <div className="bg-secondary p-4 rounded-xl border border-gray-700/50">
      <div className="flex items-center gap-3">
        <Skeleton className="h-14 w-14 rounded-full" />
        <div className="space-y-2 flex-1">
          <Skeleton className="h-4 w-32" />
          <Skeleton className="h-3 w-20" />
          <Skeleton className="h-3 w-24" />
        </div>
      </div>
    </div>
  )
}

export function ChartSkeleton({ height = 300 }: { height?: number }) {
  return (
    <div className="bg-secondary p-6 rounded-xl border border-gray-700/50">
      <Skeleton className="h-5 w-40 mb-4" />
      <div className="relative" style={{ height }}>
        <Skeleton className="w-full h-full rounded-lg" />
        {/* Fake bar chart silhouette */}
        <div className="absolute bottom-0 left-0 right-0 flex items-end gap-3 px-8 pb-4 h-3/4">
          {[60, 80, 45, 90, 70, 55, 85].map((h, i) => (
            <div
              key={i}
              className="flex-1 bg-gray-600/30 rounded-t"
              style={{ height: `${h}%` }}
            />
          ))}
        </div>
      </div>
    </div>
  )
}

export function PredictionSkeleton() {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="text-center space-y-4">
        <Skeleton className="h-20 w-48 mx-auto rounded-xl" />
        <Skeleton className="h-8 w-64 mx-auto" />
        <Skeleton className="h-10 w-48 mx-auto rounded-full" />
      </div>
      <div className="pt-6 border-t border-gray-700">
        <Skeleton className="h-5 w-32 mb-4" />
        <div className="flex justify-center">
          <Skeleton className="h-56 w-56 rounded-full" />
        </div>
      </div>
      <div className="grid grid-cols-2 gap-4 pt-6 border-t border-gray-700">
        <Skeleton className="h-24 rounded-xl" />
        <Skeleton className="h-24 rounded-xl" />
      </div>
    </div>
  )
}

export function MatchupSkeleton() {
  return (
    <div className="space-y-4 animate-pulse">
      {[1, 2, 3].map((i) => (
        <div key={i} className="bg-secondary p-4 rounded-xl border border-gray-700/50">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Skeleton className="h-10 w-10 rounded-lg" />
              <div className="space-y-2">
                <Skeleton className="h-4 w-24" />
                <Skeleton className="h-3 w-16" />
              </div>
            </div>
            <Skeleton className="h-6 w-6 rounded" />
            <div className="flex items-center gap-4">
              <div className="space-y-2 text-right">
                <Skeleton className="h-4 w-24" />
                <Skeleton className="h-3 w-16" />
              </div>
              <Skeleton className="h-10 w-10 rounded-lg" />
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export function PickOfDaySkeleton() {
  return (
    <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl border border-gray-600 p-6 animate-pulse">
      <div className="flex items-center gap-2 mb-4">
        <Skeleton className="h-5 w-5 rounded-full" />
        <Skeleton className="h-4 w-28" />
      </div>
      <div className="flex items-center justify-between">
        <div className="text-center space-y-2">
          <Skeleton className="h-12 w-12 rounded-xl mx-auto" />
          <Skeleton className="h-4 w-16 mx-auto" />
          <Skeleton className="h-3 w-20 mx-auto" />
        </div>
        <div className="text-center space-y-1">
          <Skeleton className="h-4 w-8 mx-auto" />
          <Skeleton className="h-6 w-20 mx-auto" />
        </div>
        <div className="text-center space-y-2">
          <Skeleton className="h-12 w-12 rounded-xl mx-auto" />
          <Skeleton className="h-4 w-16 mx-auto" />
          <Skeleton className="h-3 w-20 mx-auto" />
        </div>
      </div>
    </div>
  )
}

// Add global keyframe via style tag (injected once)
export function SkeletonStyles() {
  return (
    <style>{`
      @keyframes skeleton-shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
      }
    `}</style>
  )
}
