import os
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from main import get_application


@pytest.fixture
def client():
    app = get_application()
    [event() for event in app.router.on_startup]
    return TestClient(app)


@pytest.fixture
def multiple_registries_client():
    os.environ["PREM_REGISTRY_URL"] = " ".join(
        (
            "https://raw.githubusercontent.com/premAI-io/prem-registry/main/manifests.json",
            "https://raw.githubusercontent.com/premAI-io/prem-daemon/main/resources/mocks/manifests.json",
        )
    )
    app = get_application()
    [event() for event in app.router.on_startup]
    return TestClient(app)


class TestController:
    def test_get_registries(self, client) -> None:
        response = client.get("/v1/registries/")
        assert response.status_code == HTTPStatus.OK

    def test_add_registry(self, client) -> None:
        response = client.get("/v1/services/")
        assert response.status_code == HTTPStatus.OK
        number_of_services = len(response.json())

        response = client.post(
            "/v1/registries/",
            json={
                "url": "https://raw.githubusercontent.com/premAI-io/prem-daemon/main/resources/mocks/manifests.json"
            },
        )
        assert response.status_code == HTTPStatus.OK

        response = client.get("/v1/services/")
        assert response.status_code == HTTPStatus.OK
        services = response.json()
        assert len(services) > number_of_services
        assert len(services) == len({service["id"] for service in services})

    def test_delete_registry(self, client) -> None:
        response = client.get("/v1/services/")
        assert response.status_code == HTTPStatus.OK
        number_of_services = len(response.json())

        response = client.get("/v1/registries/")
        assert response.status_code == HTTPStatus.OK
        number_of_registries = len(response.json())

        response = client.delete(
            "/v1/registries/",
            params={
                "url": "https://raw.githubusercontent.com/premAI-io/prem-daemon/main/resources/mocks/manifests.json"
            },
        )
        assert response.status_code == HTTPStatus.OK

        response = client.get("/v1/services/")
        assert response.status_code == HTTPStatus.OK
        assert len(response.json()) < number_of_services

        response = client.get("/v1/registries/")
        assert response.status_code == HTTPStatus.OK
        assert len(response.json()) < number_of_registries

        response = client.post(
            "/v1/registries/",
            json={
                "url": "https://raw.githubusercontent.com/premAI-io/prem-daemon/main/resources/mocks/manifests.json"
            },
        )
        assert response.status_code == HTTPStatus.OK

    def test_add_custom_service(self, client) -> None:
        response = client.get("/v1/services/")
        assert response.status_code == HTTPStatus.OK
        number_of_services = len(response.json())

        response = client.post(
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
        assert response.status_code == HTTPStatus.OK

        response = client.get("/v1/services/")
        assert response.status_code == HTTPStatus.OK
        assert len(response.json()) == number_of_services + 1

    def test_add_existing_service(self, client) -> None:
        response = client.get("/v1/services/")
        assert response.status_code == HTTPStatus.OK
        number_of_services = len(response.json())

        response = client.post(
            "/v1/services/",
            json=response.json()[-1],
        )
        assert response.status_code != HTTPStatus.OK

        response = client.get("/v1/services/")
        assert response.status_code == HTTPStatus.OK
        assert len(response.json()) == number_of_services

    def test_multiple_registries(self, multiple_registries_client):
        response = multiple_registries_client.get("/v1/registries/")
        assert response.status_code == HTTPStatus.OK
        assert len(response.json()) == 2
