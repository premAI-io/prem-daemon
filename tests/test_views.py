from fastapi.testclient import TestClient

from main import get_application


def test_controller() -> None:
    app = get_application()
    with TestClient(app) as client:
        response = client.get("/api/v1/services/")
        assert response.status_code == 200
