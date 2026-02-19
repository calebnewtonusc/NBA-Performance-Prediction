'use client'

interface ExplorerPaginationProps {
  currentPage: number
  totalPages: number
  loading: boolean
  onPageChange: (page: number) => void
}

export function ExplorerPagination({
  currentPage,
  totalPages,
  loading,
  onPageChange,
}: ExplorerPaginationProps) {
  if (totalPages <= 1) return null

  return (
    <div className="p-4 border-t border-gray-700 flex flex-col sm:flex-row items-center justify-between gap-4">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1 || loading}
        className="w-full sm:w-auto px-4 py-2 bg-background border border-gray-600 rounded-lg hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        Previous
      </button>

      <div className="flex items-center gap-1 sm:gap-2 flex-wrap justify-center">
        {currentPage > 3 && (
          <>
            <button
              onClick={() => onPageChange(1)}
              className="px-3 py-1 rounded hover:bg-gray-700 transition-colors"
            >
              1
            </button>
            {currentPage > 4 && <span className="text-gray-500">...</span>}
          </>
        )}

        {Array.from({ length: totalPages }, (_, i) => i + 1)
          .filter(
            (page) =>
              page === currentPage ||
              page === currentPage - 1 ||
              page === currentPage + 1 ||
              page === currentPage - 2 ||
              page === currentPage + 2
          )
          .map((page) => (
            <button
              key={page}
              onClick={() => onPageChange(page)}
              disabled={loading}
              className={`px-3 py-1 rounded transition-colors ${
                page === currentPage ? 'bg-primary text-white' : 'hover:bg-gray-700'
              }`}
            >
              {page}
            </button>
          ))}

        {currentPage < totalPages - 2 && (
          <>
            {currentPage < totalPages - 3 && <span className="text-gray-500">...</span>}
            <button
              onClick={() => onPageChange(totalPages)}
              className="px-3 py-1 rounded hover:bg-gray-700 transition-colors"
            >
              {totalPages}
            </button>
          </>
        )}
      </div>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages || loading}
        className="px-4 py-2 bg-background border border-gray-600 rounded-lg hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        Next
      </button>
    </div>
  )
}
