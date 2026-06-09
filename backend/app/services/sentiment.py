from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Any


class SentimentLabel(str, enum.Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


@dataclass
class SentimentResult:
    comment: str
    label: SentimentLabel


def build_sentiment_prompt(comments: list[str]) -> str:
    numbered = "\n".join(f"{i+1}. {c}" for i, c in enumerate(comments))
    return (
        "Classify the sentiment of each comment below as positive, neutral, or negative.\n"
        "Reply with only the sentiment label (positive / neutral / negative) for each comment, one per line.\n\n"
        f"Comments:\n{numbered}\n\n"
        "情緒分析結果（每行一個標籤）："
    )


def parse_sentiment_response(response_text: str, comment: str) -> SentimentResult:
    label_str = response_text.strip().lower()
    try:
        label = SentimentLabel(label_str)
    except ValueError:
        label = SentimentLabel.NEUTRAL
    return SentimentResult(comment=comment, label=label)


async def analyze_comments(
    comments: list[str],
    *,
    client: Any,
    model: str = "claude-haiku-4-5-20251001",
) -> list[SentimentResult]:
    if not comments:
        return []

    results: list[SentimentResult] = []
    for comment in comments:
        prompt = build_sentiment_prompt([comment])
        message = await client.messages.create(
            model=model,
            max_tokens=16,
            messages=[{"role": "user", "content": prompt}],
        )
        text = message.content[0].text
        results.append(parse_sentiment_response(text, comment))
    return results
