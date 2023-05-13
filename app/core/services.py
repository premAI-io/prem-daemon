import shutil

from app.core import utils


def get_services(app_id: str = None) -> dict:
    if app_id is None:
        return utils.SERVICES
    return [service for service in utils.SERVICES if app_id in service["apps"]]


def get_service_by_id(service_id: str) -> dict:
    for service in utils.SERVICES:
        if service["id"] == service_id:
            return service


def get_apps():
    return utils.APPS


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


def get_docker_stats(container_name: str):
    total, used, _ = shutil.disk_usage("/")
    client = utils.get_docker_client()
    container = client.containers.get(container_name)
    value = container.stats(stream=False)
    cpu_percentage, memory_usage, memory_limit, memory_percentage = format_stats(value)
    return {
        "cpu_percentage": cpu_percentage,
        "memory_usage": memory_usage,
        "memory_limit": memory_limit,
        "memory_percentage": memory_percentage,
        "storage_percentage": (used / total) * 100,
        "storage_usage": used // (2**30),
        "storage_limit": total // (2**30),
    }
