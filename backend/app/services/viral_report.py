"""爆文特徵報告（W6 AI 分析引擎）。

generate_viral_report 串接三個分析模組：
  analytics        → 互動數排名，篩出前 top_n 高互動文章
  content_analysis → 提取各文章的文字特徵（hashtag、字數、語氣）
  time_analysis    → 計算高互動文章的發文時段分佈

輸出 ViralFeatureReport，供後續 Claude 生成建議或直接展示看板。
全程純計算，不依賴資料庫或外部 API。
"""

from dataclasses import dataclass, field
from datetime import datetime

from app.services.analytics import AggregatedMetrics
from app.services.content_analysis import extract_features
from app.services.time_analysis import best_posting_hours, best_posting_weekdays


@dataclass
class PostData:
    """一篇貼文的完整分析輸入。"""

    post_id: int
    content: str
    posted_at: datetime
    metrics: AggregatedMetrics


@dataclass
class ViralFeatureReport:
    """高互動貼文共同特徵摘要。"""

    post_count: int
    avg_hashtag_count: float
    avg_char_count: float
    avg_url_count: float
    has_question_ratio: float
    has_exclamation_ratio: float
    top_hours: list[int] = field(default_factory=list)     # 前 3 高互動小時
    top_weekdays: list[int] = field(default_factory=list)  # 前 3 高互動星期幾


def generate_viral_report(
    posts: list[PostData],
    top_n: int = 10,
) -> ViralFeatureReport:
    """從 posts 挑出互動數前 top_n 篇，歸納爆文特徵。

    Raises:
        ValueError: posts 為空。
    """
    if not posts:
        raise ValueError("posts 不能為空，無法產生報告")

    # 依互動數降序，取前 top_n
    ranked = sorted(posts, key=lambda p: p.metrics.total_interactions, reverse=True)
    top = ranked[:top_n]

    features = [extract_features(p.content) for p in top]
    n = len(top)

    # 時段分析
    time_pairs = [(p.posted_at, p.metrics) for p in top]
    hour_stats = best_posting_hours(time_pairs, top_n=3)
    weekday_stats = best_posting_weekdays(time_pairs)

    return ViralFeatureReport(
        post_count=n,
        avg_hashtag_count=sum(f.hashtag_count for f in features) / n,
        avg_char_count=sum(f.char_count for f in features) / n,
        avg_url_count=sum(f.url_count for f in features) / n,
        has_question_ratio=sum(1 for f in features if f.has_question) / n,
        has_exclamation_ratio=sum(1 for f in features if f.has_exclamation) / n,
        top_hours=[s.hour for s in hour_stats],
        top_weekdays=[s.weekday for s in weekday_stats[:3]],
    )
