'use client'

import { useState } from 'react'

interface PublishPanelProps {
  content: string
  platforms: string[]
}

type State = 'idle' | 'loading' | 'success' | 'error'

interface BackupResult {
  sha256: string
  proof_timestamp: string
}

export function PublishPanel({ content, platforms }: PublishPanelProps) {
  const [state, setState] = useState<State>('idle')
  const [backup, setBackup] = useState<BackupResult | null>(null)

  const disabled = content === '' || platforms.length === 0

  async function handlePublish() {
    setState('loading')
    try {
      const res = await fetch('/api/v1/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content, platforms }),
      })
      if (!res.ok) {
        setState('error')
        return
      }
      const data = await res.json()
      setBackup(data)
      setState('success')
    } catch {
      setState('error')
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <button
        onClick={handlePublish}
        disabled={disabled || state === 'loading'}
        className="rounded-lg bg-blue-600 px-6 py-2 text-sm font-semibold text-white disabled:opacity-40"
      >
        發布
      </button>

      {(state === 'loading' || state === 'success') && (
        <p className="text-sm text-blue-600 font-medium">發布中...</p>
      )}

      {state === 'success' && backup && (
        <div className="rounded-lg border border-green-300 bg-green-50 p-3 text-sm text-green-800">
          <p className="font-semibold">備份完成</p>
          <p className="mt-1 font-mono text-xs">{backup.sha256}</p>
          <p className="text-xs text-green-600">{backup.proof_timestamp}</p>
        </div>
      )}

      {state === 'error' && (
        <p className="text-sm text-red-500 font-medium">發布失敗，請稍後再試。</p>
      )}
    </div>
  )
}
