"""彙整 v1 所有路由。"""

from fastapi import APIRouter

from app.api.v1.endpoints import health, posts, schedules

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(schedules.router, prefix="/schedules", tags=["schedules"])
