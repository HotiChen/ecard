from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class WeeklyStats:
    post_count: int
    total_likes: int
    total_comments: int
    total_reposts: int
    total_views: int
    top_platform: str
    best_post_content: str


@dataclass
class WeeklyReport:
    summary: str
    stats: WeeklyStats


def build_weekly_report_prompt(stats: WeeklyStats) -> str:
    return (
        "你是一位社群媒體數據分析師。請根據以下本週數據，生成一份簡短的中文週報摘要（約 100–150 字），"
        "包含本週表現亮點、最佳平台與下週建議。\n\n"
        f"本週貼文數：{stats.post_count}\n"
        f"總按讚數：{stats.total_likes}\n"
        f"總留言數：{stats.total_comments}\n"
        f"總轉發數：{stats.total_reposts}\n"
        f"總觀看數：{stats.total_views}\n"
        f"表現最佳平台：{stats.top_platform}\n"
        f"最受歡迎貼文：{stats.best_post_content}\n\n"
        "週報摘要："
    )


def parse_weekly_report_response(response_text: str, stats: WeeklyStats) -> WeeklyReport:
    return WeeklyReport(summary=response_text.strip(), stats=stats)


async def generate_weekly_report(
    stats: WeeklyStats,
    *,
    client: Any,
    model: str = "claude-haiku-4-5-20251001",
) -> WeeklyReport:
    prompt = build_weekly_report_prompt(stats)
    message = await client.messages.create(
        model=model,
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    text = message.content[0].text
    return parse_weekly_report_response(text, stats)
