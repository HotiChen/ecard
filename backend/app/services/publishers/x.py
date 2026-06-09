"""X (Twitter) 發文器（X API v2）。

TODO(W3)：串接 POST /2/tweets，圖片需先走 media upload 取得 media_id。
目前為骨架。
"""

import httpx

from app.models.enums import Platform
from app.schemas.post import PublishResult
from app.services.publishers.base import BasePublisher

X_API_BASE = "https://api.twitter.com/2"


class XPublisher(BasePublisher):
    platform = Platform.X

    async def publish(
        self,
        *,
        access_token: str,
        content: str,
        image_urls: list[str],
    ) -> PublishResult:
        try:
            async with httpx.AsyncClient(base_url=X_API_BASE, timeout=30) as _client:
                raise NotImplementedError("X publish 尚未串接（W3）")
        except NotImplementedError as exc:
            return PublishResult(platform=self.platform, success=False, error=str(exc))
        except httpx.HTTPError as exc:  # pragma: no cover - 骨架
            return PublishResult(platform=self.platform, success=False, error=str(exc))
