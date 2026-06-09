"""免費試用 14 天邏輯單元測試（W7）。

驗證試用期起算、狀態判斷、剩餘天數計算，全用固定 datetime，不依賴真實時鐘。
"""

from datetime import datetime, timedelta, timezone

import pytest

from app.services.trial import (
    TRIAL_DAYS,
    TrialStatus,
    get_trial_status,
    start_trial,
    trial_days_remaining,
)

NOW = datetime(2026, 6, 9, 12, 0, 0, tzinfo=timezone.utc)


# ── start_trial ───────────────────────────────────────────────────────────────


def test_start_trial_returns_now_plus_14_days():
    ends_at = start_trial(now=NOW)
    assert ends_at == NOW + timedelta(days=14)


def test_trial_days_constant_is_14():
    assert TRIAL_DAYS == 14


# ── get_trial_status ──────────────────────────────────────────────────────────


def test_trial_active_when_ends_in_future():
    ends_at = NOW + timedelta(days=7)
    assert get_trial_status(ends_at, now=NOW) == TrialStatus.ACTIVE


def test_trial_expired_when_ends_in_past():
    ends_at = NOW - timedelta(seconds=1)
    assert get_trial_status(ends_at, now=NOW) == TrialStatus.EXPIRED


def test_trial_expired_when_ends_exactly_now():
    assert get_trial_status(NOW, now=NOW) == TrialStatus.EXPIRED


def test_no_trial_when_ends_at_is_none():
    assert get_trial_status(None, now=NOW) == TrialStatus.NO_TRIAL


# ── trial_days_remaining ──────────────────────────────────────────────────────


def test_full_14_days_remaining_at_start():
    ends_at = start_trial(now=NOW)
    assert trial_days_remaining(ends_at, now=NOW) == 14


def test_days_remaining_correct_mid_trial():
    ends_at = NOW + timedelta(days=5, hours=6)
    # 5 days and 6 hours → floor to 5
    assert trial_days_remaining(ends_at, now=NOW) == 5


def test_days_remaining_zero_when_expired():
    ends_at = NOW - timedelta(days=2)
    assert trial_days_remaining(ends_at, now=NOW) == 0


def test_days_remaining_zero_exactly_at_expiry():
    assert trial_days_remaining(NOW, now=NOW) == 0
