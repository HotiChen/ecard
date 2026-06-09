from pydantic import BaseModel


class SubscriptionRead(BaseModel):
    id: int
    plan: str
    status: str
    trial_ends_at: str | None
    current_period_end: str | None

    model_config = {"from_attributes": True}


class SubscriptionSeed(BaseModel):
    plan: str = "free"
    status: str = "trialing"
    trial_ends_at: str | None = None
    current_period_end: str | None = None
