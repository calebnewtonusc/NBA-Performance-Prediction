'use client'

import Image from 'next/image'
import { motion } from 'framer-motion'

const SF = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', sans-serif"

export function FooterBuiltBy() {
  return (
    <motion.a
      href="https://calebnewton.me"
      target="_blank"
      rel="noopener noreferrer"
      whileHover={{ y: -2, borderColor: 'rgba(255,59,48,0.35)', boxShadow: '0 8px 28px rgba(0,0,0,0.5)' }}
      transition={{ duration: 0.18, ease: [0.25, 0.46, 0.45, 0.94] }}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '14px',
        padding: '14px 24px',
        background: '#2c2c2e',
        borderRadius: '100px',
        border: '0.5px solid rgba(255,255,255,0.1)',
        boxShadow: '0 2px 16px rgba(0,0,0,0.4)',
        textDecoration: 'none',
      }}
    >
      <Image
        src="/caleb-usc.jpg"
        alt="Caleb Newton"
        width={36}
        height={36}
        style={{
          borderRadius: '50%',
          objectFit: 'cover',
          objectPosition: 'center 30%',
          border: '2px solid #FF3B30',
          flexShrink: 0,
        }}
      />
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1px' }}>
        <span
          style={{
            fontFamily: SF,
            fontSize: '11px',
            fontWeight: 600,
            color: 'rgba(255,255,255,0.45)',
            textTransform: 'uppercase',
            letterSpacing: '1px',
          }}
        >
          Built by
        </span>
        <span
          style={{
            fontFamily: SF,
            fontSize: '15px',
            fontWeight: 700,
            color: '#ffffff',
            letterSpacing: '-0.3px',
          }}
        >
          Caleb Newton
        </span>
      </div>
    </motion.a>
  )
}
