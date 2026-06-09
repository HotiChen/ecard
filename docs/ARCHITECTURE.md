# 🏛️ 架構說明

## 系統概觀

```
                    ┌─────────────────────────────┐
                    │   前端 Next.js (Cloudflare)  │
                    │  登入 / 發文編輯 / 看板 / 訂閱 │
                    └──────────────┬──────────────┘
                                   │ HTTPS / REST
                    ┌──────────────▼──────────────┐
                    │      後端 FastAPI            │
                    │  ┌────────────────────────┐  │
                    │  │ api/        REST 路由   │  │
                    │  │ services/   業務邏輯    │  │
                    │  │  ├ publishers (Threads/IG/X)
                    │  │  ├ backup (Drive+SHA256)
                    │  │  └ analysis (Claude)   │  │
                    │  └────────────────────────┘  │
                    └───┬───────────┬───────────┬──┘
                        │           │           │
              ┌─────────▼──┐  ┌─────▼─────┐  ┌──▼───────────┐
              │ PostgreSQL │  │  Redis    │  │ 外部 API     │
              │ (Supabase) │  │ (Celery)  │  │ Meta/X/Drive │
              └────────────┘  └─────┬─────┘  │ Claude/Stripe│
                                    │        └──────────────┘
                              ┌─────▼─────┐
                              │  Celery   │  排程發文 / 每日數據同步
                              │  workers  │
                              └───────────┘
```

## 後端分層

- **`api/`** — 只負責 HTTP（驗證輸入、呼叫 service、回傳）。不放業務邏輯。
- **`services/`** — 核心業務邏輯，可被 API 與 Celery task 共用。
  - `publishers/` — 各平台發文器，共用 `BasePublisher` 介面，方便擴充平台。
  - `backup.py` — 發文成功後備份到 Google Drive 並產生 SHA-256 存證。
  - `analysis.py`（W6）— 呼叫 Claude API 做數據分析。
- **`models/`** — SQLAlchemy ORM。
- **`schemas/`** — Pydantic，API 進出資料的型別。
- **`core/config.py`** — 用 pydantic-settings 從環境變數讀設定，全專案唯一設定來源。

## 資料模型（初版）

| 模型 | 用途 |
|------|------|
| `User` | 使用者帳號、訂閱方案 |
| `SocialAccount` | 使用者連結的 Threads/IG/X 帳號與 token |
| `Post` | 一篇發文內容與各平台發布結果 |
| `BackupRecord` | Google Drive 備份檔與 SHA-256 存證 |
| `ScheduledPost` | 排程發文任務 |
| `PostMetric` | 每日同步的互動數據（讚/留言/回覆）|
| `Subscription` | Stripe 訂閱狀態 |

## 關鍵設計決策

1. **Publisher 用策略模式**：每個平台一個 class、實作相同介面，新增平台不動既有程式。
2. **發文與備份解耦**：發文成功 → 發事件 → 備份。備份失敗不該讓發文「看起來失敗」，但要記錄並可重試。
3. **Celery 同時負責排程發文與每日 Cron**：避免再引入第二套排程系統。
4. **設定全走環境變數**：金鑰不進 repo，`.env.example` 只列鍵名不列值。
5. **AI 分析走 Claude**：預設 `claude-opus-4-8`（深度週報）與 `claude-sonnet-4-6`（即時、量大的分析）混用以平衡成本。
