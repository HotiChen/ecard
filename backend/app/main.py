"""PhotoFlow AI 後端進入點。"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title="PhotoFlow AI API",
    version="0.1.0",
    description="攝影師多平台發文、自動備份與 AI 分析。",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root() -> dict:
    return {"app": "PhotoFlow AI", "docs": "/docs", "health": "/api/v1/health"}
