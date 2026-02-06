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
          <footer className="mt-20 pt-12 pb-12 bg-gradient-to-br from-orange-50/50 to-blue-50/50 border-t-2 border-orange-200 rounded-t-3xl">
            <div className="container mx-auto px-4 flex flex-col items-center gap-6">
              <a
                href="https://calebnewton.me"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-4 px-8 py-6 bg-white/70 backdrop-blur-sm rounded-full border-2 border-orange-200/60 shadow-md hover:shadow-xl hover:-translate-y-0.5 hover:border-orange-400/80 transition-all duration-300 no-underline"
              >
                <img
                  src="/caleb-usc.jpg"
                  alt="Caleb Newton at USC"
                  className="w-12 h-12 rounded-full object-cover border-2 border-orange-400 shadow-lg"
                  style={{ objectPosition: 'center 30%' }}
                />
                <div className="flex flex-col items-start gap-1">
                  <span className="text-xs text-orange-500 uppercase tracking-wider font-semibold">
                    Built by
                  </span>
                  <span className="text-base text-gray-900 font-bold">
                    Caleb Newton
                  </span>
                </div>
              </a>
              <div className="text-center text-sm text-gray-700">
                <p className="font-semibold text-gray-900 mb-1">NBA Performance Prediction</p>
                <p className="text-xs">Machine learning predictions for NBA games and player stats</p>
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  )
}
