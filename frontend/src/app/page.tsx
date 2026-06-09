'use client'

import { useState } from 'react'
import { NavBar, Tab } from '@/components/NavBar'
import { AiAnalysisPage } from '@/components/AiAnalysisPage'
import { AnalyticsDashboard } from '@/components/AnalyticsDashboard'
import { ComposePage } from '@/components/ComposePage'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { SchedulePage } from '@/components/SchedulePage'
import { SubscriptionPage } from '@/components/SubscriptionPage'

export default function Home() {
  const [tab, setTab] = useState<Tab>('compose')

  return (
    <main className="mx-auto max-w-2xl px-6 py-12">
      <h1 className="text-3xl font-bold tracking-tight mb-1">📷 PhotoFlow AI</h1>
      <p className="text-sm text-neutral-500 mb-6">
        多平台發文、自動備份與 AI 內容分析平台
      </p>
      <NavBar active={tab} onNavigate={setTab} />
      <ErrorBoundary>
        {tab === 'compose' && <ComposePage />}
        {tab === 'schedule' && <SchedulePage />}
        {tab === 'analytics' && <AnalyticsDashboard />}
        {tab === 'ai' && <AiAnalysisPage />}
        {tab === 'subscription' && <SubscriptionPage />}
      </ErrorBoundary>
    </main>
  )
}
