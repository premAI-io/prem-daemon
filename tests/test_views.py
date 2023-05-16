from fastapi.testclient import TestClient

from main import get_application


class TestController:
    def setup_method(self):
        app = get_application()
        [event() for event in app.router.on_startup]
        self.client = TestClient(app)

    def test_apps(self) -> None:
        response = self.client.get("/api/v1/apps/")
        assert response.status_code == 200

    def test_services(self) -> None:
        response = self.client.get("/api/v1/services/")
        assert response.status_code == 200

    def test_service_by_id(self) -> None:
        response = self.client.get("/api/v1/services/vicuna-7b-q4")
        assert response.status_code == 200

    def test_services_by_app(self) -> None:
        response = self.client.get("/api/v1/services-by-app/chat")
        assert response.status_code == 200

    def test_download_remove_service(self) -> None:
        response = self.client.get("/api/v1/download-service/redis")
        assert response.status_code == 200

        response = self.client.get("/api/v1/remove-service/redis")
        assert response.status_code == 200

    def test_run_stop_service(self) -> None:
        response = self.client.post(
            "/api/v1/run-service/",
            json={"id": "redis"},
        )
        assert response.status_code == 200

        response = self.client.get("/api/v1/stop-service/redis")
        assert response.status_code == 200

        response = self.client.post(
            "/api/v1/run-service/",
            json={"id": "redis"},
        )
        assert response.status_code == 200

        response = self.client.get("/api/v1/stop-service/redis")
        assert response.status_code == 200

    def test_stats(self) -> None:
        response = self.client.get("/api/v1/stop-service/redis")

        response = self.client.post(
            "/api/v1/run-service/",
            json={"id": "redis"},
        )
        assert response.status_code == 200

        response = self.client.get("/api/v1/stats/")
        assert response.status_code == 200

        response = self.client.get("/api/v1/stop-service/redis")
        assert response.status_code == 200

    def test_stats_by_service(self) -> None:
        response = self.client.post(
            "/api/v1/run-service/",
            json={"id": "redis"},
        )
        assert response.status_code == 200

        response = self.client.get("/api/v1/stats/redis")
        assert response.status_code == 200

        response = self.client.get("/api/v1/stop-service/redis")
        assert response.status_code == 200
