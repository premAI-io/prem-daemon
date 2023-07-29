from fastapi.testclient import TestClient

from main import get_application


class TestController:
    def setup_method(self):
        app = get_application()
        [event() for event in app.router.on_startup]
        self.client = TestClient(app)

    def test_get_registries(self) -> None:
        response = self.client.get("/v1/registries/")
        assert response.status_code == 200

    def test_add_registry(self) -> None:
        response = self.client.get("/v1/services/")
        assert response.status_code == 200
        number_of_services = len(response.json())

        response = self.client.post(
            "/v1/registries/",
            json={
                "url": "https://raw.githubusercontent.com/premAI-io/prem-daemon/main/resources/mocks/manifests.json"
            },
        )
        assert response.status_code == 200

        response = self.client.get("/v1/services/")
        assert response.status_code == 200
        assert len(response.json()) > number_of_services

    def test_delete_registry(self) -> None:
        response = self.client.post(
            "/v1/registries/",
            json={
                "url": "https://raw.githubusercontent.com/premAI-io/prem-daemon/main/resources/mocks/manifests.json"
            },
        )
        assert response.status_code == 200

        response = self.client.get("/v1/services/")
        assert response.status_code == 200
        number_of_services = len(response.json())

        response = self.client.get("/v1/registries/")
        assert response.status_code == 200
        number_of_registries = len(response.json())

        response = self.client.post(
            "/v1/delete-registry/",
            json={
                "url": "https://raw.githubusercontent.com/premAI-io/prem-daemon/main/resources/mocks/manifests.json"
            },
        )
        assert response.status_code == 200

        response = self.client.get("/v1/services/")
        assert response.status_code == 200
        assert len(response.json()) < number_of_services

        response = self.client.get("/v1/registries/")
        assert response.status_code == 200
        assert len(response.json()) < number_of_registries

    def test_add_custom_service(self) -> None:
        response = self.client.get("/v1/services/")
        assert response.status_code == 200
        number_of_services = len(response.json())

        response = self.client.post(
            "/v1/services/",
            json={
                "id": "whisper-tiny-mock",
                "name": "Whisper Tiny Mock",
                "interfaces": ["audio-to-text"],
                "modelInfo": {},
                "dockerImages": {
                    "cpu": {
                        "size": 5565095283,
                        "image": "ghcr.io/premai-io/audio-to-text-whisper-tiny-cpu:1.0.1",
                    }
                },
                "defaultPort": 8000,
                "defaultExternalPort": 10111,
            },
        )
        assert response.status_code == 200

        response = self.client.get("/v1/services/")
        assert response.status_code == 200
        assert len(response.json()) == number_of_services + 1
