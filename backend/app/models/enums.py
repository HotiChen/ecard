"""跨模型共用的列舉型別。"""

import enum


class Platform(str, enum.Enum):
    THREADS = "threads"
    INSTAGRAM = "instagram"
    X = "x"


class PostStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"


class SubscriptionPlan(str, enum.Enum):
    FREE = "free"          # 14 天試用
    BASIC = "basic"        # NT$390 / 月
    PRO = "pro"            # NT$990 / 月


class SubscriptionStatus(str, enum.Enum):
    TRIALING = "trialing"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
