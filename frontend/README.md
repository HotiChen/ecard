# PhotoFlow AI — 前端 (Next.js)

## 開發

```bash
npm install
cp .env.example .env.local
npm run dev
```

開啟 http://localhost:3000

## 技術

- Next.js 15（App Router）+ React 19
- TypeScript
- Tailwind CSS

## 目錄

```
src/app/
├── layout.tsx     全站版型
├── page.tsx       首頁（landing）
└── globals.css    Tailwind 進入點
```

後續頁面（依 ROADMAP）：
- `/login`、`/settings`（連接 Threads/IG 帳號）— W3
- `/compose`（發文編輯 + 平台多選 + 圖片上傳）— W3
- `/schedule`（排程管理）— W4
- `/dashboard`（數據看板）— W5
