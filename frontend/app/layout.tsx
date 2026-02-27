import type { Metadata } from 'next'
import './globals.css'
import Navigation from '@/components/Navigation'
import { FooterBuiltBy } from '@/components/FooterBuiltBy'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { KeyboardShortcutsProvider } from '@/components/KeyboardShortcutsProvider'
import { Toaster } from 'sonner'

export const metadata: Metadata = {
  title: 'NBA Performance Prediction',
  description: 'Machine learning-powered NBA game predictions',
  icons: {
    icon: [
      { url: '/favicon.svg', type: 'image/svg+xml' },
      { url: '/favicon.ico' },
    ],
  },
}

const SF = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', sans-serif"

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
                style={{
                  marginTop: '80px',
                  background: '#1c1c1e',
                  borderTop: '0.5px solid rgba(255,255,255,0.08)',
                  borderRadius: '20px 20px 0 0',
                  padding: '48px 20px 40px',
                }}
              >
                <div
                  style={{
                    maxWidth: '1152px',
                    margin: '0 auto',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '24px',
                  }}
                >
                  {/* Built by pill */}
                  <FooterBuiltBy />

                  {/* Project name */}
                  <div style={{ textAlign: 'center' }}>
                    <p
                      style={{
                        fontFamily: SF,
                        fontSize: '15px',
                        fontWeight: 700,
                        color: '#ffffff',
                        letterSpacing: '-0.3px',
                        marginBottom: '6px',
                      }}
                    >
                      NBA Performance Prediction
                    </p>
                    <p
                      style={{
                        fontFamily: SF,
                        fontSize: '13px',
                        color: 'rgba(255,255,255,0.45)',
                        lineHeight: 1.5,
                        maxWidth: '320px',
                      }}
                    >
                      Machine learning predictions for NBA games and player performance
                    </p>
                  </div>

                  {/* Separator */}
                  <div
                    style={{
                      width: '100%',
                      maxWidth: '480px',
                      height: '0.5px',
                      backgroundColor: 'rgba(255,255,255,0.08)',
                    }}
                  />

                  {/* Copyright */}
                  <p
                    style={{
                      fontFamily: SF,
                      fontSize: '12px',
                      color: 'rgba(255,255,255,0.3)',
                      letterSpacing: '0.2px',
                    }}
                  >
                    {new Date().getFullYear()} · For educational purposes only
                  </p>
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
                  fontFamily: SF,
                },
              }}
            />
          </ErrorBoundary>
        </KeyboardShortcutsProvider>
      </body>
    </html>
  )
}
