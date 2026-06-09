'use client'

import { useState } from 'react'

interface ScheduleFormProps {
  content: string
  platforms: string[]
}

type State = 'idle' | 'loading' | 'success' | 'error'

export function ScheduleForm({ content, platforms }: ScheduleFormProps) {
  const [scheduledAt, setScheduledAt] = useState('')
  const [state, setState] = useState<State>('idle')

  const disabled = !content || platforms.length === 0 || !scheduledAt

  async function handleSubmit() {
    setState('loading')
    try {
      const res = await fetch('/api/v1/schedules', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content, platforms, scheduled_at: scheduledAt }),
      })
      setState(res.ok ? 'success' : 'error')
    } catch {
      setState('error')
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col gap-1">
        <label htmlFor="schedule-datetime" className="text-sm font-medium text-gray-700">
          排程時間
        </label>
        <input
          id="schedule-datetime"
          type="datetime-local"
          value={scheduledAt}
          onChange={(e) => setScheduledAt(e.target.value)}
          className="rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>

      <button
        onClick={handleSubmit}
        disabled={disabled || state === 'loading'}
        className="self-start rounded-lg bg-blue-600 px-6 py-2 text-sm font-semibold text-white disabled:opacity-40"
      >
        建立排程
      </button>

      {state === 'success' && (
        <p className="text-sm font-medium text-green-600">排程已建立！</p>
      )}
      {state === 'error' && (
        <p className="text-sm font-medium text-red-500">排程失敗，請稍後再試。</p>
      )}
    </div>
  )
}
