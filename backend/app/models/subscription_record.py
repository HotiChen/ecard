"""Standalone subscription record — SQLite-compatible, no FK constraints."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class SubscriptionRecord(Base, TimestampMixin):
    __tablename__ = "subscription_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    plan: Mapped[str] = mapped_column(String(32), default="free")
    status: Mapped[str] = mapped_column(String(32), default="trialing")
    trial_ends_at: Mapped[str | None] = mapped_column(String(64), nullable=True)
    current_period_end: Mapped[str | None] = mapped_column(String(64), nullable=True)
