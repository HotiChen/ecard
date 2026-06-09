"""貼文數據看板聚合邏輯單元測試（W5）。

驗證 aggregate_metrics、engagement_rate、group_by_platform、
top_posts_by_engagement 等純函式，不依賴資料庫或網路。
"""

import pytest

from app.models.enums import Platform
from app.services.analytics import (
    AggregatedMetrics,
    MetricSnapshot,
    aggregate_metrics,
    group_by_platform,
    top_posts_by_engagement,
)


def snap(
    post_id: int = 1,
    platform: Platform = Platform.THREADS,
    *,
    likes: int = 0,
    comments: int = 0,
    replies: int = 0,
    reposts: int = 0,
    views: int = 0,
) -> MetricSnapshot:
    return MetricSnapshot(
        post_id=post_id,
        platform=platform,
        likes=likes,
        comments=comments,
        replies=replies,
        reposts=reposts,
        views=views,
    )


# ── aggregate_metrics ─────────────────────────────────────────────────────────


def test_aggregate_empty_returns_zeros():
    result = aggregate_metrics([])
    assert result.likes == 0
    assert result.comments == 0
    assert result.views == 0


def test_aggregate_sums_all_fields():
    metrics = [
        snap(likes=10, comments=5, replies=2, reposts=3, views=100),
        snap(likes=20, comments=3, replies=1, reposts=1, views=200),
    ]
    result = aggregate_metrics(metrics)
    assert result.likes == 30
    assert result.comments == 8
    assert result.replies == 3
    assert result.reposts == 4
    assert result.views == 300


def test_total_interactions_excludes_views():
    agg = AggregatedMetrics(likes=5, comments=3, replies=2, reposts=1, views=1000)
    assert agg.total_interactions == 11


# ── engagement_rate ───────────────────────────────────────────────────────────


def test_engagement_rate_correct():
    agg = AggregatedMetrics(likes=10, comments=5, replies=0, reposts=0, views=100)
    assert agg.engagement_rate == pytest.approx(0.15)


def test_engagement_rate_zero_when_no_views():
    agg = AggregatedMetrics(likes=100, comments=50, replies=0, reposts=0, views=0)
    assert agg.engagement_rate == 0.0


# ── group_by_platform ─────────────────────────────────────────────────────────


def test_group_by_platform_separates_correctly():
    metrics = [
        snap(platform=Platform.THREADS, likes=10, views=100),
        snap(platform=Platform.INSTAGRAM, likes=20, views=200),
        snap(platform=Platform.THREADS, likes=5, views=50),
    ]
    result = group_by_platform(metrics)
    assert result[Platform.THREADS].likes == 15
    assert result[Platform.THREADS].views == 150
    assert result[Platform.INSTAGRAM].likes == 20


def test_group_by_platform_only_includes_present_platforms():
    metrics = [snap(platform=Platform.THREADS, likes=1)]
    result = group_by_platform(metrics)
    assert Platform.THREADS in result
    assert Platform.INSTAGRAM not in result


# ── top_posts_by_engagement ───────────────────────────────────────────────────


def test_top_posts_sorted_by_total_interactions():
    metrics_per_post = {
        1: [snap(post_id=1, likes=5, comments=1)],
        2: [snap(post_id=2, likes=100, comments=50)],
        3: [snap(post_id=3, likes=10, comments=2)],
    }
    result = top_posts_by_engagement(metrics_per_post, n=3)
    assert [post_id for post_id, _ in result] == [2, 3, 1]


def test_top_posts_respects_n_limit():
    metrics_per_post = {i: [snap(post_id=i, likes=i)] for i in range(1, 11)}
    result = top_posts_by_engagement(metrics_per_post, n=3)
    assert len(result) == 3


def test_top_posts_fewer_than_n_returns_all():
    metrics_per_post = {1: [snap(post_id=1, likes=5)]}
    result = top_posts_by_engagement(metrics_per_post, n=10)
    assert len(result) == 1
