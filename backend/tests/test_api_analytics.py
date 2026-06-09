"""
TDD tests for /api/v1/analytics/metrics endpoint.
Uses SQLite in-memory + StaticPool — no real DB needed.
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
    from app.models.metric_record import MetricRecord  # noqa: F401
    Base.metadata.create_all(_engine, tables=[MetricRecord.__table__])
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(_engine, tables=[MetricRecord.__table__])
    app.dependency_overrides.clear()


client = TestClient(app)

METRIC_PAYLOAD = {
    "post_id": 1,
    "platform": "threads",
    "likes": 120,
    "comments": 30,
    "replies": 10,
    "reposts": 5,
    "views": 1000,
}


def test_list_metrics_empty_initially():
    resp = client.get("/api/v1/analytics/metrics")
    assert resp.status_code == 200
    assert resp.json() == []


def test_record_metric_returns_201():
    resp = client.post("/api/v1/analytics/metrics", json=METRIC_PAYLOAD)
    assert resp.status_code == 201


def test_record_metric_stores_likes():
    resp = client.post("/api/v1/analytics/metrics", json=METRIC_PAYLOAD)
    assert resp.json()["likes"] == 120


def test_record_metric_stores_platform():
    resp = client.post("/api/v1/analytics/metrics", json=METRIC_PAYLOAD)
    assert resp.json()["platform"] == "threads"


def test_record_metric_appears_in_list():
    client.post("/api/v1/analytics/metrics", json=METRIC_PAYLOAD)
    resp = client.get("/api/v1/analytics/metrics")
    assert len(resp.json()) == 1
    assert resp.json()[0]["post_id"] == 1


def test_list_metrics_multiple_entries():
    client.post("/api/v1/analytics/metrics", json=METRIC_PAYLOAD)
    client.post("/api/v1/analytics/metrics", json={**METRIC_PAYLOAD, "platform": "instagram", "likes": 80})
    resp = client.get("/api/v1/analytics/metrics")
    assert len(resp.json()) == 2


def test_filter_metrics_by_post_id():
    client.post("/api/v1/analytics/metrics", json=METRIC_PAYLOAD)
    client.post("/api/v1/analytics/metrics", json={**METRIC_PAYLOAD, "post_id": 2, "likes": 5})
    resp = client.get("/api/v1/analytics/metrics?post_id=1")
    data = resp.json()
    assert len(data) == 1
    assert data[0]["post_id"] == 1


def test_filter_metrics_by_platform():
    client.post("/api/v1/analytics/metrics", json=METRIC_PAYLOAD)
    client.post("/api/v1/analytics/metrics", json={**METRIC_PAYLOAD, "platform": "instagram"})
    resp = client.get("/api/v1/analytics/metrics?platform=instagram")
    data = resp.json()
    assert len(data) == 1
    assert data[0]["platform"] == "instagram"


def test_record_metric_requires_valid_platform():
    resp = client.post("/api/v1/analytics/metrics", json={**METRIC_PAYLOAD, "platform": "tiktok"})
    assert resp.status_code == 422
