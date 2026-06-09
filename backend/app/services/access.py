"""授權與 Feature Gating。

根據訂閱方案（plan）+ 訂閱狀態（status）+ 試用期限管控功能存取，
完全無狀態，可獨立單元測試，不依賴 Stripe 或資料庫。

功能分級：
  Level 0 (PUBLISH, BACKUP)         — 所有有效訂閱
  Level 1 (SCHEDULE, MULTI_PLATFORM) — BASIC 以上
  Level 2 (AI_ANALYSIS, WEEKLY_REPORT) — PRO 專屬

試用期（TRIALING）且 trial_ends_at > now：開放全部功能。
PAST_DUE：寬限期，維持原方案權限。
CANCELED：完全關閉。
"""

import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.models.enums import SubscriptionPlan, SubscriptionStatus


class Feature(str, enum.Enum):
    PUBLISH = "publish"                  # 發文（Level 0）
    BACKUP = "backup"                    # 備份存證（Level 0）
    SCHEDULE = "schedule"               # 排程發文（Level 1）
    MULTI_PLATFORM = "multi_platform"   # 多平台同步（Level 1）
    AI_ANALYSIS = "ai_analysis"         # Claude AI 分析（Level 2）
    WEEKLY_REPORT = "weekly_report"     # 每週 AI 報告（Level 2）


_PLAN_FEATURES: dict[SubscriptionPlan, set[Feature]] = {
    SubscriptionPlan.FREE: {
        Feature.PUBLISH,
        Feature.BACKUP,
    },
    SubscriptionPlan.BASIC: {
        Feature.PUBLISH,
        Feature.BACKUP,
        Feature.SCHEDULE,
        Feature.MULTI_PLATFORM,
    },
    SubscriptionPlan.PRO: set(Feature),  # 全部功能
}


@dataclass
class AccessContext:
    plan: SubscriptionPlan
    status: SubscriptionStatus
    trial_ends_at: datetime | None = field(default=None)


def is_subscription_active(ctx: AccessContext, now: datetime | None = None) -> bool:
    """訂閱是否有效（可使用任何功能）。"""
    if now is None:
        now = datetime.now(timezone.utc)

    if ctx.status == SubscriptionStatus.CANCELED:
        return False

    if ctx.status == SubscriptionStatus.TRIALING:
        return ctx.trial_ends_at is not None and ctx.trial_ends_at > now

    # ACTIVE 或 PAST_DUE（寬限期）皆視為有效
    return True


def can_access(ctx: AccessContext, feature: Feature, now: datetime | None = None) -> bool:
    """使用者是否可存取指定功能。"""
    if now is None:
        now = datetime.now(timezone.utc)

    if not is_subscription_active(ctx, now=now):
        return False

    # 試用期間開放全部功能
    if ctx.status == SubscriptionStatus.TRIALING:
        return True

    return feature in _PLAN_FEATURES.get(ctx.plan, set())
