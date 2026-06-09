"""
TDD tests for /api/v1/subscription endpoint.
Uses SQLite in-memory + StaticPool.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.main import app
from app.db.session import get_db

_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_Session = sessionmaker(bind=_engine, autoflush=False, expire_on_commit=False)


def override_get_db():
    db = _Session()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    from app.models.subscription_record import SubscriptionRecord  # noqa: F401
    Base.metadata.create_all(_engine, tables=[SubscriptionRecord.__table__])
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(_engine, tables=[SubscriptionRecord.__table__])
    app.dependency_overrides.clear()


client = TestClient(app)


def _seed(plan="pro", status="active", trial_ends_at=None, current_period_end="2026-07-09"):
    return client.post(
        "/api/v1/subscription/_seed",
        json={"plan": plan, "status": status,
              "trial_ends_at": trial_ends_at,
              "current_period_end": current_period_end},
    )


def test_get_subscription_404_when_none():
    resp = client.get("/api/v1/subscription")
    assert resp.status_code == 404


def test_seed_creates_subscription():
    resp = _seed()
    assert resp.status_code == 201


def test_get_subscription_returns_plan():
    _seed(plan="pro")
    data = client.get("/api/v1/subscription").json()
    assert data["plan"] == "pro"


def test_get_subscription_returns_status():
    _seed(status="active")
    data = client.get("/api/v1/subscription").json()
    assert data["status"] == "active"


def test_get_subscription_returns_trial_info():
    _seed(plan="free", status="trialing", trial_ends_at="2026-06-23")
    data = client.get("/api/v1/subscription").json()
    assert data["status"] == "trialing"
    assert "2026-06-23" in data["trial_ends_at"]


def test_cancel_subscription_sets_canceled():
    _seed()
    resp = client.post("/api/v1/subscription/cancel")
    assert resp.status_code == 200
    assert resp.json()["status"] == "canceled"


def test_cancel_reflects_in_get():
    _seed()
    client.post("/api/v1/subscription/cancel")
    data = client.get("/api/v1/subscription").json()
    assert data["status"] == "canceled"


def test_cancel_when_no_subscription_returns_404():
    resp = client.post("/api/v1/subscription/cancel")
    assert resp.status_code == 404
