"""發文服務單元測試（W2）。

測試 publish_post 的多平台 dispatch 邏輯，外部 HTTP 呼叫全用 mock。
不依賴真實 API 金鑰或網路連線。
"""

import pytest
from unittest.mock import AsyncMock

from app.models.enums import Platform
from app.schemas.post import PublishResult
from app.services.publish import publish_post


def _ok(platform: Platform, post_id: str = "abc") -> PublishResult:
    return PublishResult(platform=platform, success=True, external_post_id=post_id)


def _fail(platform: Platform, error: str = "err") -> PublishResult:
    return PublishResult(platform=platform, success=False, error=error)


@pytest.mark.asyncio
async def test_publish_post_returns_result_for_each_platform():
    mock = AsyncMock()
    mock.publish.return_value = _ok(Platform.THREADS, "t123")

    results = await publish_post(
        content="攝影師的一天",
        platforms=[Platform.THREADS],
        access_tokens={Platform.THREADS: "token"},
        publishers={Platform.THREADS: mock},
    )

    assert Platform.THREADS in results
    assert results[Platform.THREADS].success is True
    assert results[Platform.THREADS].external_post_id == "t123"


@pytest.mark.asyncio
async def test_publish_post_passes_correct_args_to_publisher():
    mock = AsyncMock()
    mock.publish.return_value = _ok(Platform.THREADS)

    await publish_post(
        content="測試內容",
        platforms=[Platform.THREADS],
        access_tokens={Platform.THREADS: "my-token"},
        publishers={Platform.THREADS: mock},
    )

    mock.publish.assert_called_once_with(
        access_token="my-token",
        content="測試內容",
        image_urls=[],
    )


@pytest.mark.asyncio
async def test_publish_post_handles_multiple_platforms():
    mock_t = AsyncMock()
    mock_t.publish.return_value = _ok(Platform.THREADS)
    mock_ig = AsyncMock()
    mock_ig.publish.return_value = _fail(Platform.INSTAGRAM, "no images")

    results = await publish_post(
        content="多平台發文",
        platforms=[Platform.THREADS, Platform.INSTAGRAM],
        access_tokens={},
        publishers={Platform.THREADS: mock_t, Platform.INSTAGRAM: mock_ig},
    )

    assert len(results) == 2
    assert results[Platform.THREADS].success is True
    assert results[Platform.INSTAGRAM].success is False
    assert results[Platform.INSTAGRAM].error == "no images"


@pytest.mark.asyncio
async def test_publish_post_returns_error_for_missing_publisher():
    results = await publish_post(
        content="test",
        platforms=[Platform.X],
        access_tokens={},
        publishers={},
    )

    assert Platform.X in results
    assert results[Platform.X].success is False
    assert results[Platform.X].error is not None


@pytest.mark.asyncio
async def test_publish_post_passes_image_urls_to_publisher():
    mock = AsyncMock()
    mock.publish.return_value = _ok(Platform.INSTAGRAM)

    await publish_post(
        content="照片日記",
        platforms=[Platform.INSTAGRAM],
        access_tokens={Platform.INSTAGRAM: "ig-token"},
        image_urls=["https://example.com/photo.jpg"],
        publishers={Platform.INSTAGRAM: mock},
    )

    mock.publish.assert_called_once_with(
        access_token="ig-token",
        content="照片日記",
        image_urls=["https://example.com/photo.jpg"],
    )
