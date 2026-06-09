from pydantic import BaseModel
from app.models.enums import Platform


class MetricCreate(BaseModel):
    post_id: int
    platform: Platform
    likes: int = 0
    comments: int = 0
    replies: int = 0
    reposts: int = 0
    views: int = 0


class MetricRead(BaseModel):
    id: int
    post_id: int
    platform: str
    likes: int
    comments: int
    replies: int
    reposts: int
    views: int

    model_config = {"from_attributes": True}
