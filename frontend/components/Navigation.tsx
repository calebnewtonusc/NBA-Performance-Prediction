'use client'

import { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { usePathname } from 'next/navigation'
import { BarChart3, Home, Users, TrendingUp, Database, Menu, X, Zap } from 'lucide-react'
import { HealthIndicator } from './HealthIndicator'

const navItems = [
  { href: '/', label: 'Home', icon: Home },
  { href: '/predictions', label: 'Predictions', icon: Zap },
  { href: '/players', label: 'Players', icon: Users },
  { href: '/performance', label: 'Performance', icon: TrendingUp },
  { href: '/explorer', label: 'Explorer', icon: Database },
]

export default function Navigation() {
  const pathname = usePathname()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <nav
      className="sticky top-0 z-50"
      style={{
        backgroundColor: 'rgba(0,0,0,0.85)',
        backdropFilter: 'blur(20px) saturate(1.8)',
        WebkitBackdropFilter: 'blur(20px) saturate(1.8)',
        borderBottom: '0.5px solid rgba(255,255,255,0.08)',
      }}
    >
      <div className="container mx-auto px-4">
        {/* Desktop Navigation */}
        <div className="flex items-center justify-between h-14">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="relative flex-shrink-0">
              <Image
                src="/nba-logo.png"
                alt="NBA Predictions Logo"
                width={28}
                height={28}
                className="rounded-lg"
                priority
                unoptimized
              />
            </div>
            <div className="hidden sm:block">
              <span
                style={{
                  fontSize: '15px',
                  fontWeight: 800,
                  color: '#ffffff',
                  letterSpacing: '-0.3px',
                  fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif",
                }}
              >
                NBA
              </span>
              <span
                style={{
                  fontSize: '15px',
                  fontWeight: 800,
                  color: '#FF3B30',
                  letterSpacing: '-0.3px',
                  marginLeft: '5px',
                  fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif",
                }}
              >
                Prediction
              </span>
            </div>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden lg:flex items-center gap-0.5">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = pathname === item.href
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  style={
                    isActive
                      ? {
                          backgroundColor: 'rgba(255,59,48,0.12)',
                          color: '#ffffff',
                          border: '0.5px solid rgba(255,59,48,0.25)',
                          borderRadius: '10px',
                          padding: '6px 12px',
                          fontSize: '13px',
                          fontWeight: 600,
                          display: 'flex',
                          alignItems: 'center',
                          gap: '5px',
                          transition: 'all 150ms ease',
                          textDecoration: 'none',
                        }
                      : {
                          color: 'rgba(255,255,255,0.55)',
                          borderRadius: '10px',
                          padding: '6px 12px',
                          fontSize: '13px',
                          fontWeight: 600,
                          display: 'flex',
                          alignItems: 'center',
                          gap: '5px',
                          transition: 'all 150ms ease',
                          textDecoration: 'none',
                        }
                  }
                  onMouseEnter={(e) => {
                    if (!isActive) {
                      e.currentTarget.style.color = '#ffffff'
                      e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.06)'
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (!isActive) {
                      e.currentTarget.style.color = 'rgba(255,255,255,0.55)'
                      e.currentTarget.style.backgroundColor = 'transparent'
                    }
                  }}
                >
                  <Icon style={{ width: '13px', height: '13px', flexShrink: 0 }} />
                  <span>{item.label}</span>
                </Link>
              )
            })}
          </div>

          {/* Right side */}
          <div className="flex items-center gap-3">
            <div className="hidden lg:block">
              <HealthIndicator />
            </div>

            {/* Mobile Menu Button */}
            <div className="lg:hidden flex items-center gap-2">
              <HealthIndicator />
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                style={{
                  padding: '6px',
                  borderRadius: '8px',
                  color: 'rgba(255,255,255,0.55)',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  transition: 'all 150ms ease',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.color = '#ffffff'
                  e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.06)'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.color = 'rgba(255,255,255,0.55)'
                  e.currentTarget.style.backgroundColor = 'transparent'
                }}
                aria-label="Toggle mobile menu"
              >
                {mobileMenuOpen ? (
                  <X style={{ width: '18px', height: '18px' }} />
                ) : (
                  <Menu style={{ width: '18px', height: '18px' }} />
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div
            className="lg:hidden py-3 space-y-0.5"
            style={{ borderTop: '0.5px solid rgba(255,255,255,0.08)' }}
          >
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = pathname === item.href
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    padding: '10px 12px',
                    borderRadius: '10px',
                    fontSize: '14px',
                    fontWeight: 600,
                    color: isActive ? '#ffffff' : 'rgba(255,255,255,0.55)',
                    backgroundColor: isActive ? 'rgba(255,59,48,0.12)' : 'transparent',
                    transition: 'all 150ms ease',
                    textDecoration: 'none',
                  }}
                >
                  <Icon style={{ width: '15px', height: '15px', flexShrink: 0 }} />
                  <span>{item.label}</span>
                </Link>
              )
            })}
          </div>
        )}
      </div>
    </nav>
  )
}
