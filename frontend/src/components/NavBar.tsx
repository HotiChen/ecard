'use client'

export type Tab = 'compose' | 'schedule' | 'analytics' | 'ai' | 'subscription'

interface NavBarProps {
  active: Tab
  onNavigate: (tab: Tab) => void
}

const TABS: { id: Tab; label: string }[] = [
  { id: 'compose', label: '發文' },
  { id: 'schedule', label: '排程' },
  { id: 'analytics', label: '數據' },
  { id: 'ai', label: 'AI 分析' },
  { id: 'subscription', label: '訂閱' },
]

export function NavBar({ active, onNavigate }: NavBarProps) {
  return (
    <nav className="flex gap-1 border-b border-gray-200 mb-8">
      {TABS.map(({ id, label }) => (
        <button
          key={id}
          onClick={() => onNavigate(id)}
          aria-current={active === id ? 'page' : undefined}
          className={`px-4 py-2 text-sm font-medium rounded-t-lg transition-colors ${
            active === id
              ? 'border-b-2 border-blue-600 text-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          {label}
        </button>
      ))}
    </nav>
  )
}
