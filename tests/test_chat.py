import os

from fastapi.testclient import TestClient

from main import get_application


def test_chat_completions_llam_cpp() -> None:
    os.environ["MODEL_ID"] = "ggml-vicuna-7b-1.1-q4_2"

    app = get_application()
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/chat/completions",
            json={
                "model": "ggml-vicuna-7b-1.1-q4_2",
                "messages": [{"role": "user", "content": "Hello!"}],
            },
        )
        assert response.status_code == 200
