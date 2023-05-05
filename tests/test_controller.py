from fastapi.testclient import TestClient

from main import get_application


def test_get_models() -> None:
    app = get_application()
    with TestClient(app) as client:
        response = client.get("/api/v1/models/")
        assert response.status_code == 200
