'use client'

import { useEffect, useState } from 'react'

interface ScheduledPost {
  id: number
  content: string
  platforms: string[]
  scheduled_at: string
  is_canceled: boolean
  executed_at: string | null
}

type LoadState = 'loading' | 'ready' | 'error'

export function SchedulePage() {
  const [posts, setPosts] = useState<ScheduledPost[]>([])
  const [loadState, setLoadState] = useState<LoadState>('loading')

  useEffect(() => {
    fetch('/api/v1/schedules')
      .then((res) => res.json())
      .then((data) => {
        setPosts(data)
        setLoadState('ready')
      })
      .catch(() => setLoadState('error'))
  }, [])

  async function cancelPost(id: number) {
    await fetch(`/api/v1/schedules/${id}/cancel`, { method: 'POST' })
    setPosts((prev) =>
      prev.map((p) => (p.id === id ? { ...p, is_canceled: true } : p))
    )
  }

  return (
    <div className="flex flex-col gap-6 p-6">
      <h1 className="text-xl font-bold">排程管理</h1>

      {loadState === 'loading' && (
        <p className="text-sm text-gray-500">載入中...</p>
      )}

      {loadState === 'ready' && posts.length === 0 && (
        <p className="text-sm text-gray-500">目前沒有排程貼文</p>
      )}

      {loadState === 'ready' && posts.length > 0 && (
        <ul className="flex flex-col gap-3">
          {posts.map((post) => (
            <li
              key={post.id}
              className="rounded-lg border border-gray-200 p-4 flex flex-col gap-2"
            >
              <p className="text-sm font-medium line-clamp-2">{post.content}</p>
              <div className="flex items-center gap-2 text-xs text-gray-500">
                <span>{new Date(post.scheduled_at).toLocaleString('zh-TW')}</span>
                <span>{post.platforms.join(', ')}</span>
                {post.is_canceled && (
                  <span className="rounded bg-red-100 px-2 py-0.5 text-red-600 font-medium">
                    已取消
                  </span>
                )}
                {post.executed_at && (
                  <span className="rounded bg-green-100 px-2 py-0.5 text-green-700 font-medium">
                    已發布
                  </span>
                )}
              </div>
              {!post.is_canceled && !post.executed_at && (
                <button
                  onClick={() => cancelPost(post.id)}
                  className="self-start rounded border border-red-300 px-3 py-1 text-xs text-red-600 hover:bg-red-50"
                >
                  取消
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
