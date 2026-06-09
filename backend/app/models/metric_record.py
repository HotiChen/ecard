"""Standalone metric record — no FK constraints, SQLite-compatible."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class MetricRecord(Base, TimestampMixin):
    __tablename__ = "metric_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(index=True)
    platform: Mapped[str] = mapped_column(String(32), index=True)
    likes: Mapped[int] = mapped_column(default=0)
    comments: Mapped[int] = mapped_column(default=0)
    replies: Mapped[int] = mapped_column(default=0)
    reposts: Mapped[int] = mapped_column(default=0)
    views: Mapped[int] = mapped_column(default=0)
