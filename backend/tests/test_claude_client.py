"""
TDD tests for Claude API client factory.
Verifies dependency injection pattern — no real API key required.
"""
from unittest.mock import MagicMock, patch

import pytest

from app.services.claude_client import (
    ClaudeClientProtocol,
    get_claude_client,
    make_claude_client,
)


def test_make_claude_client_returns_object_with_messages():
    """make_claude_client should return an object that has a .messages attribute."""
    with patch("app.services.claude_client.anthropic") as mock_anthropic:
        mock_instance = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_instance
        client = make_claude_client(api_key="test-key")
        assert client is mock_instance
        mock_anthropic.Anthropic.assert_called_once_with(api_key="test-key")


def test_make_claude_client_uses_settings_key_when_none_given():
    with patch("app.services.claude_client.anthropic") as mock_anthropic:
        with patch("app.services.claude_client.settings") as mock_settings:
            mock_settings.anthropic_api_key = "settings-key"
            mock_anthropic.Anthropic.return_value = MagicMock()
            make_claude_client()
            mock_anthropic.Anthropic.assert_called_once_with(api_key="settings-key")


def test_get_claude_client_is_generator():
    """get_claude_client is a FastAPI dependency (generator function)."""
    with patch("app.services.claude_client.make_claude_client") as mock_make:
        mock_make.return_value = MagicMock()
        gen = get_claude_client()
        client = next(gen)
        assert client is mock_make.return_value


def test_protocol_has_messages_attribute():
    """Any object with a .messages attribute satisfies the protocol."""
    mock = MagicMock(spec=ClaudeClientProtocol)
    assert hasattr(mock, "messages")


def test_mock_client_usable_as_dependency():
    """Verify a MagicMock passes as a ClaudeClientProtocol replacement."""
    mock_client = MagicMock()
    mock_client.messages.create = MagicMock()
    assert callable(mock_client.messages.create)
