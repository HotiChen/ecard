"""多平台發文 dispatcher。

publish_post 是「發文」流程的核心入口：
  - 接受平台清單與各平台的 access token
  - 將工作分派給對應的 BasePublisher 實作
  - 回傳 {Platform: PublishResult} 讓呼叫端決定如何處理成功/失敗

publishers 參數預設為 None（使用真實發文器），測試時可注入 mock。
"""

from app.models.enums import Platform
from app.schemas.post import PublishResult
from app.services.publishers.base import BasePublisher


async def publish_post(
    content: str,
    platforms: list[Platform],
    access_tokens: dict[Platform, str],
    image_urls: list[str] | None = None,
    publishers: dict[Platform, BasePublisher] | None = None,
) -> dict[Platform, PublishResult]:
    """發布貼文到多個平台，回傳每個平台的 PublishResult。"""
    if publishers is None:
        publishers = _default_publishers()

    results: dict[Platform, PublishResult] = {}
    for platform in platforms:
        publisher = publishers.get(platform)
        if publisher is None:
            results[platform] = PublishResult(
                platform=platform,
                success=False,
                error=f"不支援或尚未設定的平台：{platform.value}",
            )
            continue
        results[platform] = await publisher.publish(
            access_token=access_tokens.get(platform, ""),
            content=content,
            image_urls=image_urls or [],
        )
    return results


def _default_publishers() -> dict[Platform, BasePublisher]:
    from app.services.publishers.instagram import InstagramPublisher
    from app.services.publishers.threads import ThreadsPublisher
    from app.services.publishers.x import XPublisher

    return {
        Platform.THREADS: ThreadsPublisher(),
        Platform.INSTAGRAM: InstagramPublisher(),
        Platform.X: XPublisher(),
    }
