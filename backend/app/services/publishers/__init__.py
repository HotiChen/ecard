"""各平台發文器。

用策略模式：每個平台一個 publisher，實作相同的 BasePublisher 介面。
新增平台時只要新增一個 class、註冊到 PUBLISHERS，不必動既有程式。
"""

from app.models.enums import Platform
from app.services.publishers.base import BasePublisher
from app.services.publishers.instagram import InstagramPublisher
from app.services.publishers.threads import ThreadsPublisher
from app.services.publishers.x import XPublisher

PUBLISHERS: dict[Platform, type[BasePublisher]] = {
    Platform.THREADS: ThreadsPublisher,
    Platform.INSTAGRAM: InstagramPublisher,
    Platform.X: XPublisher,
}


def get_publisher(platform: Platform) -> BasePublisher:
    """依平台取得對應的發文器實例。"""
    return PUBLISHERS[platform]()


__all__ = ["BasePublisher", "PUBLISHERS", "get_publisher"]
