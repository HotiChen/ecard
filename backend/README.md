# PhotoFlow AI — 後端 (FastAPI)

## 開發

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # 填入金鑰
uvicorn app.main:app --reload
```

- API 文件：http://localhost:8000/docs
- 健康檢查：http://localhost:8000/api/v1/health

## Celery（W4 起）

```bash
# worker
celery -A app.worker.celery_app worker --loglevel=info
# 排程（每日數據同步等）
celery -A app.worker.celery_app beat --loglevel=info
```

## 測試

```bash
pytest
```

## 目錄

```
app/
├── main.py            FastAPI 進入點
├── core/config.py     設定（讀環境變數）
├── db/                資料庫連線、Base
├── models/            SQLAlchemy 模型
├── schemas/           Pydantic schema
├── api/v1/            REST 路由
└── services/          業務邏輯（發文器、備份、AI）
```
