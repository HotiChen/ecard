"""貼文互動數據聚合邏輯（W5 數據看板）。

四個純函式，不依賴資料庫或外部服務，可獨立單元測試：
  - aggregate_metrics:       加總多筆 MetricSnapshot
  - group_by_platform:       按平台分組聚合
  - top_posts_by_engagement: 依互動總數排名前 N 篇
  - AggregatedMetrics.engagement_rate: 互動率 property
"""

from dataclasses import dataclass

from app.models.enums import Platform


@dataclass
class MetricSnapshot:
    """單筆互動數據（對應 PostMetric 欄位，不含 DB 主鍵）。"""

    post_id: int
    platform: Platform
    likes: int = 0
    comments: int = 0
    replies: int = 0
    reposts: int = 0
    views: int = 0


@dataclass
class AggregatedMetrics:
    """多筆 MetricSnapshot 聚合後的總數。"""

    likes: int
    comments: int
    replies: int
    reposts: int
    views: int

    @property
    def total_interactions(self) -> int:
        """互動總數（不含曝光 views）。"""
        return self.likes + self.comments + self.replies + self.reposts

    @property
    def engagement_rate(self) -> float:
        """互動率 = total_interactions / views；views 為 0 時回傳 0.0。"""
        if self.views == 0:
            return 0.0
        return self.total_interactions / self.views


def aggregate_metrics(metrics: list[MetricSnapshot]) -> AggregatedMetrics:
    """加總所有 MetricSnapshot，空串列回傳全零。"""
    return AggregatedMetrics(
        likes=sum(m.likes for m in metrics),
        comments=sum(m.comments for m in metrics),
        replies=sum(m.replies for m in metrics),
        reposts=sum(m.reposts for m in metrics),
        views=sum(m.views for m in metrics),
    )


def group_by_platform(
    metrics: list[MetricSnapshot],
) -> dict[Platform, AggregatedMetrics]:
    """將 MetricSnapshot 按平台分組後各自聚合。"""
    by_platform: dict[Platform, list[MetricSnapshot]] = {}
    for m in metrics:
        by_platform.setdefault(m.platform, []).append(m)
    return {p: aggregate_metrics(ms) for p, ms in by_platform.items()}


def top_posts_by_engagement(
    metrics_per_post: dict[int, list[MetricSnapshot]],
    n: int = 5,
) -> list[tuple[int, AggregatedMetrics]]:
    """回傳互動數最高的前 n 篇貼文，格式為 [(post_id, AggregatedMetrics), ...]。"""
    ranked = [
        (post_id, aggregate_metrics(ms))
        for post_id, ms in metrics_per_post.items()
    ]
    ranked.sort(key=lambda x: x[1].total_interactions, reverse=True)
    return ranked[:n]
