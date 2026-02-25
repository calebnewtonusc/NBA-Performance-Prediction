'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { Home, Zap, Users, TrendingUp, Database, Menu, X } from 'lucide-react'
import { HealthIndicator } from './HealthIndicator'

const navItems = [
  { href: '/', label: 'Home', icon: Home },
  { href: '/predictions', label: 'Predictions', icon: Zap },
  { href: '/players', label: 'Players', icon: Users },
  { href: '/performance', label: 'Performance', icon: TrendingUp },
  { href: '/explorer', label: 'Explorer', icon: Database },
]

const SF = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif"

export default function Navigation() {
  const pathname = usePathname()
  const [mobileOpen, setMobileOpen] = useState(false)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    setMobileOpen(false)
  }, [pathname])

  return (
    <nav
      className="sticky top-0 z-50"
      style={{
        height: '56px',
        backgroundColor: 'rgba(0,0,0,0.88)',
        backdropFilter: 'blur(20px) saturate(1.8)',
        WebkitBackdropFilter: 'blur(20px) saturate(1.8)',
        borderBottom: '0.5px solid rgba(255,255,255,0.08)',
        position: 'sticky',
        top: 0,
      }}
    >
      <div
        style={{
          maxWidth: '1152px',
          margin: '0 auto',
          padding: '0 20px',
          height: '56px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '24px',
        }}
      >
        {/* Logo */}
        <Link
          href="/"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            textDecoration: 'none',
            flexShrink: 0,
          }}
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4, ease: [0.25, 0.46, 0.45, 0.94] }}
            style={{
              width: '28px',
              height: '28px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #FF3B30 0%, #FF6B35 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '15px',
              boxShadow: '0 2px 8px rgba(255,59,48,0.4)',
            }}
          >
            🏀
          </motion.div>
          <motion.div
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.4, delay: 0.05, ease: [0.25, 0.46, 0.45, 0.94] }}
            style={{ display: 'flex', alignItems: 'baseline', gap: '0px' }}
          >
            <span
              style={{
                fontFamily: SF,
                fontSize: '17px',
                fontWeight: 800,
                color: '#ffffff',
                letterSpacing: '-0.5px',
              }}
            >
              NBA
            </span>
            <span
              style={{
                fontFamily: SF,
                fontSize: '17px',
                fontWeight: 800,
                color: '#FF3B30',
                letterSpacing: '-0.5px',
                marginLeft: '5px',
              }}
            >
              Prediction
            </span>
          </motion.div>
        </Link>

        {/* Desktop Nav — Center */}
        <div
          className="hidden lg:flex"
          style={{
            flex: 1,
            justifyContent: 'center',
            alignItems: 'center',
            gap: '2px',
          }}
        >
          {mounted &&
            navItems.map((item, i) => {
              const isActive = pathname === item.href
              return (
                <motion.div
                  key={item.href}
                  initial={{ opacity: 0, y: -6 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{
                    duration: 0.35,
                    delay: 0.06 + i * 0.05,
                    ease: [0.25, 0.46, 0.45, 0.94],
                  }}
                  style={{ position: 'relative' }}
                >
                  <Link
                    href={item.href}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '5px',
                      padding: '6px 14px',
                      borderRadius: '8px',
                      fontSize: '14px',
                      fontWeight: isActive ? 600 : 500,
                      color: isActive ? '#ffffff' : 'rgba(255,255,255,0.55)',
                      textDecoration: 'none',
                      fontFamily: SF,
                      letterSpacing: '-0.1px',
                      transition: 'color 150ms ease, background-color 150ms ease',
                      backgroundColor: isActive ? 'rgba(255,255,255,0.06)' : 'transparent',
                      position: 'relative',
                    }}
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
                    {item.label}
                    {/* Active dot indicator */}
                    {isActive && (
                      <motion.div
                        layoutId="nav-active-dot"
                        style={{
                          position: 'absolute',
                          bottom: '2px',
                          left: '50%',
                          transform: 'translateX(-50%)',
                          width: '4px',
                          height: '4px',
                          borderRadius: '50%',
                          backgroundColor: '#FF3B30',
                        }}
                        transition={{ type: 'spring', stiffness: 500, damping: 35 }}
                      />
                    )}
                  </Link>
                </motion.div>
              )
            })}
        </div>

        {/* Right side */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexShrink: 0 }}>
          <div className="hidden lg:block">
            <HealthIndicator />
          </div>

          {/* Mobile controls */}
          <div className="flex lg:hidden items-center gap-2">
            <HealthIndicator />
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              aria-label="Toggle menu"
              style={{
                width: '32px',
                height: '32px',
                borderRadius: '8px',
                background: 'rgba(255,255,255,0.06)',
                border: '0.5px solid rgba(255,255,255,0.1)',
                color: 'rgba(255,255,255,0.75)',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <AnimatePresence mode="wait" initial={false}>
                {mobileOpen ? (
                  <motion.div
                    key="x"
                    initial={{ opacity: 0, rotate: -90 }}
                    animate={{ opacity: 1, rotate: 0 }}
                    exit={{ opacity: 0, rotate: 90 }}
                    transition={{ duration: 0.15 }}
                  >
                    <X style={{ width: '16px', height: '16px' }} />
                  </motion.div>
                ) : (
                  <motion.div
                    key="menu"
                    initial={{ opacity: 0, rotate: 90 }}
                    animate={{ opacity: 1, rotate: 0 }}
                    exit={{ opacity: 0, rotate: -90 }}
                    transition={{ duration: 0.15 }}
                  >
                    <Menu style={{ width: '16px', height: '16px' }} />
                  </motion.div>
                )}
              </AnimatePresence>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Dropdown */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, y: -8, scaleY: 0.95 }}
            animate={{ opacity: 1, y: 0, scaleY: 1 }}
            exit={{ opacity: 0, y: -8, scaleY: 0.95 }}
            transition={{ duration: 0.2, ease: [0.25, 0.46, 0.45, 0.94] }}
            style={{
              transformOrigin: 'top',
              backgroundColor: 'rgba(0,0,0,0.96)',
              backdropFilter: 'blur(20px) saturate(1.8)',
              WebkitBackdropFilter: 'blur(20px) saturate(1.8)',
              borderBottom: '0.5px solid rgba(255,255,255,0.08)',
              padding: '8px 20px 16px',
            }}
            className="lg:hidden"
          >
            {navItems.map((item, i) => {
              const Icon = item.icon
              const isActive = pathname === item.href
              return (
                <motion.div
                  key={item.href}
                  initial={{ opacity: 0, x: -12 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.2, delay: i * 0.04 }}
                >
                  <Link
                    href={item.href}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                      padding: '12px 14px',
                      borderRadius: '12px',
                      fontSize: '15px',
                      fontWeight: isActive ? 600 : 500,
                      color: isActive ? '#ffffff' : 'rgba(255,255,255,0.6)',
                      backgroundColor: isActive ? 'rgba(255,59,48,0.1)' : 'transparent',
                      textDecoration: 'none',
                      fontFamily: SF,
                      letterSpacing: '-0.1px',
                      marginBottom: '2px',
                    }}
                  >
                    <div
                      style={{
                        width: '32px',
                        height: '32px',
                        borderRadius: '8px',
                        backgroundColor: isActive ? 'rgba(255,59,48,0.15)' : 'rgba(255,255,255,0.06)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        flexShrink: 0,
                      }}
                    >
                      <Icon
                        style={{
                          width: '15px',
                          height: '15px',
                          color: isActive ? '#FF3B30' : 'rgba(255,255,255,0.45)',
                        }}
                      />
                    </div>
                    {item.label}
                    {isActive && (
                      <div
                        style={{
                          marginLeft: 'auto',
                          width: '6px',
                          height: '6px',
                          borderRadius: '50%',
                          backgroundColor: '#FF3B30',
                        }}
                      />
                    )}
                  </Link>
                </motion.div>
              )
            })}
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  )
}
