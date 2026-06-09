export default function Home() {
  const features = [
    { title: "多平台發文", desc: "一鍵發到 Threads / Instagram / X" },
    { title: "自動備份", desc: "發文瞬間備份到 Google Drive + SHA-256 存證" },
    { title: "排程發文", desc: "選好時間，到點自動發布" },
    { title: "AI 分析", desc: "Claude 分析最佳時段與爆文特徵" },
  ];

  return (
    <main className="mx-auto max-w-3xl px-6 py-20">
      <h1 className="text-4xl font-bold tracking-tight">📷 PhotoFlow AI</h1>
      <p className="mt-4 text-lg text-neutral-600">
        攝影師的多平台發文、自動備份與 AI 內容分析平台。
      </p>

      <div className="mt-12 grid gap-4 sm:grid-cols-2">
        {features.map((f) => (
          <div
            key={f.title}
            className="rounded-xl border border-neutral-200 bg-white p-5 shadow-sm"
          >
            <h2 className="font-semibold">{f.title}</h2>
            <p className="mt-1 text-sm text-neutral-500">{f.desc}</p>
          </div>
        ))}
      </div>

      <p className="mt-12 text-sm text-neutral-400">
        專案骨架階段 · 開發藍圖見 docs/ROADMAP.md
      </p>
    </main>
  );
}
