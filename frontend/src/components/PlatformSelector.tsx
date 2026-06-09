'use client'

export type Platform = 'threads' | 'instagram' | 'x'

const PLATFORMS: { id: Platform; label: string }[] = [
  { id: 'threads', label: 'Threads' },
  { id: 'instagram', label: 'Instagram' },
  { id: 'x', label: 'X (Twitter)' },
]

interface PlatformSelectorProps {
  selected: Platform[]
  onChange: (platforms: Platform[]) => void
}

export function PlatformSelector({ selected, onChange }: PlatformSelectorProps) {
  function toggle(platform: Platform) {
    if (selected.includes(platform)) {
      onChange(selected.filter((p) => p !== platform))
    } else {
      onChange([...selected, platform])
    }
  }

  return (
    <div className="flex flex-wrap gap-3">
      {PLATFORMS.map(({ id, label }) => (
        <label
          key={id}
          className="flex items-center gap-2 cursor-pointer select-none"
        >
          <input
            type="checkbox"
            aria-label={label}
            checked={selected.includes(id)}
            onChange={() => toggle(id)}
            className="w-4 h-4 rounded accent-blue-600"
          />
          <span className="text-sm font-medium text-gray-700">{label}</span>
        </label>
      ))}
    </div>
  )
}
