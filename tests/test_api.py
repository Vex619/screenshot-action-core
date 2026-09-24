import pytest


def test_api_health_and_text_endpoint():
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from screenshot_action.api import app

    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    response = TestClient(app).post(
        "/analyze/text",
        json={"text": "Assignment due tomorrow at 8 PM", "reference_date": "2026-09-24"},
    )
    assert response.status_code == 200
    assert response.json()["entities"]["date_iso"] == "2026-09-25"
