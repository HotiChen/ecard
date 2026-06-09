"""健康檢查。"""

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "env": settings.app_env}
