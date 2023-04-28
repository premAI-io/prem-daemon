from fastapi.testclient import TestClient

from main import get_application


def test_predict_verbatim() -> None:
    app = get_application()
    with TestClient(app) as client:
        response = client.post(
            "/api/predict-verbatim",
            json={"texts": ["The service was good."], "language": "en"},
        )
        assert response.status_code == 200
        assert response.json()["input"] == ["The service was good."]
        assert len(response.json()["predictions"]) == 1
        assert len(response.json()["probabilities"]) == 1
        assert len(response.json()["classes"]) == 3