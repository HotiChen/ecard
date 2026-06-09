"""
Tests for next-post suggestion using a mock Anthropic client.
Only tests prompt construction and response parsing — no real API calls.
"""
from unittest.mock import AsyncMock, MagicMock
import pytest

from app.services.next_post_suggestion import (
    PostHistory,
    PostSuggestion,
    build_suggestion_prompt,
    parse_suggestion_response,
    suggest_next_post,
)


HISTORY = PostHistory(
    recent_contents=["攝影日記：金門夕陽", "街頭攝影心得分享", "相機包開箱"],
    top_hashtags=["#攝影", "#台灣風景", "#旅行"],
    best_platform="threads",
    avg_likes=95.0,
)


def test_post_history_fields():
    assert len(HISTORY.recent_contents) == 3
    assert HISTORY.best_platform == "threads"


def test_build_prompt_includes_recent_content():
    prompt = build_suggestion_prompt(HISTORY)
    assert "攝影日記：金門夕陽" in prompt


def test_build_prompt_includes_hashtags():
    prompt = build_suggestion_prompt(HISTORY)
    assert "#攝影" in prompt


def test_build_prompt_includes_platform():
    prompt = build_suggestion_prompt(HISTORY)
    assert "threads" in prompt


def test_build_prompt_includes_avg_likes():
    prompt = build_suggestion_prompt(HISTORY)
    assert "95" in prompt


def test_parse_response_returns_suggestion():
    raw = "建議發一篇關於台灣日出攝影的貼文，搭配 #攝影 #日出 標籤。"
    result = parse_suggestion_response(raw)
    assert isinstance(result, PostSuggestion)
    assert result.suggestion == raw


def test_parse_strips_whitespace():
    result = parse_suggestion_response("  建議內容  ")
    assert result.suggestion == "建議內容"


@pytest.mark.asyncio
async def test_suggest_calls_client():
    mock_client = MagicMock()
    mock_msg = MagicMock()
    mock_msg.content = [MagicMock(text="建議主題：夜間攝影技巧分享")]
    mock_client.messages = MagicMock()
    mock_client.messages.create = AsyncMock(return_value=mock_msg)

    result = await suggest_next_post(HISTORY, client=mock_client)
    assert mock_client.messages.create.called
    assert result.suggestion == "建議主題：夜間攝影技巧分享"


@pytest.mark.asyncio
async def test_suggest_uses_specified_model():
    mock_client = MagicMock()
    mock_msg = MagicMock()
    mock_msg.content = [MagicMock(text="建議")]
    mock_client.messages = MagicMock()
    mock_client.messages.create = AsyncMock(return_value=mock_msg)

    await suggest_next_post(HISTORY, client=mock_client, model="claude-sonnet-4-6")
    _, kwargs = mock_client.messages.create.call_args
    assert kwargs.get("model") == "claude-sonnet-4-6"
