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
      <body style={{ backgroundColor: '#000000', margin: 0 }}>
        <KeyboardShortcutsProvider>
          <ErrorBoundary>
            <div className="min-h-screen" style={{ backgroundColor: '#000000' }}>
              <Navigation />
              <main className="container mx-auto px-4 py-8">
                {children}
              </main>

              {/* Footer */}
              <footer
                className="mt-20 pt-10 pb-10"
                style={{
                  background: '#1c1c1e',
                  borderTop: '0.5px solid rgba(255,255,255,0.08)',
                  borderRadius: '20px 20px 0 0',
                }}
              >
                <div className="container mx-auto px-4 flex flex-col items-center gap-5">
                  <a
                    href="https://calebnewton.me"
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '14px',
                      padding: '14px 22px',
                      background: '#2c2c2e',
                      borderRadius: '16px',
                      border: '0.5px solid rgba(255,255,255,0.08)',
                      boxShadow: '0 1px 12px rgba(0,0,0,0.4)',
                      textDecoration: 'none',
                      transition: 'all 200ms ease',
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.border = '0.5px solid rgba(255,59,48,0.3)'
                      e.currentTarget.style.transform = 'translateY(-1px)'
                      e.currentTarget.style.boxShadow = '0 4px 20px rgba(0,0,0,0.5)'
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.border = '0.5px solid rgba(255,255,255,0.08)'
                      e.currentTarget.style.transform = 'translateY(0)'
                      e.currentTarget.style.boxShadow = '0 1px 12px rgba(0,0,0,0.4)'
                    }}
                  >
                    <Image
                      src="/caleb-usc.jpg"
                      alt="Caleb Newton at USC"
                      width={40}
                      height={40}
                      className="rounded-full object-cover"
                      style={{
                        objectPosition: 'center 30%',
                        border: '2px solid #FF3B30',
                        flexShrink: 0,
                      }}
                    />
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
                      <span
                        style={{
                          fontSize: '11px',
                          fontWeight: 600,
                          color: 'rgba(255,255,255,0.45)',
                          textTransform: 'uppercase',
                          letterSpacing: '0.5px',
                        }}
                      >
                        Built by
                      </span>
                      <span
                        style={{
                          fontSize: '15px',
                          fontWeight: 700,
                          color: '#ffffff',
                          letterSpacing: '-0.2px',
                        }}
                      >
                        Caleb Newton
                      </span>
                    </div>
                  </a>

                  <div style={{ textAlign: 'center' }}>
                    <p
                      style={{
                        fontSize: '14px',
                        fontWeight: 700,
                        color: '#ffffff',
                        marginBottom: '4px',
                        letterSpacing: '-0.2px',
                      }}
                    >
                      NBA Performance Prediction
                    </p>
                    <p
                      style={{
                        fontSize: '12px',
                        color: 'rgba(255,255,255,0.45)',
                      }}
                    >
                      Machine learning predictions for NBA games and player stats
                    </p>
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
                  background: '#2c2c2e',
                  border: '0.5px solid rgba(255,255,255,0.1)',
                  color: '#ffffff',
                  fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif",
                },
              }}
            />
          </ErrorBoundary>
        </KeyboardShortcutsProvider>
      </body>
    </html>
  )
}
