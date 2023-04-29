from fastapi.testclient import TestClient

from main import get_application


def test_chat_completions() -> None:
    app = get_application()
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/chat/completions",
            json={
                "model": "gpt4all-j-v1.3-groovy",
                "messages": [{"role": "user", "content": "Hello!"}],
            },
        )
        assert response.status_code == 200
