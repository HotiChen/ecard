'use client'

import { useState } from 'react'

interface SentimentResult {
  comment: string
  label: string
}

const LABEL_STYLE: Record<string, string> = {
  positive: 'bg-green-100 text-green-700',
  neutral: 'bg-gray-100 text-gray-600',
  negative: 'bg-red-100 text-red-600',
}

export function AiAnalysisPage() {
  const [comment, setComment] = useState('')
  const [sentimentResults, setSentimentResults] = useState<SentimentResult[]>([])
  const [sentimentLoading, setSentimentLoading] = useState(false)

  const [suggestion, setSuggestion] = useState('')
  const [suggestLoading, setSuggestLoading] = useState(false)

  async function handleSentiment() {
    if (!comment.trim()) return
    setSentimentLoading(true)
    try {
      const res = await fetch('/api/v1/ai/sentiment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comments: [comment] }),
      })
      const data = await res.json()
      setSentimentResults(data)
    } finally {
      setSentimentLoading(false)
    }
  }

  async function handleSuggest() {
    setSuggestLoading(true)
    try {
      const res = await fetch('/api/v1/ai/suggest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          recent_contents: [],
          top_hashtags: [],
          best_platform: 'threads',
          avg_likes: 0,
        }),
      })
      const data = await res.json()
      setSuggestion(data.suggestion)
    } finally {
      setSuggestLoading(false)
    }
  }

  return (
    <div className="flex flex-col gap-8">
      <h1 className="text-xl font-bold">AI 分析</h1>

      {/* Sentiment section */}
      <section className="flex flex-col gap-3 rounded-xl border border-gray-100 p-5">
        <h2 className="font-semibold text-gray-800">留言情緒分析</h2>
        <div className="flex gap-2">
          <input
            type="text"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="輸入留言，按下按鈕分析情緒"
            className="flex-1 rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            onClick={handleSentiment}
            disabled={!comment.trim() || sentimentLoading}
            className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-40"
          >
            {sentimentLoading ? '分析中...' : '分析情緒'}
          </button>
        </div>
        {sentimentResults.length > 0 && (
          <ul className="flex flex-col gap-2">
            {sentimentResults.map((r, i) => (
              <li key={i} className="flex items-center gap-3 text-sm">
                <span className="flex-1 text-gray-700">{r.comment}</span>
                <span className={`rounded-full px-3 py-0.5 text-xs font-medium ${LABEL_STYLE[r.label] ?? 'bg-gray-100 text-gray-600'}`}>
                  {r.label}
                </span>
              </li>
            ))}
          </ul>
        )}
      </section>

      {/* Weekly report section */}
      <section className="flex flex-col gap-3 rounded-xl border border-gray-100 p-5">
        <h2 className="font-semibold text-gray-800">每週週報</h2>
        <p className="text-sm text-gray-500">
          連接真實數據後，AI 將自動生成本週摘要與下週建議。
        </p>
      </section>

      {/* Next post suggestion section */}
      <section className="flex flex-col gap-3 rounded-xl border border-gray-100 p-5">
        <h2 className="font-semibold text-gray-800">下一篇建議</h2>
        <button
          onClick={handleSuggest}
          disabled={suggestLoading}
          className="self-start rounded-lg bg-purple-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-40"
        >
          {suggestLoading ? '生成中...' : '取得建議'}
        </button>
        {suggestion && (
          <p className="rounded-lg bg-purple-50 p-3 text-sm text-purple-900 leading-relaxed">
            {suggestion}
          </p>
        )}
      </section>
    </div>
  )
}
