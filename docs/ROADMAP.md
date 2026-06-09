# 🗺️ PhotoFlow AI 開發藍圖（8 週）

每週一個可驗收的里程碑。打勾 = 已完成。

---

## Week 1 — Meta API 權限驗證（最重要，先卡關卡這裡）

> ⚠️ 這是整個專案最大的不確定性。Meta 的 Threads / Instagram 內容發布權限需要 App Review，
> 可能要送審、要 Business 驗證、要等待。**務必第一週就開始跑流程**，不要拖到後面。

- [ ] 在 developers.facebook.com 建立新 App（類型選 **Business**）
- [ ] 申請 **Threads API** 發文權限（`threads_basic`, `threads_content_publish`）
- [ ] 申請 **Instagram Graph API** 發文權限（`instagram_content_publish`，需連結 IG 商業帳號 + FB 粉專）
- [ ] 用測試帳號／測試 token 成功發出一則測試貼文
- [ ] 確認「發文成功瞬間」能觸發備份流程（先寫到本機，W2 再接 Drive）

**驗收標準**：能用 API 發出一則 Threads + IG 貼文，並在 log 看到回傳的 post id。

---

## Week 2 — 核心備份引擎

- [x] FastAPI 後端環境建置（✅ 骨架已建）
- [ ] Google Drive API 串接 OAuth 2.0
- [x] 建立發文內容資料庫模型（PostRecord + /api/v1/posts → SHA-256 存證回傳）
- [ ] 實作：發文 → 自動備份到 Google Drive
- [x] 實作：SHA-256 時間戳記存證檔自動生成
- [x] 單元測試：發文、備份、存證三個流程都跑得通

**驗收標準**：發一篇文後，Google Drive 出現備份檔 + `.sha256` 存證，且測試綠燈。

---

## Week 3 — 多平台發文介面

- [x] Next.js 前端專案建立（✅ 骨架已建）
- [ ] 登入／設定頁，連接 Threads / IG 帳號（OAuth）
- [x] 發文編輯區：文字 + 圖片上傳
- [x] 平台選擇（Threads / IG / X 多選）
- [x] 一鍵發布
- [x] 發布成功後顯示備份確認訊息

---

## Week 4 — 排程發文

- [x] 日期時間選擇元件
- [x] 排程任務存入資料庫（ScheduleEntry model + /api/v1/schedules CRUD）
- [ ] Celery + Redis 排程引擎建置
- [x] 排程發文自動執行測試
- [x] 排程任務管理頁

---

## Week 5 — 互動數據同步

- [x] 每日凌晨 2:00 Cron Job — 觸發邏輯（get_due_schedules + mark_schedule_executed）
- [ ] 讀取各貼文留言、回覆、按讚數
- [x] 互動數據存入資料庫（MetricRecord model + /api/v1/analytics/metrics CRUD）
- [x] 備份檔同步更新互動記錄（update_proof_with_metrics + MetricsSnapshot）
- [x] 貼文數據看板（基礎版）（✅ AnalyticsDashboard 元件含測試）

---

## Week 6 — Claude AI 分析引擎

- [ ] Claude API 串接（`claude-opus-4-8` / `claude-sonnet-4-6`）
- [x] 最佳發文時段分析
- [x] 內容類型分析
- [x] 留言情緒分析
- [x] 爆文特徵報告
- [x] 每週自動週報
- [x] 「下一篇建議」功能

---

## Week 7 — 金流與訂閱

- [ ] Stripe 帳號設定
- [x] 訂閱方案：/api/v1/subscription GET + cancel + _seed（SubscriptionRecord model）
- [x] 授權流程（plan → feature gating）
- [x] 免費試用 14 天
- [x] 付款成功／失敗 Webhook 處理
- [x] 訂閱管理頁

---

## Week 8 — Beta 測試與上線

- [ ] 找 5–10 位攝影師朋友免費測試
- [ ] 收集回饋、調整功能優先序
- [ ] 金流全流程測試
- [ ] 錯誤處理與通知系統測試
- [ ] Cloudflare 部署
- [ ] 自訂網域
- [ ] 正式對外公布

---

## 風險與建議（重要）

1. **Meta App Review 是頭號風險**：審核可能數週、可能被拒。建議 W1 就送審，期間用測試帳號開發其餘功能。
2. **IG 發圖限制多**：IG Graph API 只能發在「已連結 FB 粉專的商業／創作者帳號」，且圖片需公開 URL。規劃時要先把圖上傳到可公開存取的儲存（如 R2/S3）。
3. **法律存證效力**：SHA-256 + 時間戳記能證明「檔案在某時間點存在且未被竄改」，但若要對外宣稱「法律存證」，時間戳記來源最好用可信第三方（如 RFC 3161 TSA），而非僅本機時間。
4. **成本控管**：X API v2 發文門檻與費用近年變動大，W1 一併確認 X 的方案與額度。
