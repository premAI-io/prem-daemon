from fastapi.testclient import TestClient

from main import get_application


class TestController:
    def setup_method(self):
        app = get_application()
        [event() for event in app.router.on_startup]
        self.client = TestClient(app)

    def test_stats(self) -> None:
        response = self.client.get("/v1/stop-service/redis-vector-db")

        response = self.client.get("/v1/download-service/redis-vector-db")
        assert response.status_code == 200

        response = self.client.post(
            "/v1/run-service/",
            json={"id": "redis-vector-db"},
        )
        assert response.status_code == 200

        response = self.client.get("/v1/stats/")
        assert response.status_code == 200

        response = self.client.get("/v1/stats-all/")
        assert response.status_code == 200

        response = self.client.get("/v1/gpu-stats-all/")
        assert response.status_code == 200

        response = self.client.get("/v1/stop-service/redis-vector-db")
        assert response.status_code == 200

    def test_stats_by_service(self) -> None:
        response = self.client.get("/v1/stop-service/redis-vector-db")

        response = self.client.get("/v1/download-service/redis-vector-db")
        assert response.status_code == 200

        response = self.client.post(
            "/v1/run-service/",
            json={"id": "redis-vector-db"},
        )
        assert response.status_code == 200

        response = self.client.get("/v1/stats/redis-vector-db")
        assert response.status_code == 200

        response = self.client.get("/v1/stop-service/redis-vector-db")
        assert response.status_code == 200
