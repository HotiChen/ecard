"""免費試用 14 天邏輯。

三個純函式，不依賴 Stripe / DB / 網路，可獨立單元測試：
  - start_trial:           計算試用到期時間（now + 14 天）
  - get_trial_status:      判斷試用狀態（ACTIVE / EXPIRED / NO_TRIAL）
  - trial_days_remaining:  計算剩餘天數（過期回傳 0）
"""

import enum
from datetime import datetime, timedelta, timezone

TRIAL_DAYS = 14


class TrialStatus(str, enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    NO_TRIAL = "no_trial"


def start_trial(now: datetime | None = None) -> datetime:
    """回傳試用到期時間 = now + TRIAL_DAYS 天。"""
    if now is None:
        now = datetime.now(timezone.utc)
    return now + timedelta(days=TRIAL_DAYS)


def get_trial_status(
    trial_ends_at: datetime | None,
    now: datetime | None = None,
) -> TrialStatus:
    """判斷試用狀態。trial_ends_at 為 None 表示從未開啟試用。"""
    if trial_ends_at is None:
        return TrialStatus.NO_TRIAL
    if now is None:
        now = datetime.now(timezone.utc)
    if trial_ends_at > now:
        return TrialStatus.ACTIVE
    return TrialStatus.EXPIRED


def trial_days_remaining(
    trial_ends_at: datetime,
    now: datetime | None = None,
) -> int:
    """剩餘試用天數（無條件捨去小數天，過期或到期當天回傳 0）。"""
    if now is None:
        now = datetime.now(timezone.utc)
    delta = trial_ends_at - now
    return max(0, delta.days)
