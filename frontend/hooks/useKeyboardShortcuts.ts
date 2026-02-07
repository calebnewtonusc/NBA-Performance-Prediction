/**
 * useKeyboardShortcuts Hook
 *
 * Global keyboard shortcuts for the application
 */

'use client'

import { useEffect } from 'react'

export function useKeyboardShortcuts() {
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      // Cmd/Ctrl + K = Focus search input
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        const searchInput = document.querySelector<HTMLInputElement>(
          'input[type="text"][placeholder*="player"],' +
          'input[type="text"][placeholder*="Player"],' +
          'input[type="search"]'
        )
        searchInput?.focus()
        searchInput?.select()
      }

      // Cmd/Ctrl + Enter = Submit current form
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        e.preventDefault()
        const submitButton = document.querySelector<HTMLButtonElement>(
          'button[type="submit"]:not([disabled])'
        )
        submitButton?.click()
      }

      // Escape = Clear focused input or close modals
      if (e.key === 'Escape') {
        const activeElement = document.activeElement as HTMLElement
        if (activeElement?.tagName === 'INPUT' || activeElement?.tagName === 'TEXTAREA') {
          activeElement.blur()
        }
      }

      // ? = Show keyboard shortcuts help
      if (e.key === '?' && !e.metaKey && !e.ctrlKey) {
        const target = e.target as HTMLElement
        // Don't trigger if typing in an input
        if (target.tagName !== 'INPUT' && target.tagName !== 'TEXTAREA') {
          e.preventDefault()
          showShortcutsHelp()
        }
      }
    }

    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [])
}

function showShortcutsHelp() {
  const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0
  const mod = isMac ? '⌘' : 'Ctrl'

  alert(`Keyboard Shortcuts:

${mod}+K  →  Focus search
${mod}+↵  →  Submit form
Esc    →  Clear/Close
?      →  Show this help`)
}
