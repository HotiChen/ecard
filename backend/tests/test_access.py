"""授權／Feature Gating 單元測試（W7）。

驗證 can_access 根據 plan + status + trial 時間正確管控功能存取。
不依賴 Stripe、資料庫或網路。
"""

from datetime import datetime, timedelta, timezone

import pytest

from app.services.access import AccessContext, Feature, can_access, is_subscription_active
from app.models.enums import SubscriptionPlan, SubscriptionStatus

NOW = datetime(2026, 6, 9, 12, 0, 0, tzinfo=timezone.utc)
FUTURE = NOW + timedelta(days=7)
PAST = NOW - timedelta(days=1)


# ── is_subscription_active ────────────────────────────────────────────────────


def test_trialing_with_valid_trial_is_active():
    ctx = AccessContext(plan=SubscriptionPlan.FREE, status=SubscriptionStatus.TRIALING, trial_ends_at=FUTURE)
    assert is_subscription_active(ctx, now=NOW)


def test_trialing_with_expired_trial_is_inactive():
    ctx = AccessContext(plan=SubscriptionPlan.FREE, status=SubscriptionStatus.TRIALING, trial_ends_at=PAST)
    assert not is_subscription_active(ctx, now=NOW)


def test_active_basic_is_active():
    ctx = AccessContext(plan=SubscriptionPlan.BASIC, status=SubscriptionStatus.ACTIVE)
    assert is_subscription_active(ctx, now=NOW)


def test_past_due_is_still_active():
    ctx = AccessContext(plan=SubscriptionPlan.BASIC, status=SubscriptionStatus.PAST_DUE)
    assert is_subscription_active(ctx, now=NOW)


def test_canceled_is_not_active():
    ctx = AccessContext(plan=SubscriptionPlan.PRO, status=SubscriptionStatus.CANCELED)
    assert not is_subscription_active(ctx, now=NOW)


# ── can_access — 試用期 ───────────────────────────────────────────────────────


def test_trialing_user_can_access_all_features():
    ctx = AccessContext(plan=SubscriptionPlan.FREE, status=SubscriptionStatus.TRIALING, trial_ends_at=FUTURE)
    for feature in Feature:
        assert can_access(ctx, feature, now=NOW), f"expected access to {feature}"


def test_expired_trial_cannot_access_any_feature():
    ctx = AccessContext(plan=SubscriptionPlan.FREE, status=SubscriptionStatus.TRIALING, trial_ends_at=PAST)
    for feature in Feature:
        assert not can_access(ctx, feature, now=NOW), f"expected no access to {feature}"


# ── can_access — BASIC 方案 ───────────────────────────────────────────────────


def test_basic_can_publish():
    ctx = AccessContext(plan=SubscriptionPlan.BASIC, status=SubscriptionStatus.ACTIVE)
    assert can_access(ctx, Feature.PUBLISH, now=NOW)


def test_basic_can_schedule():
    ctx = AccessContext(plan=SubscriptionPlan.BASIC, status=SubscriptionStatus.ACTIVE)
    assert can_access(ctx, Feature.SCHEDULE, now=NOW)


def test_basic_cannot_access_ai_analysis():
    ctx = AccessContext(plan=SubscriptionPlan.BASIC, status=SubscriptionStatus.ACTIVE)
    assert not can_access(ctx, Feature.AI_ANALYSIS, now=NOW)


def test_basic_cannot_access_weekly_report():
    ctx = AccessContext(plan=SubscriptionPlan.BASIC, status=SubscriptionStatus.ACTIVE)
    assert not can_access(ctx, Feature.WEEKLY_REPORT, now=NOW)


# ── can_access — PRO 方案 ─────────────────────────────────────────────────────


def test_pro_can_access_all_features():
    ctx = AccessContext(plan=SubscriptionPlan.PRO, status=SubscriptionStatus.ACTIVE)
    for feature in Feature:
        assert can_access(ctx, feature, now=NOW), f"PRO should access {feature}"


# ── can_access — 取消訂閱 ─────────────────────────────────────────────────────


def test_canceled_cannot_access_any_feature():
    ctx = AccessContext(plan=SubscriptionPlan.PRO, status=SubscriptionStatus.CANCELED)
    for feature in Feature:
        assert not can_access(ctx, feature, now=NOW), f"canceled should not access {feature}"
