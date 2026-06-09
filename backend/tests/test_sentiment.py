"""
Tests for comment sentiment analysis using a mock Anthropic client.
We only test prompt construction and response parsing — no real API calls.
"""
from unittest.mock import AsyncMock, MagicMock
import pytest

from app.services.sentiment import (
    SentimentResult,
    SentimentLabel,
    analyze_comments,
    build_sentiment_prompt,
    parse_sentiment_response,
)


COMMENTS = ["這照片太美了！", "普通吧", "差評，不喜歡"]


def test_build_prompt_includes_all_comments():
    prompt = build_sentiment_prompt(COMMENTS)
    for comment in COMMENTS:
        assert comment in prompt


def test_build_prompt_includes_instruction_keyword():
    prompt = build_sentiment_prompt(COMMENTS)
    assert "sentiment" in prompt.lower() or "情緒" in prompt or "positive" in prompt.lower()


def test_parse_positive():
    result = parse_sentiment_response("positive", COMMENTS[0])
    assert result.label == SentimentLabel.POSITIVE
    assert result.comment == COMMENTS[0]


def test_parse_negative():
    result = parse_sentiment_response("negative", COMMENTS[2])
    assert result.label == SentimentLabel.NEGATIVE


def test_parse_neutral():
    result = parse_sentiment_response("neutral", COMMENTS[1])
    assert result.label == SentimentLabel.NEUTRAL


def test_parse_case_insensitive():
    result = parse_sentiment_response("POSITIVE", COMMENTS[0])
    assert result.label == SentimentLabel.POSITIVE


def test_parse_unknown_falls_back_to_neutral():
    result = parse_sentiment_response("gibberish", COMMENTS[0])
    assert result.label == SentimentLabel.NEUTRAL


@pytest.mark.asyncio
async def test_analyze_comments_calls_client():
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="positive")]
    mock_client.messages = MagicMock()
    mock_client.messages.create = AsyncMock(return_value=mock_message)

    results = await analyze_comments(["好！"], client=mock_client)
    assert mock_client.messages.create.called
    assert len(results) == 1
    assert results[0].label == SentimentLabel.POSITIVE


@pytest.mark.asyncio
async def test_analyze_comments_returns_one_result_per_comment():
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="neutral")]
    mock_client.messages = MagicMock()
    mock_client.messages.create = AsyncMock(return_value=mock_message)

    results = await analyze_comments(COMMENTS, client=mock_client)
    assert len(results) == len(COMMENTS)


@pytest.mark.asyncio
async def test_analyze_comments_empty_list():
    mock_client = MagicMock()
    results = await analyze_comments([], client=mock_client)
    assert results == []
    mock_client.messages.create.assert_not_called() if hasattr(mock_client.messages, "create") else None
