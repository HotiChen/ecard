"""資料庫連線與 FastAPI 相依注入。"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    """FastAPI 相依：每個 request 一個 session，結束時關閉。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
