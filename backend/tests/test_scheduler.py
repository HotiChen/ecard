"""排程邏輯單元測試（W4）。

測試 validate_schedule_time 與 is_post_due 的純時間邏輯。
不依賴 Celery、Redis 或資料庫。
"""

from datetime import datetime, timedelta, timezone

import pytest

from app.services.scheduler import is_post_due, validate_schedule_time

NOW = datetime(2026, 6, 9, 12, 0, 0, tzinfo=timezone.utc)
PAST = NOW - timedelta(hours=1)
FUTURE = NOW + timedelta(hours=1)


# ── validate_schedule_time ────────────────────────────────────────────────────


def test_validate_future_time_returns_datetime():
    result = validate_schedule_time(FUTURE, now=NOW)
    assert result == FUTURE


def test_validate_past_time_raises_value_error():
    with pytest.raises(ValueError, match="過去"):
        validate_schedule_time(PAST, now=NOW)


def test_validate_exactly_now_raises_value_error():
    with pytest.raises(ValueError, match="過去"):
        validate_schedule_time(NOW, now=NOW)


def test_validate_one_second_ahead_is_ok():
    just_future = NOW + timedelta(seconds=1)
    assert validate_schedule_time(just_future, now=NOW) == just_future


# ── is_post_due ───────────────────────────────────────────────────────────────


def test_past_scheduled_not_canceled_not_executed_is_due():
    assert is_post_due(scheduled_at=PAST, is_canceled=False, executed_at=None, now=NOW)


def test_future_scheduled_is_not_due():
    assert not is_post_due(scheduled_at=FUTURE, is_canceled=False, executed_at=None, now=NOW)


def test_canceled_post_is_not_due():
    assert not is_post_due(scheduled_at=PAST, is_canceled=True, executed_at=None, now=NOW)


def test_already_executed_post_is_not_due():
    assert not is_post_due(scheduled_at=PAST, is_canceled=False, executed_at=PAST, now=NOW)


def test_exactly_at_scheduled_time_is_due():
    assert is_post_due(scheduled_at=NOW, is_canceled=False, executed_at=None, now=NOW)
