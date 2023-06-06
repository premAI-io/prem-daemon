from fastapi.testclient import TestClient

from main import get_application


class TestController:
    def setup_method(self):
        app = get_application()
        [event() for event in app.router.on_startup]
        self.client = TestClient(app)

    def test_interfaces(self) -> None:
        response = self.client.get("/v1/interfaces/")
        assert response.status_code == 200

    def test_services(self) -> None:
        response = self.client.get("/v1/services/")
        assert response.status_code == 200

    def test_service_by_id(self) -> None:
        response = self.client.get("/v1/services/vicuna-7b-q4")
        assert response.status_code == 200

    def test_services_by_interface(self) -> None:
        response = self.client.get("/v1/services-by-interface/chat")
        assert response.status_code == 200

    def test_download_remove_service(self) -> None:
        response = self.client.get("/v1/download-service/redis-vector-db")
        assert response.status_code == 200

        response = self.client.get("/v1/download-service-stream/redis-vector-db")
        assert response.status_code == 200

        response = self.client.get("/v1/remove-service/redis-vector-db")
        assert response.status_code == 200

    def test_run_stop_service(self) -> None:
        response = self.client.get("/v1/download-service/redis-vector-db")
        assert response.status_code == 200

        response = self.client.post(
            "/v1/run-service/",
            json={"id": "redis-vector-db"},
        )
        assert response.status_code == 200

        response = self.client.get("/v1/services/redis-vector-db")
        assert response.status_code == 200

        response = self.client.get("/v1/stop-service/redis-vector-db")
        assert response.status_code == 200

        response = self.client.post(
            "/v1/run-service/",
            json={"id": "redis-vector-db"},
        )
        assert response.status_code == 200

        response = self.client.get("/v1/stop-service/redis-vector-db")
        assert response.status_code == 200

        response = self.client.get("/v1/remove-volume/prem-redis-vector-db-data")
        assert response.status_code == 200

    def test_run_stop_all_services(self) -> None:
        response = self.client.get("/v1/download-service/redis-vector-db")
        assert response.status_code == 200

        response = self.client.post(
            "/v1/run-service/",
            json={"id": "redis-vector-db"},
        )
        assert response.status_code == 200

        response = self.client.get("/v1/services/redis-vector-db")
        assert response.status_code == 200

        response = self.client.get("/v1/stop-all-services/")
        assert response.status_code == 200

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
