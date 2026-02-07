import React from 'react'
import { render, screen } from '@testing-library/react'
import { ErrorBoundary } from '@/components/ErrorBoundary'

describe('ErrorBoundary', () => {
  // Suppress console.error for these tests
  beforeEach(() => {
    jest.spyOn(console, 'error').mockImplementation(() => {})
  })

  afterEach(() => {
    jest.restoreAllMocks()
  })

  it('renders children when there is no error', () => {
    render(
      <ErrorBoundary>
        <div>Test Content</div>
      </ErrorBoundary>
    )

    expect(screen.getByText('Test Content')).toBeInTheDocument()
  })

  it('renders error UI when child component throws', () => {
    const ThrowError = () => {
      throw new Error('Test error')
    }

    render(
      <ErrorBoundary>
        <ThrowError />
      </ErrorBoundary>
    )

    expect(screen.getByText('Something went wrong')).toBeInTheDocument()
  })

  it('displays error details in collapsible section', () => {
    const errorMessage = 'Specific test error'
    const ThrowError = () => {
      throw new Error(errorMessage)
    }

    render(
      <ErrorBoundary>
        <ThrowError />
      </ErrorBoundary>
    )

    const details = screen.getByText('Error details')
    expect(details).toBeInTheDocument()
  })

  it('renders custom fallback when provided', () => {
    const ThrowError = () => {
      throw new Error('Test error')
    }

    const customFallback = <div>Custom Error UI</div>

    render(
      <ErrorBoundary fallback={customFallback}>
        <ThrowError />
      </ErrorBoundary>
    )

    expect(screen.getByText('Custom Error UI')).toBeInTheDocument()
  })

  it('has refresh button that reloads page', () => {
    const ThrowError = () => {
      throw new Error('Test error')
    }

    // Mock window.location.reload
    delete (window as any).location
    window.location = { reload: jest.fn() } as any

    render(
      <ErrorBoundary>
        <ThrowError />
      </ErrorBoundary>
    )

    const refreshButton = screen.getByText('Refresh Page')
    expect(refreshButton).toBeInTheDocument()
  })
})
