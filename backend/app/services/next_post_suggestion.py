from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class PostHistory:
    recent_contents: list[str]
    top_hashtags: list[str]
    best_platform: str
    avg_likes: float


@dataclass
class PostSuggestion:
    suggestion: str


def build_suggestion_prompt(history: PostHistory) -> str:
    recent = "\n".join(f"- {c}" for c in history.recent_contents)
    hashtags = " ".join(history.top_hashtags)
    return (
        "你是一位社群媒體內容策略師。根據以下創作者的歷史貼文資料，"
        "建議下一篇最有可能爆紅的貼文主題與大綱（約 80–120 字）。\n\n"
        f"近期貼文：\n{recent}\n\n"
        f"常用標籤：{hashtags}\n"
        f"表現最佳平台：{history.best_platform}\n"
        f"平均按讚數：{history.avg_likes:.0f}\n\n"
        "下一篇建議："
    )


def parse_suggestion_response(response_text: str) -> PostSuggestion:
    return PostSuggestion(suggestion=response_text.strip())


async def suggest_next_post(
    history: PostHistory,
    *,
    client: Any,
    model: str = "claude-haiku-4-5-20251001",
) -> PostSuggestion:
    prompt = build_suggestion_prompt(history)
    message = await client.messages.create(
        model=model,
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    text = message.content[0].text
    return parse_suggestion_response(text)
