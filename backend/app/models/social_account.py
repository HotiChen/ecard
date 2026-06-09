"""使用者連結的社群平台帳號與存取權杖。

注意：access_token 等敏感欄位正式上線前應加密儲存（如 KMS / Fernet），
此處骨架先以純文字欄位佔位。
"""

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import Platform


class SocialAccount(Base, TimestampMixin):
    __tablename__ = "social_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    platform: Mapped[Platform] = mapped_column(index=True)

    # 平台上的帳號識別
    external_account_id: Mapped[str] = mapped_column(String(128))
    username: Mapped[str | None] = mapped_column(String(120), nullable=True)

    # OAuth tokens（TODO: 上線前加密）
    access_token: Mapped[str] = mapped_column(Text)
    refresh_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    token_expires_at: Mapped[str | None] = mapped_column(String(64), nullable=True)

    user: Mapped["User"] = relationship(back_populates="social_accounts")  # noqa: F821
