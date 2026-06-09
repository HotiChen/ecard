'use client'

import { useEffect, useState } from 'react'

interface Subscription {
  plan: string
  status: string
  trial_ends_at: string | null
  current_period_end: string | null
}

type LoadState = 'loading' | 'ready' | 'error'

const PLAN_LABELS: Record<string, string> = {
  free: 'Free',
  basic: 'Basic',
  pro: 'Pro',
}

export function SubscriptionPage() {
  const [sub, setSub] = useState<Subscription | null>(null)
  const [loadState, setLoadState] = useState<LoadState>('loading')

  useEffect(() => {
    fetch('/api/v1/subscription')
      .then((res) => res.json())
      .then((data) => {
        setSub(data)
        setLoadState('ready')
      })
      .catch(() => setLoadState('error'))
  }, [])

  async function handleCancel() {
    await fetch('/api/v1/subscription/cancel', { method: 'POST' })
    setSub((prev) => prev ? { ...prev, status: 'canceled' } : prev)
  }

  const isPaid = sub?.plan !== 'free' && sub?.status !== 'trialing'

  return (
    <div className="flex flex-col gap-6 p-6">
      <h1 className="text-xl font-bold">訂閱管理</h1>

      {loadState === 'loading' && (
        <p className="text-sm text-gray-500">載入中...</p>
      )}

      {loadState === 'ready' && sub && (
        <div className="flex flex-col gap-4">
          <div className="rounded-lg border border-gray-200 p-4 flex flex-col gap-2">
            <div className="flex items-center gap-3">
              <span className="text-lg font-semibold">
                {PLAN_LABELS[sub.plan] ?? sub.plan} 方案
              </span>
              {sub.status === 'active' && (
                <span className="rounded-full bg-green-100 px-3 py-0.5 text-xs font-medium text-green-700">
                  訂閱中
                </span>
              )}
              {sub.status === 'trialing' && (
                <span className="rounded-full bg-blue-100 px-3 py-0.5 text-xs font-medium text-blue-700">
                  試用中
                </span>
              )}
              {sub.status === 'canceled' && (
                <span className="rounded-full bg-gray-100 px-3 py-0.5 text-xs font-medium text-gray-600">
                  已取消
                </span>
              )}
              {sub.status === 'past_due' && (
                <span className="rounded-full bg-red-100 px-3 py-0.5 text-xs font-medium text-red-600">
                  付款逾期
                </span>
              )}
            </div>

            {sub.trial_ends_at && (
              <p className="text-sm text-gray-500">
                試用到期：{sub.trial_ends_at.slice(0, 10)}
              </p>
            )}
            {sub.current_period_end && (
              <p className="text-sm text-gray-500">
                下次續費：{sub.current_period_end.slice(0, 10)}
              </p>
            )}
          </div>

          <div className="flex gap-3">
            {!isPaid && (
              <button className="rounded-lg bg-blue-600 px-5 py-2 text-sm font-semibold text-white hover:bg-blue-700">
                升級方案
              </button>
            )}
            {isPaid && sub.status !== 'canceled' && (
              <button
                onClick={handleCancel}
                className="rounded-lg border border-red-300 px-5 py-2 text-sm font-medium text-red-600 hover:bg-red-50"
              >
                取消訂閱
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
