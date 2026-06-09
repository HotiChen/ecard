"""Threads 發文器（Meta Graph API）。

Threads 發文是兩步：
  1) 建立 media container（POST /{user-id}/threads）
  2) 發布 container（POST /{user-id}/threads_publish）

TODO(W1)：填入真實的 user-id 取得流程與錯誤處理；目前為骨架。
"""

import httpx

from app.models.enums import Platform
from app.schemas.post import PublishResult
from app.services.publishers.base import BasePublisher

THREADS_API_BASE = "https://graph.threads.net/v1.0"


class ThreadsPublisher(BasePublisher):
    platform = Platform.THREADS

    async def publish(
        self,
        *,
        access_token: str,
        content: str,
        image_urls: list[str],
    ) -> PublishResult:
        # TODO(W1): 實作真正的兩步發布流程。先以骨架結構表達意圖。
        try:
            async with httpx.AsyncClient(base_url=THREADS_API_BASE, timeout=30) as _client:
                # 1) create container -> 2) publish
                # creation = await _client.post("/me/threads", params={...})
                # publish  = await _client.post("/me/threads_publish", params={...})
                raise NotImplementedError("Threads publish 尚未串接（W1）")
        except NotImplementedError as exc:
            return PublishResult(platform=self.platform, success=False, error=str(exc))
        except httpx.HTTPError as exc:  # pragma: no cover - 骨架
            return PublishResult(platform=self.platform, success=False, error=str(exc))
