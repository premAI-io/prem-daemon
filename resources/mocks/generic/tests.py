from fastapi.testclient import TestClient

from main import get_application


def test_chat_and_embeddings() -> None:
    app = get_application()
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/chat/completions",
            json={
                "model": "vicuna-7b-q4",
                "messages": [{"role": "user", "content": "Hello!"}],
            },
        )
        assert response.status_code == 200

        response = client.post(
            "/api/v1/embeddings",
            json={
                "model": "vicuna-7b-q4",
                "input": "Hello!",
            },
        )
        assert response.status_code == 200
