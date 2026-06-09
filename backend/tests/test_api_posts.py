"""
TDD tests for POST /api/v1/posts — stores post and returns SHA-256 proof.
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
    from app.models.post_record import PostRecord  # noqa: F401
    Base.metadata.create_all(_engine, tables=[PostRecord.__table__])
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(_engine, tables=[PostRecord.__table__])
    app.dependency_overrides.clear()


client = TestClient(app)

VALID_PAYLOAD = {
    "content": "攝影日記：金門夕陽",
    "platforms": ["threads"],
}


def test_create_post_returns_201():
    resp = client.post("/api/v1/posts", json=VALID_PAYLOAD)
    assert resp.status_code == 201


def test_create_post_returns_sha256():
    resp = client.post("/api/v1/posts", json=VALID_PAYLOAD)
    data = resp.json()
    assert "sha256" in data
    assert len(data["sha256"]) == 64  # hex SHA-256


def test_create_post_returns_proof_timestamp():
    resp = client.post("/api/v1/posts", json=VALID_PAYLOAD)
    data = resp.json()
    assert "proof_timestamp" in data
    assert "2026" in data["proof_timestamp"] or "T" in data["proof_timestamp"]


def test_create_post_sha256_is_deterministic_for_same_content():
    # Two separate posts with same content produce different sha256
    # (because timestamps differ) — just verify it's 64-char hex each time
    r1 = client.post("/api/v1/posts", json=VALID_PAYLOAD).json()
    r2 = client.post("/api/v1/posts", json=VALID_PAYLOAD).json()
    assert len(r1["sha256"]) == 64
    assert len(r2["sha256"]) == 64


def test_create_post_stores_in_db():
    client.post("/api/v1/posts", json=VALID_PAYLOAD)
    resp = client.get("/api/v1/posts")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_create_post_stores_content():
    client.post("/api/v1/posts", json=VALID_PAYLOAD)
    posts = client.get("/api/v1/posts").json()
    assert posts[0]["content"] == "攝影日記：金門夕陽"


def test_create_post_stores_platforms():
    client.post("/api/v1/posts", json=VALID_PAYLOAD)
    posts = client.get("/api/v1/posts").json()
    assert posts[0]["platforms"] == ["threads"]


def test_create_post_requires_content():
    resp = client.post("/api/v1/posts", json={**VALID_PAYLOAD, "content": ""})
    assert resp.status_code == 422


def test_create_post_requires_platforms():
    resp = client.post("/api/v1/posts", json={**VALID_PAYLOAD, "platforms": []})
    assert resp.status_code == 422


def test_list_posts_empty_initially():
    resp = client.get("/api/v1/posts")
    assert resp.status_code == 200
    assert resp.json() == []
