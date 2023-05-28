import shutil

from app.core import utils


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
            for image in images:
                if len(image.tags) > 0 and image.tags[0] == service["dockerImage"]:
                    service["downloaded"] = True
            return service


def get_apps():
    return utils.APPS


def get_docker_stats(container_name: str):
    client = utils.get_docker_client()
    container = client.containers.get(container_name)
    value = container.stats(stream=False)
    cpu_percentage, memory_usage, memory_limit, memory_percentage = utils.format_stats(
        value
    )
    return {
        "cpu_percentage": cpu_percentage,
        "memory_usage": memory_usage,
        "memory_limit": memory_limit,
        "memory_percentage": memory_percentage,
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
        "cpu_percentage": cpu_percentage,
        "memory_usage": memory_usage,
        "memory_limit": memory_limit,
        "memory_percentage": memory_percentage,
        "storage_percentage": (used / total) * 100,
        "storage_usage": used // (2**30),
        "storage_limit": total // (2**30),
    }


def get_free_port(default_port: int = 8000):
    client = utils.get_docker_client()
    containers = client.containers.list()

    allocated_ports = []
    for container in containers:
        allocated_ports.extend(
            int(value[0]["HostPort"]) for value in container.ports.values()
        )

    for port in range(default_port, 9000):
        if port not in allocated_ports:
            return port
