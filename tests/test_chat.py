import os
from fastapi.testclient import TestClient

from main import get_application


def test_chat_completions_gpt4all_j() -> None:
    os.environ["MODEL_ID"] = "gpt4all-j-v1.3-groovy"

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


def test_chat_completions_llam_cpp() -> None:
    os.environ["MODEL_ID"] = "gpt4all-lora-quantized-ggml"

    app = get_application()
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/chat/completions",
            json={
                "model": "gpt4all-lora-quantized-ggml",
                "messages": [{"role": "user", "content": "Hello!"}],
            },
        )
        assert response.status_code == 200
