from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_sections():
    response = client.get("/browse/sections/1")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search():
    response = client.get("/browse/search?q=battery")

    assert response.status_code == 200
    assert len(response.json()) > 0


def test_generation():
    response = client.get("/generation/1")

    assert response.status_code == 200

    data = response.json()

    assert "test_cases" in data
    assert len(data["test_cases"]) == 5


def test_stale():
    response = client.get("/stale/1")

    assert response.status_code == 200

    data = response.json()

    assert "stale" in data