'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { BarChart3, Home, Users, TrendingUp, Database } from 'lucide-react'
import { HealthIndicator } from './HealthIndicator'

const navItems = [
  { href: '/', label: 'Home', icon: Home },
  { href: '/predictions', label: 'Game Predictions', icon: BarChart3 },
  { href: '/players', label: 'Player Stats', icon: Users },
  { href: '/performance', label: 'Model Performance', icon: TrendingUp },
  { href: '/explorer', label: 'Data Explorer', icon: Database },
]

export default function Navigation() {
  const pathname = usePathname()

  return (
    <nav className="bg-secondary border-b border-gray-700">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-2">
            <BarChart3 className="h-8 w-8 text-primary" />
            <span className="text-xl font-bold">NBA Predictions</span>
          </div>
          <div className="flex items-center gap-6">
            <div className="flex space-x-4">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = pathname === item.href
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-primary text-white'
                        : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{item.label}</span>
                  </Link>
                )
              })}
            </div>
            <HealthIndicator />
          </div>
        </div>
      </div>
    </nav>
  )
}
