import type { Metadata } from 'next'
import './globals.css'
import Navigation from '@/components/Navigation'
import { ErrorBoundary } from '@/components/ErrorBoundary'

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
        <ErrorBoundary>
          <div className="min-h-screen bg-background">
            <Navigation />
            <main className="container mx-auto px-4 py-8">
              {children}
            </main>

          {/* Footer */}
          <footer className="mt-20 pt-12 pb-12 bg-gradient-to-br from-gray-800/30 to-gray-900/30 border-t-2 border-gray-700 rounded-t-3xl">
            <div className="container mx-auto px-4 flex flex-col items-center gap-6">
              <a
                href="https://calebnewton.me"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-4 px-8 py-6 bg-secondary/60 backdrop-blur-sm rounded-full border-2 border-primary/30 shadow-md hover:shadow-xl hover:-translate-y-0.5 hover:border-primary/60 transition-all duration-300 no-underline"
                style={{ backgroundColor: 'rgba(38, 39, 48, 0.6)' }}
              >
                <img
                  src="/caleb-usc.jpg"
                  alt="Caleb Newton at USC"
                  className="w-12 h-12 rounded-full object-cover shadow-lg"
                  style={{
                    objectPosition: 'center 30%',
                    border: '2px solid #FF6B6B'
                  }}
                />
                <div className="flex flex-col items-start gap-1">
                  <span className="text-xs text-gray-400 uppercase tracking-wider font-semibold">
                    Built by
                  </span>
                  <span className="text-base text-white font-bold">
                    Caleb Newton
                  </span>
                </div>
              </a>
              <div className="text-center text-sm text-gray-400">
                <p className="font-semibold text-white mb-1">NBA Performance Prediction</p>
                <p className="text-xs">Machine learning predictions for NBA games and player stats</p>
              </div>
            </div>
          </footer>
        </div>
        </ErrorBoundary>
      </body>
    </html>
  )
}
