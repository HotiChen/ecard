"""排程發文核心邏輯。

兩個純函式，不依賴 Celery / Redis / DB，可獨立單元測試：
  - validate_schedule_time: 拒絕過去時間，確保排程合理
  - is_post_due: 判斷一筆排程任務是否到了應執行的時刻
"""

from datetime import datetime, timezone


def validate_schedule_time(
    scheduled_at: datetime,
    now: datetime | None = None,
) -> datetime:
    """驗證排程時間必須在未來。

    Args:
        scheduled_at: 使用者指定的發文時間（應含時區資訊）。
        now: 注入當前時間（測試用）；None 時使用 UTC now。

    Returns:
        通過驗證的 scheduled_at。

    Raises:
        ValueError: 若 scheduled_at <= now。
    """
    if now is None:
        now = datetime.now(timezone.utc)
    if scheduled_at <= now:
        raise ValueError(f"排程時間必須在未來，不能是過去或現在的時間：{scheduled_at.isoformat()}")
    return scheduled_at


def is_post_due(
    scheduled_at: datetime,
    is_canceled: bool,
    executed_at: datetime | None,
    now: datetime | None = None,
) -> bool:
    """判斷一筆排程任務是否應該立即執行。

    條件：scheduled_at <= now AND 未取消 AND 尚未執行。
    """
    if now is None:
        now = datetime.now(timezone.utc)
    if is_canceled:
        return False
    if executed_at is not None:
        return False
    return scheduled_at <= now
