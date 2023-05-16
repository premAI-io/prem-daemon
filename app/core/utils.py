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
        "icon": "/assets/apps/chat.svg",
    },
    {
        "id": "embeddings",
        "name": "Prem Embeddings",
        "playground": False,
        "documentation": """
        # Prem Chat
        """,
        "icon": "/assets/apps/embeddings.svg",
    },
    {
        "id": "store",
        "name": "Prem Store",
        "playground": False,
        "documentation": """
        # Prem Chat
        """,
        "icon": "/assets/apps/store.svg",
    },
    {
        "id": "copilot",
        "name": "Prem Copilot",
        "playground": False,
        "documentation": """
        # Prem Chat
        """,
        "icon": "/assets/apps/copilot.svg",
    },
    {
        "id": "michelangelo",
        "name": "Prem Michelangelo",
        "playground": True,
        "documentation": """
        # Prem Chat
        """,
        "icon": "/assets/apps/michelangelo.svg",
    },
]

SERVICES = []


def get_docker_client():
    return docker.from_env()


def get_services():
    global SERVICES
    response = requests.get("https://prem-registry.fly.dev/manifests/")
    SERVICES = response.json()


def format_stats(value):
    cpu_delta = (
        value["cpu_stats"]["cpu_usage"]["total_usage"]
        - value["precpu_stats"]["cpu_usage"]["total_usage"]
    )
    system_delta = (
        value["cpu_stats"]["system_cpu_usage"]
        - value["precpu_stats"]["system_cpu_usage"]
    )
    cpu_percentage = (
        (cpu_delta / system_delta) * value["cpu_stats"]["online_cpus"] * 100
    )

    memory_usage = value["memory_stats"]["usage"] / (
        1024 * 1024
    )  # Convert bytes to MiB
    memory_limit = value["memory_stats"]["limit"] / (
        1024 * 1024 * 1024
    )  # Convert bytes to GiB
    memory_percentage = (
        memory_usage * 1024 / memory_limit
    ) * 100  # Convert MiB to GiB for percentage calculation
    return cpu_percentage, memory_usage, memory_limit, memory_percentage
