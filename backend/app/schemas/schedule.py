from datetime import datetime

from pydantic import BaseModel, Field


class ScheduleCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)
    platforms: list[str] = Field(..., min_length=1)
    scheduled_at: datetime


class ScheduleRead(BaseModel):
    id: int
    content: str
    platforms: list[str]
    scheduled_at: datetime
    is_canceled: bool
    executed_at: datetime | None

    model_config = {"from_attributes": True}
