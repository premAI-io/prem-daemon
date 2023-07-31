import logging
import subprocess
import xml.etree.ElementTree as ET

import docker
import requests
import torch

from app.core import config

logger = logging.getLogger(__name__)

SERVICES = []
REGISTRIES = config.PREM_REGISTRY_URL.strip().split()
INTERFACES = [
    {
        "id": "chat",
        "name": "Chat",
        "playground": True,
        "documentation": """
# Chat
        """,
        "icon": "/assets/apps/chat.svg",
    },
    {
        "id": "embeddings",
        "name": "Embeddings",
        "playground": False,
        "documentation": """
# Embeddings

## Description

Embeddings are all the services used to transform unstructured text in a vector representation. A vector representation is a vector of numbers that represents the most important features of the text. For example, a sentence can be represented as a vector of numbers. The vector is obtained using a neural network that is trained to extract the most important features of the sentence. Embeddings are used in many NLP tasks, such as text classification, text clustering, text similarity, and so on. In order to give memory to ChatGPT, we need to transform the text in a vector representation and store them in a vectorstore for later retrieval.

All the services compatible with Prem Embeddings interface expose an API that can be used directly with Langchain python library. You can find the library [here](https://python.langchain.com/en/latest/index.html).

## Getting Started

```python
import os

from langchain.embeddings import OpenAIEmbeddings

os.environ["OPENAI_API_KEY"] = "random-string"

# assuming the service is running on localhost
embeddings = OpenAIEmbeddings(openai_api_base="http://localhost:8000/api/v1")

text = "Prem is an easy to use open source AI platform."
query_result = embeddings.embed_query(text)
doc_result = embeddings.embed_documents([text])
```

""",  # noqa E501
        "icon": "/assets/apps/embeddings.svg",
    },
    {
        "id": "vector-store",
        "name": "Vector Store",
        "playground": False,
        "documentation": """
# Vector Store

## Description

Vector Store are all the services that expose a vector database. A vector database is used to store embeddings. An embedding is a vector representation of a piece of data. For example, a sentence can be represented as a vector of numbers. The vector is obtained using a neural network that is trained to extract the most important features of the sentence.

## Installation & Usage

We don't have a standard interface for what concerns Prem Store. However, we suggest to connect to the services using [Langchain](https://python.langchain.com/en/latest/index.html) python library or [Llama Index](https://gpt-index.readthedocs.io/en/latest/index.html).
""",  # noqa E501
        "icon": "/assets/apps/store.svg",
    },
    {
        "id": "coder",
        "name": "Coder",
        "playground": False,
        "documentation": """
# Coder

## Installation

In order to use Coder, you will need to use Tabby extension. You can find the extension [here](https://marketplace.visualstudio.com/items?itemName=TabbyML.vscode-tabby).

When the service is running and the extension installed, you can use the command: `Tabby: Set URL of Tabby Server` to connect the extension to your service.

> We plan to support the official Github Copilot extension in the future.

""",  # noqa E501
        "icon": "/assets/apps/coder.svg",
    },
    {
        "id": "diffuser",
        "name": "Diffuser",
        "playground": True,
        "documentation": """
        # Prem Diffuser
        """,
        "icon": "/assets/apps/diffuser.svg",
    },
    {
        "id": "upscaler",
        "name": "Upscaler",
        "playground": True,
        "documentation": """
        # Prem Upscaler
        """,
        "icon": "/assets/apps/upscaler.svg",
    },
    {
        "id": "text-to-audio",
        "name": "Text to Audio",
        "playground": True,
        "documentation": """
        # Prem Text to Audio
        """,
        "icon": "/assets/apps/tta.svg",
    },
    {
        "id": "audio-to-text",
        "name": "Audio to Text",
        "playground": True,
        "documentation": """
        # Prem Audio to Text
        """,
        "icon": "/assets/apps/att.svg",
    },
]


def get_docker_client():
    return docker.from_env()


def is_gpu_available() -> bool:
    return torch.cuda.is_available()


def add_services_from_registry(url: str):
    global SERVICES
    response = requests.get(url)

    service_ids = [service["id"] for service in SERVICES]
    for service in response.json():
        if service["id"] not in service_ids:
            SERVICES.append(service)


def delete_services_from_registry(url: str):
    global SERVICES
    response = requests.get(url)

    service_ids_to_remove = {service["id"] for service in response.json()}
    SERVICES = [
        service for service in SERVICES if service["id"] not in service_ids_to_remove
    ]


def get_interfaces():
    return INTERFACES


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

    memory_usage = round(value["memory_stats"]["usage"] / (1024 * 1024), 2)
    memory_limit = round(value["memory_stats"]["limit"] / (1024 * 1024), 2)
    memory_percentage = round(memory_usage / memory_limit, 2) * 100
    return cpu_percentage, memory_usage, memory_limit, memory_percentage


def get_gpu_info():
    nvidia_smi_xml = subprocess.check_output(["nvidia-smi", "-q", "-x"]).decode()

    root = ET.fromstring(nvidia_smi_xml)

    gpu = root.find("gpu")

    gpu_name = gpu.find("product_name").text
    total_memory = gpu.find("fb_memory_usage/total").text
    used_memory = gpu.find("fb_memory_usage/used").text

    total_memory_value = int(total_memory[:-4])
    used_memory_value = int(used_memory[:-4])

    mem_percentage = (used_memory_value / total_memory_value) * 100

    return gpu_name, total_memory_value, used_memory_value, mem_percentage
