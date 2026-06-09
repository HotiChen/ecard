import { ComposePage } from '@/components/ComposePage'

export default function Home() {
  return (
    <main className="mx-auto max-w-2xl px-6 py-12">
      <h1 className="text-3xl font-bold tracking-tight mb-2">📷 PhotoFlow AI</h1>
      <p className="text-sm text-neutral-500 mb-10">
        多平台發文、自動備份與 AI 內容分析平台
      </p>
      <ComposePage />
    </main>
  )
}
