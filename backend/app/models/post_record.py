"""Standalone post record — SQLite-compatible, no FK constraints."""
from sqlalchemy import JSON, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class PostRecord(Base, TimestampMixin):
    __tablename__ = "post_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    platforms: Mapped[list] = mapped_column(JSON, default=list)
    sha256: Mapped[str] = mapped_column(Text)
    proof_timestamp: Mapped[str] = mapped_column(Text)
