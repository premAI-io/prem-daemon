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
        # Prem Embeddings

        ## Description

        Prem Embeddings are all the services used to transform unstructured text in a vector representation. A vector representation is a vector of numbers that represents the most important features of the text. For example, a sentence can be represented as a vector of numbers. The vector is obtained using a neural network that is trained to extract the most important features of the sentence. Embeddings are used in many NLP tasks, such as text classification, text clustering, text similarity, and so on. In order to give memory to ChatGPT, we need to transform the text in a vector representation and store them in a vectorstore for later retrieval.

        ## Installation & Usage

        All the services compatible with Prem Embeddings interface expose an API with the following endpoints:

        - `/api/v1/embeddings/`

        Check the OpenAPI documentation at the link http://{service}:{port}/docs for more information.

        """,  # noqa E501
        "icon": "/assets/apps/embeddings.svg",
    },
    {
        "id": "store",
        "name": "Prem Store",
        "playground": False,
        "documentation": """
        # Prem Store

        ## Description

        Prem Store are all the services that expose a vector database. A vector database is used to store embeddings. An embedding is a vector representation of a piece of data. For example, a sentence can be represented as a vector of numbers. The vector is obtained using a neural network that is trained to extract the most important features of the sentence.

        ## Installation & Usage

        We don't have a standard interface for what concerns Prem Store. However, we suggest to connect with Prem Store services using Langchain python library. You can find the library [here](https://python.langchain.com/en/latest/index.html).
        """,  # noqa E501
        "icon": "/assets/apps/store.svg",
    },
    {
        "id": "copilot",
        "name": "Prem Copilot",
        "playground": False,
        "documentation": """
        # Prem Copilot

        All the services exposed using Prem Copilot interface can be used using the official Github Copilot extension. You can find the extension [here](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot).

        ## Installation

        In the `settings.json` file of your VSCode, add the following lines:

        ```json
            "github.copilot.advanced": {
            "debug.overrideEngine": "codegen",
            "debug.testOverrideProxyUrl": "http://localhost:18080",
            "debug.overrideProxyUrl": "http://localhost:18080"
        }
        ```

        > Make sure to point to the correct port of the Prem Copilot service.
        """,  # noqa E501
        "icon": "/assets/apps/copilot.svg",
    },
    {
        "id": "michelangelo",
        "name": "Prem Michelangelo",
        "playground": True,
        "documentation": """
        # Prem Michelangelo
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
    for service in SERVICES:
        service["icon"] = f"https://prem-registry.fly.dev{service['icon']}"


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
