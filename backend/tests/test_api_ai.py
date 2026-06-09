"""
TDD tests for /api/v1/ai endpoints.
Overrides get_claude_client with a mock — no real API key needed.
"""
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.claude_client import get_claude_client


def make_mock_client(text: str) -> MagicMock:
    mock_msg = MagicMock()
    mock_msg.content = [MagicMock(text=text)]
    mock_client = MagicMock()
    mock_client.messages.create = AsyncMock(return_value=mock_msg)
    return mock_client


@pytest.fixture(autouse=True)
def override_client():
    mock = make_mock_client("positive")
    app.dependency_overrides[get_claude_client] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


client = TestClient(app)


# ── /api/v1/ai/sentiment ─────────────────────────────────────────────────────

def test_sentiment_returns_200():
    resp = client.post("/api/v1/ai/sentiment", json={"comments": ["好棒！"]})
    assert resp.status_code == 200


def test_sentiment_returns_list():
    resp = client.post("/api/v1/ai/sentiment", json={"comments": ["好棒！", "普通"]})
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_sentiment_result_has_label():
    resp = client.post("/api/v1/ai/sentiment", json={"comments": ["好棒！"]})
    assert "label" in resp.json()[0]


def test_sentiment_empty_list_returns_empty():
    resp = client.post("/api/v1/ai/sentiment", json={"comments": []})
    assert resp.json() == []


# ── /api/v1/ai/weekly-report ─────────────────────────────────────────────────

def _weekly_stats():
    return {
        "post_count": 5,
        "total_likes": 320,
        "total_comments": 60,
        "total_reposts": 15,
        "total_views": 4200,
        "top_platform": "threads",
        "best_post_content": "最佳貼文",
    }


def test_weekly_report_returns_200(override_client):
    override_client.messages.create = AsyncMock(
        return_value=MagicMock(content=[MagicMock(text="本週週報摘要")])
    )
    resp = client.post("/api/v1/ai/weekly-report", json=_weekly_stats())
    assert resp.status_code == 200


def test_weekly_report_has_summary(override_client):
    override_client.messages.create = AsyncMock(
        return_value=MagicMock(content=[MagicMock(text="本週週報摘要")])
    )
    resp = client.post("/api/v1/ai/weekly-report", json=_weekly_stats())
    assert "summary" in resp.json()
    assert resp.json()["summary"] == "本週週報摘要"


# ── /api/v1/ai/suggest ───────────────────────────────────────────────────────

def _history():
    return {
        "recent_contents": ["攝影日記第一篇", "街頭攝影"],
        "top_hashtags": ["#攝影", "#台灣"],
        "best_platform": "threads",
        "avg_likes": 95.0,
    }


def test_suggest_returns_200(override_client):
    override_client.messages.create = AsyncMock(
        return_value=MagicMock(content=[MagicMock(text="建議主題：夜間攝影")])
    )
    resp = client.post("/api/v1/ai/suggest", json=_history())
    assert resp.status_code == 200


def test_suggest_has_suggestion(override_client):
    override_client.messages.create = AsyncMock(
        return_value=MagicMock(content=[MagicMock(text="建議主題：夜間攝影")])
    )
    resp = client.post("/api/v1/ai/suggest", json=_history())
    assert resp.json()["suggestion"] == "建議主題：夜間攝影"
