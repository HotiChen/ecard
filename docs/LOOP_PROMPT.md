# 🔁 TDD 開發 Loop 提示

在**新對話視窗**(建議用 Sonnet 4.6)直接複製下面整段貼上,即可讓 Claude 用
TDD 方式、依 `docs/ROADMAP.md` 的進度自動往下開發。

> 開始前先確認:已切到分支 `claude/project-review-corrections-b8lkqt`,
> 並已執行 `pip install -r backend/requirements.txt`。

---

## 直接貼這段

```
/loop 30m 依 TDD 開發 PhotoFlow AI,一輪只做一個子任務:
(1) 讀 docs/ROADMAP.md,挑出下一個還沒打勾、且不需要外部 API 金鑰或
人工申請(Meta 審核、Stripe 帳號、找人測試等)就能寫的最小子任務,只挑一個。
(2) 嚴格 TDD:先在 backend/tests 寫一個會失敗的測試,跑 pytest 確認紅燈;
再寫最少的程式讓它綠燈,必要時重構,全程保持其他測試也綠。優先寫不需要
真實資料庫/網路的純邏輯測試,外部服務一律用 mock。
(3) 全綠後把該任務在 ROADMAP 打勾,用清楚訊息 git commit,並 push 到
claude/project-review-corrections-b8lkqt 分支。
(4) 一次只完成一個子任務就停;若可寫的任務都完成、或卡在需要金鑰/人工的
步驟,明確說明卡在哪,不要硬寫假資料。結束前絕不留紅燈或無法編譯的程式碼。
```

---

## 設計重點

| 設計 | 原因 |
|------|------|
| 讀 ROADMAP 挑下一個 | `/loop` 每輪跑同一段字,必須讓它自己找進度,否則重做同一件事 |
| 只寫不需金鑰/人工的任務 | 申請 Meta 權限、開 Stripe、找人測試等 Agent 做不了,要自動跳過 |
| mock 外部服務、優先純邏輯測試 | 否則測試會因沒有 Postgres/網路而紅燈,卡死整個 loop |
| 一輪一個子任務 + 結束不留紅燈 | 每輪都是乾淨可提交狀態,中斷也安全 |
| `30m` 間隔 | 一個 TDD 任務約 10–20 分鐘,間隔太短會在前一輪沒跑完就疊上來 |

## 提醒

- 新視窗記得切到同一分支,並先安裝後端套件,否則第一輪會卡在缺套件。
- Sonnet 4.6 跑 TDD 很合適;若某輪遇到較複雜的架構決策,可手動切回 Opus 處理完再續跑。
- 停止 loop:在該視窗輸入 `/loop` 的停止指令或直接中斷即可。
