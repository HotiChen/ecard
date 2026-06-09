"""每日同步的貼文互動數據。"""

from datetime import date

from sqlalchemy import Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import Platform


class PostMetric(Base, TimestampMixin):
    __tablename__ = "post_metrics"
    # 同一篇文、同一平台、同一天只留一筆（每日同步更新）
    __table_args__ = (
        UniqueConstraint("post_id", "platform", "metric_date", name="uq_metric_daily"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), index=True)
    platform: Mapped[Platform] = mapped_column(index=True)
    metric_date: Mapped[date] = mapped_column(Date, index=True)

    likes: Mapped[int] = mapped_column(default=0)
    comments: Mapped[int] = mapped_column(default=0)
    replies: Mapped[int] = mapped_column(default=0)
    reposts: Mapped[int] = mapped_column(default=0)
    views: Mapped[int] = mapped_column(default=0)

    post: Mapped["Post"] = relationship(back_populates="metrics")  # noqa: F821
