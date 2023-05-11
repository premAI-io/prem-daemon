import logging

import docker
import requests

logger = logging.getLogger(__name__)

APPS = [
    {
        "id": "chat",
        "name": "Prem Chat",
        "playground": True,
        "documentation": """
        # Prem Chat
        """,
    },
    {
        "id": "embeddings",
        "name": "Prem Embeddings",
        "playground": False,
        "documentation": """
        # Prem Chat
        """,
    },
    {
        "id": "store",
        "name": "Prem Store",
        "playground": False,
        "documentation": """
        # Prem Chat
        """,
    },
    {
        "id": "copilot",
        "name": "Prem Copilot",
        "playground": False,
        "documentation": """
        # Prem Chat
        """,
    },
    {
        "id": "michelangelo",
        "name": "Prem Michelangelo",
        "playground": True,
        "documentation": """
        # Prem Chat
        """,
    },
]

SERVICES = []


def get_docker_client():
    return docker.from_env()


def get_services():
    global SERVICES
    response = requests.get("https://prem-registry.fly.dev/manifests/")
    SERVICES = response.json()
