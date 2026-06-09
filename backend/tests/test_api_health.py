"""FastAPI 後端環境整合測試（W2）。

使用 TestClient 驗證 app 可正常啟動、路由正確、health endpoint 回傳預期格式。
不依賴真實資料庫或外部服務。
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_app_info():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["app"] == "PhotoFlow AI"
    assert "docs" in data
    assert "health" in data


def test_health_returns_200():
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200


def test_health_status_is_ok():
    resp = client.get("/api/v1/health")
    assert resp.json()["status"] == "ok"


def test_health_includes_env():
    resp = client.get("/api/v1/health")
    assert "env" in resp.json()


def test_health_includes_version():
    resp = client.get("/api/v1/health")
    data = resp.json()
    assert "version" in data
    assert data["version"] == "0.1.0"
