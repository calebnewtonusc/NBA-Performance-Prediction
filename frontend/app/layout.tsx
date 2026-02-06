import type { Metadata } from 'next'
import './globals.css'
import Navigation from '@/components/Navigation'

export const metadata: Metadata = {
  title: 'NBA Performance Prediction',
  description: 'Machine learning-powered NBA game predictions',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen bg-background">
          <Navigation />
          <main className="container mx-auto px-4 py-8">
            {children}
          </main>

          {/* Footer */}
          <footer className="mt-12 border-t border-gray-200 bg-gray-50">
            <div className="container mx-auto px-4 py-6 text-center">
              <p className="text-sm font-semibold text-gray-900">
                NBA Performance Prediction v1.0.0
              </p>
              <p className="text-xs text-gray-700 mt-2">
                Machine learning platform for NBA game and player predictions
              </p>
              <p className="text-xs text-gray-600 mt-3">
                Built by <a href="https://calebnewton.me" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-700 font-medium transition-colors">Caleb Newton</a>
              </p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  )
}
