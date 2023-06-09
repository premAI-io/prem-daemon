import logging
import subprocess
import xml.etree.ElementTree as ET

import docker
import requests
import torch

from app.core.config import PREM_REGISTRY_URL

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
        "id": "store",
        "name": "Prem Store",
        "playground": False,
        "documentation": """
# Prem Store

## Description

Prem Store are all the services that expose a vector database. A vector database is used to store embeddings. An embedding is a vector representation of a piece of data. For example, a sentence can be represented as a vector of numbers. The vector is obtained using a neural network that is trained to extract the most important features of the sentence.

## Installation & Usage

We don't have a standard interface for what concerns Prem Store. However, we suggest to connect to the services using [Langchain](https://python.langchain.com/en/latest/index.html) python library or [Llama Index](https://gpt-index.readthedocs.io/en/latest/index.html).
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
        "id": "diffusion",
        "name": "Prem Diffusion",
        "playground": True,
        "documentation": """
        # Prem Diffusion
        """,
        "icon": "/assets/apps/diffusion.svg",
    },
]

SERVICES = []


def get_docker_client():
    return docker.from_env()


def is_gpu_available() -> bool:
    return torch.cuda.is_available()


def get_services():
    global SERVICES
    response = requests.get(PREM_REGISTRY_URL)
    SERVICES = response.json()
    for service in SERVICES:
        if is_gpu_available() and "gpu" in service["dockerImages"]:
            service["dockerImage"] = service["dockerImages"]["gpu"]["image"]
            service["dockerImageSize"] = service["dockerImages"]["gpu"]["size"]
            service["supported"] = True
        elif "cpu" in service["dockerImages"]:
            service["dockerImage"] = service["dockerImages"]["cpu"]["image"]
            service["dockerImageSize"] = service["dockerImages"]["cpu"]["size"]
            service["supported"] = True
        else:
            service["dockerImage"] = ""
            service["dockerImageSize"] = 0
            service["supported"] = False
        service["icon"] = service["icon"]


def get_apps():
    return APPS


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
