"""爆文特徵報告單元測試（W6）。

驗證 generate_viral_report 從高互動貼文歸納特徵，結合 analytics /
content_analysis / time_analysis，純計算無外部依賴。
"""

from datetime import datetime, timezone

import pytest

from app.services.analytics import AggregatedMetrics
from app.services.viral_report import PostData, ViralFeatureReport, generate_viral_report

UTC = timezone.utc


def make_post(
    post_id: int,
    content: str,
    interactions: int,
    hour: int = 9,
) -> PostData:
    return PostData(
        post_id=post_id,
        content=content,
        posted_at=datetime(2026, 6, 9, hour, 0, tzinfo=UTC),
        metrics=AggregatedMetrics(
            likes=interactions, comments=0, replies=0, reposts=0, views=max(interactions * 10, 1)
        ),
    )


# ── 基本行為 ──────────────────────────────────────────────────────────────────


def test_empty_posts_raises():
    with pytest.raises(ValueError):
        generate_viral_report([])


def test_single_post_returns_report():
    post = make_post(1, "攝影師的一天 #攝影 #台灣", interactions=100)
    report = generate_viral_report([post])
    assert isinstance(report, ViralFeatureReport)
    assert report.post_count == 1


# ── 特徵計算 ──────────────────────────────────────────────────────────────────


def test_avg_hashtag_count_correct():
    posts = [
        make_post(1, "#a #b #c", interactions=100),   # 3 個 hashtag
        make_post(2, "#x #y", interactions=90),        # 2 個 hashtag
    ]
    report = generate_viral_report(posts)
    assert report.avg_hashtag_count == pytest.approx(2.5)


def test_avg_char_count_correct():
    posts = [
        make_post(1, "12345", interactions=100),    # 5 字
        make_post(2, "1234567890", interactions=80), # 10 字
    ]
    report = generate_viral_report(posts)
    assert report.avg_char_count == pytest.approx(7.5)


def test_has_question_ratio_correct():
    posts = [
        make_post(1, "你喜歡攝影嗎？", interactions=100),  # 有問句
        make_post(2, "攝影師的一天。", interactions=90),   # 沒問句
        make_post(3, "這好嗎？", interactions=80),          # 有問句
    ]
    report = generate_viral_report(posts)
    assert report.has_question_ratio == pytest.approx(2 / 3)


def test_has_exclamation_ratio_correct():
    posts = [
        make_post(1, "太棒了！", interactions=100),
        make_post(2, "普通的一天。", interactions=50),
    ]
    report = generate_viral_report(posts)
    assert report.has_exclamation_ratio == pytest.approx(0.5)


# ── top_n 篩選 ────────────────────────────────────────────────────────────────


def test_only_top_n_posts_analysed():
    posts = [
        make_post(1, "#a #b #c #d", interactions=100),  # 高互動，4 hashtag
        make_post(2, "#x", interactions=80),              # 高互動，1 hashtag
        make_post(3, "", interactions=1),                 # 低互動，排除
        make_post(4, "", interactions=2),                 # 低互動，排除
    ]
    report = generate_viral_report(posts, top_n=2)
    assert report.post_count == 2
    assert report.avg_hashtag_count == pytest.approx(2.5)  # (4+1)/2


def test_top_hours_come_from_top_posts():
    posts = [
        make_post(1, "高互動", interactions=200, hour=21),
        make_post(2, "高互動", interactions=150, hour=21),
        make_post(3, "低互動", interactions=5, hour=8),   # 低互動，top_n=2 排除
    ]
    report = generate_viral_report(posts, top_n=2)
    assert 21 in report.top_hours


def test_report_post_count_does_not_exceed_available():
    posts = [make_post(i, "test", interactions=i * 10) for i in range(1, 4)]
    report = generate_viral_report(posts, top_n=10)
    assert report.post_count == 3
