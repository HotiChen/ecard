'use client'

import { useEffect, useState } from 'react'

interface MetricSnapshot {
  post_id: number
  platform: string
  likes: number
  comments: number
  replies: number
  reposts: number
  views: number
}

interface Summary {
  totalLikes: number
  totalComments: number
  totalViews: number
  totalReposts: number
}

type LoadState = 'loading' | 'ready' | 'error'

function sumMetrics(metrics: MetricSnapshot[]): Summary {
  return metrics.reduce(
    (acc, m) => ({
      totalLikes: acc.totalLikes + m.likes,
      totalComments: acc.totalComments + m.comments,
      totalViews: acc.totalViews + m.views,
      totalReposts: acc.totalReposts + m.reposts,
    }),
    { totalLikes: 0, totalComments: 0, totalViews: 0, totalReposts: 0 }
  )
}

export function AnalyticsDashboard() {
  const [metrics, setMetrics] = useState<MetricSnapshot[]>([])
  const [loadState, setLoadState] = useState<LoadState>('loading')

  useEffect(() => {
    fetch('/api/v1/analytics/metrics')
      .then((res) => res.json())
      .then((data) => {
        setMetrics(data)
        setLoadState('ready')
      })
      .catch(() => setLoadState('error'))
  }, [])

  const summary = sumMetrics(metrics)

  return (
    <div className="flex flex-col gap-6 p-6">
      <h1 className="text-xl font-bold">數據看板</h1>

      {loadState === 'loading' && (
        <p className="text-sm text-gray-500">載入中...</p>
      )}

      {loadState === 'ready' && metrics.length === 0 && (
        <p className="text-sm text-gray-500">尚無數據</p>
      )}

      {loadState === 'ready' && metrics.length > 0 && (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
          {[
            { label: '按讚數', value: summary.totalLikes },
            { label: '留言數', value: summary.totalComments },
            { label: '轉發數', value: summary.totalReposts },
            { label: '觀看數', value: summary.totalViews },
          ].map(({ label, value }) => (
            <div
              key={label}
              className="rounded-lg border border-gray-200 bg-white p-4 text-center shadow-sm"
            >
              <p className="text-2xl font-bold text-blue-600">{value}</p>
              <p className="text-xs text-gray-500 mt-1">{label}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
