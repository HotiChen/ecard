"""發文相關的 Pydantic schema（API 進出型別）。"""

from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import Platform, PostStatus


class PostCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)
    image_urls: list[str] = Field(default_factory=list)
    target_platforms: list[Platform] = Field(..., min_length=1)
    # 有值代表排程發文；無值代表立即發布
    scheduled_at: datetime | None = None


class PostRead(BaseModel):
    id: int
    content: str
    image_urls: list[str]
    target_platforms: list[Platform]
    status: PostStatus
    platform_results: dict
    created_at: datetime

    model_config = {"from_attributes": True}


class PublishResult(BaseModel):
    """單一平台的發布結果。"""

    platform: Platform
    success: bool
    external_post_id: str | None = None
    error: str | None = None
