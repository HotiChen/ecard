"""Stripe Webhook 處理單元測試（W7）。

驗證簽章驗證（HMAC-SHA256）與事件路由邏輯。
測試用的簽章由測試自行生成，不需要真實 Stripe 帳號或網路連線。
"""

import hashlib
import hmac
import time

import pytest

from app.models.enums import SubscriptionStatus
from app.services.webhook import (
    WebhookError,
    handle_stripe_event,
    verify_stripe_signature,
)

SECRET = "whsec_test_secret"
PAYLOAD = b'{"type":"invoice.payment_succeeded"}'


def _make_sig_header(payload: bytes, secret: str, timestamp: int | None = None) -> str:
    """產生合法的 Stripe-Signature 標頭（測試用）。"""
    ts = timestamp if timestamp is not None else int(time.time())
    signed = f"{ts}.".encode() + payload
    sig = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    return f"t={ts},v1={sig}"


# ── verify_stripe_signature ───────────────────────────────────────────────────


def test_valid_signature_does_not_raise():
    header = _make_sig_header(PAYLOAD, SECRET)
    verify_stripe_signature(PAYLOAD, header, SECRET)  # 不應拋例外


def test_wrong_secret_raises_webhook_error():
    header = _make_sig_header(PAYLOAD, "wrong_secret")
    with pytest.raises(WebhookError, match="簽章"):
        verify_stripe_signature(PAYLOAD, header, SECRET)


def test_tampered_payload_raises_webhook_error():
    header = _make_sig_header(PAYLOAD, SECRET)
    with pytest.raises(WebhookError, match="簽章"):
        verify_stripe_signature(b'{"tampered":true}', header, SECRET)


def test_expired_timestamp_raises_webhook_error():
    old_ts = int(time.time()) - 600  # 10 分鐘前，超過預設 5 分鐘容差
    header = _make_sig_header(PAYLOAD, SECRET, timestamp=old_ts)
    with pytest.raises(WebhookError, match="時間"):
        verify_stripe_signature(PAYLOAD, header, SECRET)


def test_missing_v1_signature_raises_webhook_error():
    header = f"t={int(time.time())}"  # 沒有 v1=
    with pytest.raises(WebhookError):
        verify_stripe_signature(PAYLOAD, header, SECRET)


# ── handle_stripe_event ───────────────────────────────────────────────────────


def test_payment_succeeded_sets_active():
    update = handle_stripe_event(
        "invoice.payment_succeeded",
        {"subscription": "sub_abc", "status": "paid"},
    )
    assert update is not None
    assert update.stripe_subscription_id == "sub_abc"
    assert update.new_status == SubscriptionStatus.ACTIVE


def test_payment_failed_sets_past_due():
    update = handle_stripe_event(
        "invoice.payment_failed",
        {"subscription": "sub_xyz", "status": "open"},
    )
    assert update is not None
    assert update.stripe_subscription_id == "sub_xyz"
    assert update.new_status == SubscriptionStatus.PAST_DUE


def test_subscription_deleted_sets_canceled():
    update = handle_stripe_event(
        "customer.subscription.deleted",
        {"id": "sub_del"},
    )
    assert update is not None
    assert update.stripe_subscription_id == "sub_del"
    assert update.new_status == SubscriptionStatus.CANCELED


def test_unknown_event_returns_none():
    update = handle_stripe_event("some.unknown.event", {})
    assert update is None
