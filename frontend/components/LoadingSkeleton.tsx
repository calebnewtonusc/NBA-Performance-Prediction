/**
 * LoadingSkeleton Components
 *
 * Reusable skeleton loading states for different UI elements.
 * These provide a better UX than plain "Loading..." text.
 */

export function SkeletonCard() {
  return (
    <div className="animate-pulse bg-secondary rounded-lg p-6 border border-gray-700">
      <div className="h-4 bg-gray-700 rounded w-3/4 mb-4"></div>
      <div className="h-4 bg-gray-700 rounded w-1/2 mb-2"></div>
      <div className="h-4 bg-gray-700 rounded w-5/6"></div>
    </div>
  )
}

export function SkeletonCardGrid({ count = 3 }: { count?: number }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {Array.from({ length: count }).map((_, i) => (
        <SkeletonCard key={i} />
      ))}
    </div>
  )
}

export function SkeletonTable({ rows = 5 }: { rows?: number }) {
  return (
    <div className="space-y-3">
      {/* Header */}
      <div className="flex gap-4 p-4 bg-background rounded-lg">
        <div className="h-4 bg-gray-700 rounded w-1/4"></div>
        <div className="h-4 bg-gray-700 rounded w-1/4"></div>
        <div className="h-4 bg-gray-700 rounded w-1/4"></div>
        <div className="h-4 bg-gray-700 rounded w-1/4"></div>
      </div>

      {/* Rows */}
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="animate-pulse flex gap-4 p-4 bg-secondary rounded-lg border border-gray-700">
          <div className="h-4 bg-gray-700 rounded w-1/4"></div>
          <div className="h-4 bg-gray-700 rounded w-1/4"></div>
          <div className="h-4 bg-gray-700 rounded w-1/4"></div>
          <div className="h-4 bg-gray-700 rounded w-1/4"></div>
        </div>
      ))}
    </div>
  )
}

export function SkeletonText({ lines = 3 }: { lines?: number }) {
  return (
    <div className="space-y-2 animate-pulse">
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className="h-4 bg-gray-700 rounded"
          style={{ width: `${Math.random() * 30 + 70}%` }}
        ></div>
      ))}
    </div>
  )
}

export function SkeletonStats() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 animate-pulse">
      {Array.from({ length: 4 }).map((_, i) => (
        <div key={i} className="bg-secondary p-6 rounded-lg border border-gray-700">
          <div className="h-3 bg-gray-700 rounded w-1/2 mb-3"></div>
          <div className="h-8 bg-gray-700 rounded w-3/4"></div>
        </div>
      ))}
    </div>
  )
}

export function SkeletonPlayerCard() {
  return (
    <div className="animate-pulse bg-secondary p-4 rounded-lg border border-gray-700">
      <div className="flex items-start gap-4">
        {/* Avatar */}
        <div className="w-12 h-12 bg-gray-700 rounded-full"></div>

        {/* Info */}
        <div className="flex-1 space-y-2">
          <div className="h-5 bg-gray-700 rounded w-3/4"></div>
          <div className="h-4 bg-gray-700 rounded w-1/2"></div>
          <div className="h-3 bg-gray-700 rounded w-2/3"></div>
        </div>
      </div>
    </div>
  )
}

export function SkeletonPlayerGrid({ count = 6 }: { count?: number }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {Array.from({ length: count }).map((_, i) => (
        <SkeletonPlayerCard key={i} />
      ))}
    </div>
  )
}

export function SkeletonChart() {
  return (
    <div className="bg-secondary p-6 rounded-lg border border-gray-700 animate-pulse">
      <div className="h-6 bg-gray-700 rounded w-1/3 mb-4"></div>
      <div className="h-64 bg-gray-700/50 rounded flex items-end justify-around gap-2 p-4">
        {Array.from({ length: 6 }).map((_, i) => (
          <div
            key={i}
            className="bg-gray-700 rounded-t w-full"
            style={{ height: `${Math.random() * 60 + 40}%` }}
          ></div>
        ))}
      </div>
    </div>
  )
}

export function SkeletonPredictionResult() {
  return (
    <div className="bg-secondary rounded-lg border border-gray-700 p-6 animate-pulse">
      <div className="h-6 bg-gray-700 rounded w-1/2 mb-6 mx-auto"></div>

      <div className="grid grid-cols-2 gap-8 mb-6">
        <div className="text-center space-y-3">
          <div className="h-8 bg-gray-700 rounded w-3/4 mx-auto"></div>
          <div className="h-12 bg-gray-700 rounded w-1/2 mx-auto"></div>
        </div>
        <div className="text-center space-y-3">
          <div className="h-8 bg-gray-700 rounded w-3/4 mx-auto"></div>
          <div className="h-12 bg-gray-700 rounded w-1/2 mx-auto"></div>
        </div>
      </div>

      <div className="h-4 bg-gray-700 rounded w-2/3 mx-auto"></div>
    </div>
  )
}

export function SkeletonForm() {
  return (
    <div className="space-y-4 animate-pulse">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i}>
          <div className="h-4 bg-gray-700 rounded w-1/4 mb-2"></div>
          <div className="h-12 bg-gray-700 rounded w-full"></div>
        </div>
      ))}
      <div className="h-12 bg-gray-700 rounded w-full mt-6"></div>
    </div>
  )
}

export function SkeletonPageHeader() {
  return (
    <div className="space-y-2 animate-pulse mb-8">
      <div className="h-10 bg-gray-700 rounded w-1/3"></div>
      <div className="h-4 bg-gray-700 rounded w-2/3"></div>
    </div>
  )
}
