import pytest

# Skip cleanly when the optional API stack (fastapi + its HTTP test client) is absent.
testclient = pytest.importorskip("fastapi.testclient")
api = pytest.importorskip("screenshot_action.api")

client = testclient.TestClient(api.app)


def test_api_health_and_text_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["version"]

    response = client.post(
        "/analyze/text",
        json={"text": "Assignment due tomorrow at 8 PM", "reference_date": "2026-09-24"},
    )
    assert response.status_code == 200
    assert response.json()["entities"]["date_iso"] == "2026-09-25"


def test_api_version_matches_package():
    import screenshot_action

    assert client.get("/health").json()["version"] == screenshot_action.__version__


def test_api_blank_text_is_a_client_error_not_a_crash():
    response = client.post("/analyze/text", json={"text": "   "})
    assert response.status_code == 422
    assert "empty" in response.json()["detail"]


def test_api_rejects_invalid_reference_date_and_missing_text():
    bad_date = client.post("/analyze/text", json={"text": "x", "reference_date": "nope"})
    assert bad_date.status_code == 422
    assert client.post("/analyze/text", json={}).status_code == 422
