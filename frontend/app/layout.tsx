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
          <footer className="mt-20 pb-12">
            <div className="container mx-auto px-4 flex justify-center">
              <a
                href="https://calebnewton.me"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-4 px-8 py-4 bg-white bg-opacity-60 rounded-full border-2 border-blue-200 shadow-md hover:shadow-xl hover:-translate-y-0.5 hover:border-blue-300 transition-all duration-300 no-underline"
              >
                <img
                  src="/caleb-usc.jpg"
                  alt="Caleb Newton at USC"
                  className="w-12 h-12 rounded-full object-cover border-2 border-blue-300 shadow-md"
                  style={{ objectPosition: 'center 30%' }}
                />
                <div className="flex flex-col items-start gap-1">
                  <span className="text-xs text-gray-400 uppercase tracking-wider font-semibold">
                    Built by
                  </span>
                  <span className="text-base text-gray-800 font-bold">
                    Caleb Newton
                  </span>
                </div>
              </a>
            </div>
          </footer>
        </div>
      </body>
    </html>
  )
}
