"""一篇發文及其在各平台的發布結果。"""

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import PostStatus


class Post(Base, TimestampMixin):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    content: Mapped[str] = mapped_column(Text)
    # 圖片的可公開存取 URL 清單（IG 發圖需要公開 URL）
    image_urls: Mapped[list] = mapped_column(JSONB, default=list)
    # 這篇文要發到哪些平台，例如 ["threads", "instagram"]
    target_platforms: Mapped[list] = mapped_column(JSONB, default=list)

    status: Mapped[PostStatus] = mapped_column(default=PostStatus.DRAFT, index=True)
    # 各平台回傳的 post id / 錯誤，例如 {"threads": {"id": "..."}, "x": {"error": "..."}}
    platform_results: Mapped[dict] = mapped_column(JSONB, default=dict)
    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True)

    user: Mapped["User"] = relationship(back_populates="posts")  # noqa: F821
    backups: Mapped[list["BackupRecord"]] = relationship(  # noqa: F821
        back_populates="post", cascade="all, delete-orphan"
    )
    metrics: Mapped[list["PostMetric"]] = relationship(  # noqa: F821
        back_populates="post", cascade="all, delete-orphan"
    )
