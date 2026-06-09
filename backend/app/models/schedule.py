"""排程發文任務。"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class ScheduledPost(Base, TimestampMixin):
    __tablename__ = "scheduled_posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), index=True)

    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    # Celery task id，方便取消／追蹤
    celery_task_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    is_canceled: Mapped[bool] = mapped_column(default=False)
    executed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
