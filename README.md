# 📷 PhotoFlow AI

攝影師的多平台發文、自動備份與 AI 內容分析 SaaS。

一鍵把貼文發到 **Threads / Instagram / X**，發文成功瞬間自動備份到 **Google Drive** 並產生 **SHA-256 時間戳記存證**，再用 **Claude AI** 分析互動數據、找出最佳發文時段與爆文特徵。

> 本 repo 目前為**專案骨架（scaffold）**階段。各模組為可開發的起始結構，尚未串接真實 API 金鑰。詳細開發藍圖見 [`docs/ROADMAP.md`](docs/ROADMAP.md)，架構決策見 [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)。

---

## 技術棧

| 層級 | 技術 |
|------|------|
| 前端 | Next.js (App Router) + TypeScript + Tailwind CSS |
| 後端 | FastAPI + SQLAlchemy + Pydantic |
| 資料庫 | PostgreSQL（正式環境用 Supabase）|
| 發文 API | Meta Graph API（Threads / Instagram）+ X API v2 |
| 備份 | Google Drive API + SHA-256 存證 |
| AI 分析 | Claude API（`claude-opus-4-8` / `claude-sonnet-4-6`）|
| 排程 | Celery + Redis |
| 金流 | Stripe（訂閱制）|
| 部署 | Cloudflare Pages（前端）+ Workers／容器（後端）|

預估月維運成本：約 **NT$4,300**

---

## 專案結構

```
.
├── backend/            FastAPI 後端（API、發文、備份、排程、AI 分析）
│   └── app/
│       ├── api/        REST 路由（v1）
│       ├── core/       設定、共用工具
│       ├── db/         資料庫連線與 Base
│       ├── models/     SQLAlchemy ORM 模型
│       ├── schemas/    Pydantic schema
│       └── services/   發文器、備份、AI 分析等業務邏輯
├── frontend/           Next.js 前端（登入、發文編輯、看板）
├── docs/               架構與開發藍圖文件
└── docker-compose.yml  本機 PostgreSQL + Redis
```

---

## 快速開始（本機開發）

### 1. 起資料庫與 Redis

```bash
docker compose up -d
```

### 2. 後端

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # 填入你的金鑰
uvicorn app.main:app --reload
```

後端啟動後：API 文件在 http://localhost:8000/docs

### 3. 前端

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

前端：http://localhost:3000

---

## 開發進度

完整 8 週藍圖見 [`docs/ROADMAP.md`](docs/ROADMAP.md)。

- [x] **W0** — 專案骨架、文件、本機開發環境
- [ ] **W1** — Meta API 權限驗證（Threads / IG 發文）
- [ ] **W2** — 核心備份引擎（Google Drive + SHA-256）
- [ ] **W3** — 多平台發文介面
- [ ] **W4** — 排程發文（Celery + Redis）
- [ ] **W5** — 互動數據同步
- [ ] **W6** — Claude AI 分析引擎
- [ ] **W7** — 金流與訂閱（Stripe）
- [ ] **W8** — Beta 測試與上線
