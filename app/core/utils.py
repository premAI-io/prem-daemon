import logging
import re
import subprocess
import time
import xml.etree.ElementTree as ET

import docker
import requests
import torch
from bs4 import BeautifulSoup
from packaging.version import parse as parse_version

from app.core import config

logger = logging.getLogger(__name__)

PREMD_IMAGE = config.PREMD_IMAGE
DEFAULT_PORT = config.DEFAULT_PORT
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

We don't have a standard interface for what concerns Vector Store services. However, we suggest to connect to the services using [Langchain](https://python.langchain.com/en/latest/index.html) python library or [Llama Index](https://gpt-index.readthedocs.io/en/latest/index.html).
""",  # noqa E501
        "icon": "/assets/apps/store.svg",
    },
    {
        "id": "coder",
        "name": "Coder",
        "playground": False,
        "documentation": """
# Coder

## Description

Coder are all the services that expose endpoints for code completion functionalities. As an example, you can think about GitHub Copilot as the main centralized alternative.

## Installation & Usage

We don't have a standard interface for what concerns Coder services. However, right now we mostly support services based on Tabby Docker images. In order to use Tabby services, you will need to install and use Tabby extension. You can find the extension [here](https://marketplace.visualstudio.com/items?itemName=TabbyML.vscode-tabby).
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


def extract_labels_from_html_file(html_content, class_names):
    soup = BeautifulSoup(html_content, "html.parser")
    labels = soup.select(class_names)
    return (label.get_text() for label in labels)


def find_maximum_label(labels):
    pattern = re.compile(r"v\d+\.\d+\.\d+$")
    return max(filter(pattern.match, labels), default=None, key=parse_version)


def get_premd_last_tag(owner, repository, package):
    response = requests.get(
        f"https://github.com/{owner}/{repository}/pkgs/container/{package}"
    )
    try:
        labels = extract_labels_from_html_file(
            response.content, ".Label.mr-1.mb-2.text-normal"
        )
    except Exception as e:
        logger.info(f"Unexpected error: {e}")
        return "latest"
    else:
        return find_maximum_label(labels)


def get_local_docker_image_tags(owner, repository):
    try:
        client = get_docker_client()
        image = client.images.get(f"ghcr.io/{owner}/{repository}")
        return image.tags
    except Exception as e:
        logger.info(f"Unexpected error: {e}")
        return []


def create_new_container(image_name, image_tag, new_container_name, old_container_name):
    client = get_docker_client()
    old_container = client.containers.get(old_container_name)

    if is_gpu_available():
        device_requests = [
            docker.types.DeviceRequest(device_ids=["all"], capabilities=[["gpu"]])
        ]
    else:
        device_requests = []

    volumes = {}
    for mount in old_container.attrs["Mounts"]:
        source = mount["Source"]
        target = mount["Destination"]
        mode = mount["Mode"]
        volumes[source] = {"bind": target, "mode": mode}

    current_ports = old_container.attrs["HostConfig"]["PortBindings"]
    current_port = list(current_ports.items())[0]

    logger.info(
        f"Starting new container {new_container_name} with image {image_name}:{image_tag} at port {current_port[0]}"
    )
    new_container = client.containers.create(
        image=f"{image_name}:{image_tag}",
        name=new_container_name,
        ports={current_port[0]: current_port[1]},
        volumes=volumes,
        environment=old_container.attrs["Config"]["Env"],
        device_requests=device_requests,
        network_mode=old_container.attrs["HostConfig"]["NetworkMode"],
        detach=True,
    )
    return new_container


def update_and_remove_old_container(old_container_name):
    client = get_docker_client()
    logger.info(f"Stopping {old_container_name}")
    old_container = client.containers.get(old_container_name)
    old_container.stop()


def update_container():
    new_container = create_new_container(
        PREMD_IMAGE, "latest", "new_container", "premd"
    )
    update_and_remove_old_container("premd")
    new_container.start()
    new_container.rename("premd")


def check_host_port_availability(host_port, timeout=30):
    start_time = time.time()
    client = get_docker_client()

    while True:
        if time.time() - start_time > timeout:
            return False

        containers = client.containers.list()
        port_used = any(
            f"{host_port}/tcp" in container.ports
            for container in containers
            if container.status == "running"
        )

        if not port_used:
            return True

        time.sleep(1)


def container_exists(container_name):
    try:
        client = get_docker_client()
        _ = client.containers.get(container_name)
        return True
    except docker.errors.NotFound:
        return False
    except docker.errors.APIError as e:
        logging.error(f"Error checking container existence: {e}")
        return False


cached_domain = None


def check_dns_exists():
    global cached_domain

    if cached_domain is not None:
        return cached_domain

    url = config.dns_exists_url()
    try:
        response = requests.get(url)
        if response.status_code == 200 and response.content:
            json_response = response.json()
            if "domain" in json_response:
                cached_domain = json_response["domain"]
                return cached_domain
            else:
                print("Domain field not found in response.")
                return None
        else:
            print(
                f"Failed to get a valid response. Status Code: {response.status_code}"
            )
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
