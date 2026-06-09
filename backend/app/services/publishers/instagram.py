"""Instagram 發文器（Instagram Graph API）。

注意：IG 發圖需要「已連結 FB 粉專的商業／創作者帳號」，且圖片必須是可公開存取的 URL。
流程同樣是兩步：建立 media container -> publish。

TODO(W1)：串接真實 API；目前為骨架。
"""

import httpx

from app.models.enums import Platform
from app.schemas.post import PublishResult
from app.services.publishers.base import BasePublisher

IG_API_BASE = "https://graph.facebook.com/v21.0"


class InstagramPublisher(BasePublisher):
    platform = Platform.INSTAGRAM

    async def publish(
        self,
        *,
        access_token: str,
        content: str,
        image_urls: list[str],
    ) -> PublishResult:
        if not image_urls:
            return PublishResult(
                platform=self.platform,
                success=False,
                error="Instagram 發文需要至少一張圖片的公開 URL",
            )
        # TODO(W1): create media -> publish
        try:
            async with httpx.AsyncClient(base_url=IG_API_BASE, timeout=30) as _client:
                raise NotImplementedError("Instagram publish 尚未串接（W1）")
        except NotImplementedError as exc:
            return PublishResult(platform=self.platform, success=False, error=str(exc))
        except httpx.HTTPError as exc:  # pragma: no cover - 骨架
            return PublishResult(platform=self.platform, success=False, error=str(exc))
