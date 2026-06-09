"""健康檢查。"""

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()

APP_VERSION = "0.1.0"


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "env": settings.app_env, "version": APP_VERSION}
