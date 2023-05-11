import logging

import docker
import requests

logger = logging.getLogger(__name__)

APPS = [
    {"id": "chat", "name": "Prem Chat", "playground": True},
    {"id": "embeddings", "name": "Prem Embeddings", "playground": False},
    {"id": "store", "name": "Prem Store", "playground": False},
    {"id": "copilot", "name": "Prem Copilot", "playground": False},
    {"id": "michelangelo", "name": "Prem Michelangelo", "playground": True},
]

SERVICES = []


def get_docker_client():
    return docker.from_env()


def get_services():
    global SERVICES
    response = requests.get("https://prem-registry.fly.dev/manifests/")
    SERVICES = response.json()
