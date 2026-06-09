"""最佳發文時段分析（W6 AI 分析引擎）。

兩個純函式，以發文時間 + 互動數據為輸入，統計各時段平均互動數並排名。
不依賴資料庫、Celery 或外部 API，可獨立單元測試。
"""

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

from app.services.analytics import AggregatedMetrics


@dataclass
class HourlyStats:
    """單一小時的互動統計。"""

    hour: int               # 0–23（UTC）
    post_count: int
    avg_interactions: float


@dataclass
class WeekdayStats:
    """單一星期幾的互動統計。"""

    weekday: int            # 0=Monday … 6=Sunday
    post_count: int
    avg_interactions: float


def best_posting_hours(
    posts: list[tuple[datetime, AggregatedMetrics]],
    top_n: int | None = None,
) -> list[HourlyStats]:
    """依平均互動數排名各小時，回傳前 top_n 筆（None 表示全部）。"""
    bucket: dict[int, list[int]] = defaultdict(list)
    for dt, agg in posts:
        bucket[dt.hour].append(agg.total_interactions)

    stats = [
        HourlyStats(
            hour=hour,
            post_count=len(vals),
            avg_interactions=sum(vals) / len(vals),
        )
        for hour, vals in bucket.items()
    ]
    stats.sort(key=lambda s: s.avg_interactions, reverse=True)
    return stats[:top_n] if top_n is not None else stats


def best_posting_weekdays(
    posts: list[tuple[datetime, AggregatedMetrics]],
) -> list[WeekdayStats]:
    """依平均互動數排名星期幾（0=Monday），回傳全部。"""
    bucket: dict[int, list[int]] = defaultdict(list)
    for dt, agg in posts:
        bucket[dt.weekday()].append(agg.total_interactions)

    stats = [
        WeekdayStats(
            weekday=wd,
            post_count=len(vals),
            avg_interactions=sum(vals) / len(vals),
        )
        for wd, vals in bucket.items()
    ]
    stats.sort(key=lambda s: s.avg_interactions, reverse=True)
    return stats
