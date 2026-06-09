"""Google Drive 備份檔與 SHA-256 存證記錄。"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class BackupRecord(Base, TimestampMixin):
    __tablename__ = "backup_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), index=True)

    drive_file_id: Mapped[str] = mapped_column(String(128))
    drive_file_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # 備份內容的 SHA-256（hex），作為未竄改的指紋
    sha256: Mapped[str] = mapped_column(String(64), index=True)
    # 產生存證當下的時間戳（ISO8601）
    proof_timestamp: Mapped[str] = mapped_column(String(64))

    post: Mapped["Post"] = relationship(back_populates="backups")  # noqa: F821
