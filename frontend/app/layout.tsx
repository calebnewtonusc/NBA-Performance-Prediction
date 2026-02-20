import type { Metadata } from 'next'
import Image from 'next/image'
import './globals.css'
import Navigation from '@/components/Navigation'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { KeyboardShortcutsProvider } from '@/components/KeyboardShortcutsProvider'
import { Toaster } from 'sonner'

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
        <KeyboardShortcutsProvider>
          <ErrorBoundary>
            <div className="min-h-screen" style={{ backgroundColor: '#0A0E1A' }}>
              <Navigation />
              <main className="container mx-auto px-4 py-8">
                {children}
              </main>

          {/* Footer */}
          <footer className="mt-20 pt-12 pb-12 border-t rounded-t-3xl" style={{ background: 'linear-gradient(135deg, rgba(17,24,39,0.8), rgba(10,14,26,0.9))', borderColor: 'rgba(55,65,81,0.4)' }}>
            <div className="container mx-auto px-4 flex flex-col items-center gap-6">
              <a
                href="https://calebnewton.me"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-4 px-8 py-6 bg-secondary/60 backdrop-blur-sm rounded-full border-2 border-primary/30 shadow-md hover:shadow-xl hover:-translate-y-0.5 hover:border-primary/60 transition-all duration-300 no-underline"
                style={{ backgroundColor: 'rgba(38, 39, 48, 0.6)' }}
              >
                <Image
                  src="/caleb-usc.jpg"
                  alt="Caleb Newton at USC"
                  width={48}
                  height={48}
                  className="rounded-full object-cover shadow-lg"
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
        <Toaster
          theme="dark"
          position="top-right"
          richColors
          closeButton
          toastOptions={{
            style: {
              background: '#1F2937',
              border: '1px solid #374151',
              color: '#F3F4F6',
            },
          }}
        />
          </ErrorBoundary>
        </KeyboardShortcutsProvider>
      </body>
    </html>
  )
}
