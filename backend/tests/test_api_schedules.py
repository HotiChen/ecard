"""
TDD tests for /api/v1/schedules endpoint.
Uses SQLite in-memory with get_db override — no real DB needed.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.main import app
from app.db.session import get_db

# StaticPool forces all sessions to reuse the same in-memory connection
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
    """Create tables before each test, drop after."""
    # Only import models needed for this endpoint to avoid JSONB issues
    from app.models.schedule_entry import ScheduleEntry  # noqa: F401
    Base.metadata.create_all(_engine, tables=[ScheduleEntry.__table__])
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(_engine, tables=[ScheduleEntry.__table__])
    app.dependency_overrides.clear()


client = TestClient(app)

VALID_PAYLOAD = {
    "content": "攝影日記",
    "platforms": ["threads"],
    "scheduled_at": "2026-07-01T09:00:00",
}


def test_create_schedule_returns_201():
    resp = client.post("/api/v1/schedules", json=VALID_PAYLOAD)
    assert resp.status_code == 201


def test_create_schedule_returns_id():
    resp = client.post("/api/v1/schedules", json=VALID_PAYLOAD)
    data = resp.json()
    assert "id" in data
    assert isinstance(data["id"], int)


def test_create_schedule_stores_content():
    resp = client.post("/api/v1/schedules", json=VALID_PAYLOAD)
    assert resp.json()["content"] == "攝影日記"


def test_create_schedule_stores_platforms():
    resp = client.post("/api/v1/schedules", json=VALID_PAYLOAD)
    assert resp.json()["platforms"] == ["threads"]


def test_create_schedule_is_not_canceled():
    resp = client.post("/api/v1/schedules", json=VALID_PAYLOAD)
    assert resp.json()["is_canceled"] is False


def test_list_schedules_empty_initially():
    resp = client.get("/api/v1/schedules")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_schedules_shows_created_entry():
    client.post("/api/v1/schedules", json=VALID_PAYLOAD)
    resp = client.get("/api/v1/schedules")
    assert len(resp.json()) == 1
    assert resp.json()[0]["content"] == "攝影日記"


def test_cancel_schedule_sets_flag():
    created = client.post("/api/v1/schedules", json=VALID_PAYLOAD).json()
    resp = client.post(f"/api/v1/schedules/{created['id']}/cancel")
    assert resp.status_code == 200
    assert resp.json()["is_canceled"] is True


def test_cancel_nonexistent_returns_404():
    resp = client.post("/api/v1/schedules/9999/cancel")
    assert resp.status_code == 404


def test_create_requires_content():
    resp = client.post("/api/v1/schedules", json={**VALID_PAYLOAD, "content": ""})
    assert resp.status_code == 422


def test_create_requires_platforms():
    resp = client.post("/api/v1/schedules", json={**VALID_PAYLOAD, "platforms": []})
    assert resp.status_code == 422
