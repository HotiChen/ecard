"""最佳發文時段分析單元測試（W6）。

驗證按小時／星期幾聚合互動數據並排名，純 datetime 計算，不依賴資料庫或 API。
"""

from datetime import datetime, timezone

import pytest

from app.services.analytics import AggregatedMetrics
from app.services.time_analysis import (
    HourlyStats,
    WeekdayStats,
    best_posting_hours,
    best_posting_weekdays,
)

UTC = timezone.utc


def agg(interactions: int = 0, views: int = 100) -> AggregatedMetrics:
    return AggregatedMetrics(
        likes=interactions, comments=0, replies=0, reposts=0, views=views
    )


def post_at(hour: int, weekday_offset: int = 0, interactions: int = 10) -> tuple:
    # 2026-06-08 是星期一（weekday=0）；offset 加幾天就是那個星期幾
    dt = datetime(2026, 6, 8 + weekday_offset, hour, 0, 0, tzinfo=UTC)
    return (dt, agg(interactions))


# ── best_posting_hours ────────────────────────────────────────────────────────


def test_empty_posts_returns_empty_hours():
    assert best_posting_hours([]) == []


def test_single_post_returns_its_hour():
    result = best_posting_hours([post_at(hour=9, interactions=50)])
    assert len(result) == 1
    assert result[0].hour == 9


def test_hours_ranked_by_avg_interactions():
    posts = [
        post_at(hour=9, interactions=100),
        post_at(hour=9, interactions=80),   # avg=90 at 9
        post_at(hour=14, interactions=20),  # avg=20 at 14
        post_at(hour=20, interactions=50),  # avg=50 at 20
    ]
    result = best_posting_hours(posts, top_n=3)
    assert result[0].hour == 9
    assert result[1].hour == 20
    assert result[2].hour == 14


def test_top_n_limits_result():
    posts = [post_at(hour=h, interactions=h) for h in range(6)]
    result = best_posting_hours(posts, top_n=2)
    assert len(result) == 2


def test_hourly_stats_has_post_count():
    posts = [post_at(hour=10, interactions=30), post_at(hour=10, interactions=50)]
    result = best_posting_hours(posts)
    assert result[0].post_count == 2


def test_hourly_stats_avg_interactions_correct():
    posts = [post_at(hour=8, interactions=40), post_at(hour=8, interactions=60)]
    result = best_posting_hours(posts)
    assert result[0].avg_interactions == pytest.approx(50.0)


def test_returns_hourly_stats_instances():
    result = best_posting_hours([post_at(hour=12)])
    assert isinstance(result[0], HourlyStats)


# ── best_posting_weekdays ─────────────────────────────────────────────────────


def test_empty_posts_returns_empty_weekdays():
    assert best_posting_weekdays([]) == []


def test_weekdays_ranked_by_avg_interactions():
    posts = [
        post_at(hour=9, weekday_offset=0, interactions=100),  # Monday
        post_at(hour=9, weekday_offset=2, interactions=20),   # Wednesday
        post_at(hour=9, weekday_offset=5, interactions=60),   # Saturday
    ]
    result = best_posting_weekdays(posts)
    assert result[0].weekday == 0   # Monday highest
    assert result[1].weekday == 5   # Saturday second
    assert result[2].weekday == 2   # Wednesday lowest


def test_weekday_stats_has_post_count():
    posts = [
        post_at(hour=9, weekday_offset=1, interactions=30),
        post_at(hour=12, weekday_offset=1, interactions=50),
    ]
    result = best_posting_weekdays(posts)
    assert result[0].post_count == 2


def test_returns_weekday_stats_instances():
    result = best_posting_weekdays([post_at(hour=10)])
    assert isinstance(result[0], WeekdayStats)
