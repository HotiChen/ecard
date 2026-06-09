"""Standalone schedule entry — no FK constraints, SQLite-compatible."""
from datetime import datetime

from sqlalchemy import JSON, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class ScheduleEntry(Base, TimestampMixin):
    __tablename__ = "schedule_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    platforms: Mapped[list] = mapped_column(JSON, default=list)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_canceled: Mapped[bool] = mapped_column(default=False)
    executed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
