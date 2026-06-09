"""發文相關端點。

目前為骨架：示範「建立發文 → (W1/W3) 發布 → (W2) 備份」的流程輪廓，
實際發布與資料庫寫入會在後續週次補上。
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.post import PostCreate, PostRead

router = APIRouter()


@router.post("", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, db: Session = Depends(get_db)) -> PostRead:
    """建立一篇發文。

    - 有 `scheduled_at`：存成排程任務（W4 由 Celery 執行）。
    - 沒有：之後會立即觸發發布 + 備份流程（W1–W3）。

    TODO：實作 DB 寫入與發布觸發；目前回傳示意資料。
    """
    raise NotImplementedError("create_post 尚未實作（W2/W3 補上 DB 寫入與發布）")


@router.get("", response_model=list[PostRead])
def list_posts(db: Session = Depends(get_db)) -> list[PostRead]:
    """列出目前使用者的發文。TODO：接 DB 查詢與身分驗證。"""
    return []
