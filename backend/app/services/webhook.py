"""Stripe Webhook 處理。

兩個核心函式，純邏輯無網路呼叫，可獨立單元測試：
  - verify_stripe_signature: HMAC-SHA256 簽章驗證（同 Stripe 官方演算法）
  - handle_stripe_event:     事件類型 → 訂閱狀態更新 mapping

Stripe Signature 格式：
  Stripe-Signature: t=<timestamp>,v1=<hmac_sha256(secret, "{ts}.{payload}")>
"""

import hashlib
import hmac
import time
from dataclasses import dataclass

from app.models.enums import SubscriptionStatus

SIGNATURE_TOLERANCE_SECONDS = 300  # 5 分鐘容差


class WebhookError(Exception):
    pass


@dataclass
class SubscriptionUpdate:
    stripe_subscription_id: str
    new_status: SubscriptionStatus


def verify_stripe_signature(
    payload: bytes,
    sig_header: str,
    secret: str,
    now: int | None = None,
    tolerance: int = SIGNATURE_TOLERANCE_SECONDS,
) -> None:
    """驗證 Stripe-Signature 標頭，不合法時拋出 WebhookError。"""
    if now is None:
        now = int(time.time())

    # 解析 t= 與 v1=
    parts = {k: v for k, v in (p.split("=", 1) for p in sig_header.split(",") if "=" in p)}
    if "t" not in parts or "v1" not in parts:
        raise WebhookError("Stripe-Signature 標頭格式錯誤：缺少 t 或 v1 欄位")

    try:
        timestamp = int(parts["t"])
    except ValueError:
        raise WebhookError("Stripe-Signature 中的時間戳記無法解析")

    if abs(now - timestamp) > tolerance:
        raise WebhookError(f"Webhook 時間戳記已過期（容差 {tolerance} 秒）")

    signed = f"{timestamp}.".encode() + payload
    expected = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected, parts["v1"]):
        raise WebhookError("Webhook 簽章驗證失敗：簽章不符")


def handle_stripe_event(
    event_type: str,
    event_data: dict,
) -> SubscriptionUpdate | None:
    """將 Stripe 事件對應到訂閱狀態更新，不認識的事件回傳 None。"""
    if event_type == "invoice.payment_succeeded":
        return SubscriptionUpdate(
            stripe_subscription_id=event_data["subscription"],
            new_status=SubscriptionStatus.ACTIVE,
        )
    if event_type == "invoice.payment_failed":
        return SubscriptionUpdate(
            stripe_subscription_id=event_data["subscription"],
            new_status=SubscriptionStatus.PAST_DUE,
        )
    if event_type == "customer.subscription.deleted":
        return SubscriptionUpdate(
            stripe_subscription_id=event_data["id"],
            new_status=SubscriptionStatus.CANCELED,
        )
    return None
