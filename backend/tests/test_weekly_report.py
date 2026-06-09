"""
Tests for weekly report generation using a mock Anthropic client.
Only tests prompt construction and response parsing — no real API calls.
"""
from unittest.mock import AsyncMock, MagicMock
import pytest

from app.services.weekly_report import (
    WeeklyStats,
    WeeklyReport,
    build_weekly_report_prompt,
    parse_weekly_report_response,
    generate_weekly_report,
)


STATS = WeeklyStats(
    post_count=5,
    total_likes=320,
    total_comments=60,
    total_reposts=15,
    total_views=4200,
    top_platform="threads",
    best_post_content="最受歡迎的攝影作品分享",
)


def test_weekly_stats_fields():
    assert STATS.post_count == 5
    assert STATS.top_platform == "threads"


def test_build_prompt_includes_post_count():
    prompt = build_weekly_report_prompt(STATS)
    assert "5" in prompt


def test_build_prompt_includes_likes():
    prompt = build_weekly_report_prompt(STATS)
    assert "320" in prompt


def test_build_prompt_includes_top_platform():
    prompt = build_weekly_report_prompt(STATS)
    assert "threads" in prompt


def test_build_prompt_includes_best_post():
    prompt = build_weekly_report_prompt(STATS)
    assert "最受歡迎的攝影作品分享" in prompt


def test_parse_response_returns_weekly_report():
    raw = "本週共發布 5 篇貼文，互動表現亮眼，建議持續在 Threads 上深耕。"
    result = parse_weekly_report_response(raw, STATS)
    assert isinstance(result, WeeklyReport)
    assert result.summary == raw
    assert result.stats == STATS


@pytest.mark.asyncio
async def test_generate_calls_client():
    mock_client = MagicMock()
    mock_msg = MagicMock()
    mock_msg.content = [MagicMock(text="好的週報摘要")]
    mock_client.messages = MagicMock()
    mock_client.messages.create = AsyncMock(return_value=mock_msg)

    report = await generate_weekly_report(STATS, client=mock_client)
    assert mock_client.messages.create.called
    assert report.summary == "好的週報摘要"
    assert report.stats == STATS


@pytest.mark.asyncio
async def test_generate_passes_model_to_client():
    mock_client = MagicMock()
    mock_msg = MagicMock()
    mock_msg.content = [MagicMock(text="摘要")]
    mock_client.messages = MagicMock()
    mock_client.messages.create = AsyncMock(return_value=mock_msg)

    await generate_weekly_report(STATS, client=mock_client, model="claude-haiku-4-5-20251001")
    call_kwargs = mock_client.messages.create.call_args
    assert call_kwargs.kwargs.get("model") == "claude-haiku-4-5-20251001" or \
           call_kwargs.args[0] == "claude-haiku-4-5-20251001" if call_kwargs.args else \
           "claude-haiku-4-5-20251001" in str(call_kwargs)
