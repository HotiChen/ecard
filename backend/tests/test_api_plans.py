"""TDD tests for GET /api/v1/plans — static pricing data, no DB needed."""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_plans_returns_200():
    resp = client.get("/api/v1/plans")
    assert resp.status_code == 200


def test_list_plans_returns_list():
    data = client.get("/api/v1/plans").json()
    assert isinstance(data, list)


def test_list_plans_has_three_plans():
    data = client.get("/api/v1/plans").json()
    assert len(data) == 3


def test_plans_have_required_fields():
    plans = client.get("/api/v1/plans").json()
    for plan in plans:
        assert "id" in plan
        assert "name" in plan
        assert "price_twd" in plan
        assert "features" in plan


def test_free_plan_price_is_zero():
    plans = {p["id"]: p for p in client.get("/api/v1/plans").json()}
    assert plans["free"]["price_twd"] == 0


def test_basic_plan_price():
    plans = {p["id"]: p for p in client.get("/api/v1/plans").json()}
    assert plans["basic"]["price_twd"] == 390


def test_pro_plan_price():
    plans = {p["id"]: p for p in client.get("/api/v1/plans").json()}
    assert plans["pro"]["price_twd"] == 990


def test_plans_features_are_lists():
    plans = client.get("/api/v1/plans").json()
    for plan in plans:
        assert isinstance(plan["features"], list)


def test_pro_plan_has_more_features_than_basic():
    plans = {p["id"]: p for p in client.get("/api/v1/plans").json()}
    assert len(plans["pro"]["features"]) >= len(plans["basic"]["features"])
