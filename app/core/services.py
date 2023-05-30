import logging
import shutil

import docker

from app.core import utils

logger = logging.getLogger(__name__)


def get_services(interface_id: str = None) -> dict:
    docker_client = utils.get_docker_client()

    images = docker_client.images.list()
    containers = docker_client.containers.list()

    if interface_id is None:
        services = utils.SERVICES
    else:
        services = [
            service
            for service in utils.SERVICES
            if interface_id in service["interfaces"]
        ]

    rich_services = []
    for service in services:
        service["running"] = False
        service["downloaded"] = False
        for container in containers:
            if container.name == service["id"]:
                service["running"] = True
        for image in images:
            if len(image.tags) > 0 and image.tags[0] == service["dockerImage"]:
                service["downloaded"] = True
        rich_services.append(service)

    return rich_services


def get_service_by_id(service_id: str) -> dict:
    docker_client = utils.get_docker_client()

    images = docker_client.images.list()
    containers = docker_client.containers.list()

    for service in utils.SERVICES:
        if service["id"] == service_id:
            service["running"] = False
            service["downloaded"] = False
            for container in containers:
                if container.name == service["id"]:
                    service["running"] = True
                    service["runningPort"] = list(container.ports.values())[0][0][
                        "HostPort"
                    ]
                    try:
                        service["volumeName"] = container.attrs["Mounts"][0]["Name"]
                    except Exception:
                        service["volumeName"] = None
            for image in images:
                if len(image.tags) > 0 and image.tags[0] == service["dockerImage"]:
                    service["downloaded"] = True
            return service


def get_apps():
    return utils.APPS


def get_docker_stats(container_name: str):
    total, _, _ = shutil.disk_usage("/")

    client = utils.get_docker_client()
    container = client.containers.get(container_name)
    value = container.stats(stream=False)
    cpu_percentage, memory_usage, memory_limit, memory_percentage = utils.format_stats(
        value
    )
    storage_usage = container.image.attrs["Size"]

    return {
        "cpu_percentage": round(cpu_percentage, 2),
        "memory_usage": round(memory_usage / 1024, 2),
        "memory_limit": round(memory_limit, 2),
        "memory_percentage": memory_percentage,
        "storage_percentage": round((storage_usage / total) * 100, 2),
        "storage_usage": round(storage_usage // (2**30), 2),
        "storage_limit": total // (2**30),
    }


def get_docker_stats_all():
    total, used, _ = shutil.disk_usage("/")
    client = utils.get_docker_client()

    cpu_percentage = 0
    memory_usage = 0
    memory_limit = 0
    memory_percentage = 0

    containers = client.containers.list()
    for container in containers:
        value = container.stats(stream=False)
        (
            c_cpu_percentage,
            c_memory_usage,
            c_memory_limit,
            c_memory_percentage,
        ) = utils.format_stats(value)
        cpu_percentage += c_cpu_percentage
        memory_usage += c_memory_usage
        memory_percentage += c_memory_percentage
        memory_limit = c_memory_limit

    return {
        "cpu_percentage": round(cpu_percentage, 2),
        "memory_usage": round(memory_usage / 1024, 2),
        "memory_limit": round(memory_limit / 1024, 2),
        "memory_percentage": memory_percentage,
        "storage_percentage": round((used / total) * 100, 2),
        "storage_usage": used // (2**30),
        "storage_limit": total // (2**30),
    }


def run_container_with_retries(service_object):
    client = utils.get_docker_client()
    port = service_object["defaultPort"] + 1

    if utils.is_gpu_available():
        device_requests = [
            docker.types.DeviceRequest(device_ids=["all"], capabilities=[["gpu"]])
        ]
    else:
        device_requests = []

    if "volumePath" in service_object:
        try:
            volume_name = f"prem-{service_object['id']}-data"
            volume = client.volumes.create(name=volume_name)
            volumes = {volume.id: {"bind": service_object["volumePath"], "mode": "rw"}}
        except Exception as error:
            logger.error(f"Failed to create volume {error}")
            volumes = {}

    for _ in range(10):
        try:
            client.containers.run(
                service_object["dockerImage"],
                detach=True,
                ports={f"{service_object['defaultPort']}/tcp": port},
                name=service_object["id"],
                volumes=volumes,
                device_requests=device_requests,
            )
            return port
        except Exception as error:
            logger.error(f"Failed to start {error}")
            port += 1
    return None


def get_gpu_stats_all():
    if utils.is_gpu_available():
        gpu_name, total_memory, used_memory, memory_percentage = utils.get_gpu_info()
        return {
            "gpu_name": gpu_name,
            "total_memory": round(total_memory / 1024, 2),
            "used_memory": round(used_memory / 1024, 2),
            "memory_percentage": memory_percentage,
        }
    return {}


def system_prune():
    client = utils.get_docker_client()
    client.containers.prune()
    client.volumes.prune()
    client.images.prune()
    client.networks.prune()
