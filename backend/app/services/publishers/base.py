"""發文器共用介面。"""

from abc import ABC, abstractmethod

from app.models.enums import Platform
from app.schemas.post import PublishResult


class BasePublisher(ABC):
    """所有平台發文器要實作的介面。"""

    platform: Platform

    @abstractmethod
    async def publish(
        self,
        *,
        access_token: str,
        content: str,
        image_urls: list[str],
    ) -> PublishResult:
        """把貼文發到該平台，回傳結果（含 external post id 或錯誤）。"""
        raise NotImplementedError
