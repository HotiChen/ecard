"""Claude API client factory and FastAPI dependency."""
from __future__ import annotations

from typing import Any, Generator, Protocol

try:
    import anthropic
except ImportError:  # anthropic not installed — tests mock it via patch
    anthropic = None  # type: ignore[assignment]

from app.core.config import settings


class ClaudeClientProtocol(Protocol):
    """Structural interface for the Anthropic client — enables mock injection."""

    @property
    def messages(self) -> Any: ...


def make_claude_client(api_key: str | None = None) -> Any:
    """Create an Anthropic client, falling back to the settings key."""
    key = api_key or settings.anthropic_api_key
    return anthropic.Anthropic(api_key=key)


def get_claude_client() -> Generator[Any, None, None]:
    """FastAPI dependency that yields a Claude client.

    Override in tests:
        app.dependency_overrides[get_claude_client] = lambda: mock_client
    """
    yield make_claude_client()
