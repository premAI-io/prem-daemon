import logging
import shutil

import docker
import psutil

from app.core import config, utils

logger = logging.getLogger(__name__)


def get_service_object(
    service, containers, images, free_memory, total_memory, free_storage
):
    service["running"] = False
    service["downloaded"] = False
    service["enoughMemory"] = True
    service["enoughSystemMemory"] = True
    service["enoughStorage"] = True

    if "command" not in service:
        service["command"] = None

    for container in containers:
        if container.name == service["id"]:
            service["running"] = True
            service["runningPort"] = list(container.ports.values())[0][0]["HostPort"]
            try:
                service["volumeName"] = container.attrs["Mounts"][0]["Name"]
            except Exception:
                service["volumeName"] = None

    if (
        "memoryRequirements" in service["modelInfo"]
        and free_memory * 1024 < service["modelInfo"]["memoryRequirements"]
        and not service["running"]
    ):
        service["enoughMemory"] = False

    if (
        "memoryRequirements" in service["modelInfo"]
        and total_memory * 1024 < service["modelInfo"]["memoryRequirements"]
    ):
        service["enoughSystemMemory"] = False

    if utils.is_gpu_available() and "gpu" in service["dockerImages"]:
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

    if service["dockerImageSize"] > free_storage * (2**30):
        service["enoughStorage"] = False

    service_image = service["dockerImage"].split(":")[0]

    service_tags = []
    for image in images:
        if len(image.tags) > 0 and service_image == image.tags[0].split(":")[0]:
            service_tags.append(image.tags[0])

    if len(service_tags) > 0:
        service["downloaded"] = True
        if service["dockerImage"] not in service_tags:
            service["needsUpdate"] = True
            service["downloadedDockerImage"] = service_tags[0]
        else:
            service["needsUpdate"] = False
            service["downloadedDockerImage"] = service["dockerImage"]
    else:
        service["downloaded"] = False

    if config.python_enabled():
        domain = utils.check_dns_exists()

        service["fullURL"] = f"{service['id']}.docker.localhost"
        if domain:
            service["fullURL"] = f"{service['id']}.{domain}"

    return service


def get_services(interface_id: str = None) -> dict:
    docker_client = utils.get_docker_client()

    free_memory, total_memory = get_free_total_memory()
    free_storage = get_free_storage()

    images = docker_client.images.list()
    containers = docker_client.containers.list()

    rich_services = []
    for service in utils.SERVICES:
        if interface_id is None or interface_id in service["interfaces"]:
            service_object = get_service_object(
                service=service,
                containers=containers,
                images=images,
                free_memory=free_memory,
                total_memory=total_memory,
                free_storage=free_storage,
            )
            rich_services.append(service_object)

    return rich_services


def get_service_by_id(service_id: str) -> dict:
    for service in get_services():
        if service["id"] == service_id:
            return service


def add_service(data: dict):
    service_ids = [service["id"] for service in utils.SERVICES]
    if data["id"] not in service_ids:
        utils.SERVICES.append(data)
        return get_service_by_id(data["id"])


def get_registries():
    return utils.REGISTRIES


def add_registry(url: str):
    if url not in utils.REGISTRIES:
        utils.REGISTRIES.append(url)
        utils.add_services_from_registry(url)
        return url


def delete_registry(url: str):
    if url in utils.REGISTRIES:
        utils.delete_services_from_registry(url)
        utils.REGISTRIES.remove(url)
        return url


def stop_all_running_services():
    client = utils.get_docker_client()
    containers = client.containers.list()
    services = get_services()

    for container in containers:
        if container.name in [service["id"] for service in services]:
            logger.info(f"Stopping container {container.name}")
            container.remove(force=True)


def run_container_with_retries(service_object):
    client = utils.get_docker_client()
    service_id = service_object["id"]  # Assuming the service ID is in service_object

    try:
        client.containers.get(service_id).remove(force=True)
    except Exception as error:
        logger.info(f"Failed to remove container {error}.")

    port = service_object["defaultExternalPort"]

    if utils.is_gpu_available():
        device_requests = [
            docker.types.DeviceRequest(device_ids=["all"], capabilities=[["gpu"]])
        ]
    else:
        device_requests = []

    volumes = {}
    if volume_path := service_object.get("volumePath"):
        try:
            volume_name = f"prem-{service_id}-data"
            volume = client.volumes.create(name=volume_name)
            volumes = {volume.id: {"bind": volume_path, "mode": "rw"}}
        except Exception as error:
            logger.error(f"Failed to create volume {error}")

    env_variables = service_object.get("envVariables", [])
    exec_commands = service_object.get("execCommands", [])

    labels = {}
    if config.python_enabled():
        dns_exists = utils.check_dns_exists()
        if dns_exists:
            labels = {
                "traefik.enable": "true",
                f"traefik.http.routers.{service_id}.rule": f"Host(`{service_id}.domain`)",
                f"traefik.http.routers.{service_id}.entrypoints": "websecure",
                f"traefik.http.routers.{service_id}.tls.certresolver": "myresolver",
            }
        else:
            labels = {
                "traefik.enable": "true",
                f"traefik.http.routers.{service_id}.rule": f"Host({service_id}.docker.localhost)",
            }

    for _ in range(10):
        try:
            container = client.containers.run(
                service_object["downloadedDockerImage"],
                command=service_object["command"],
                auto_remove=True,
                detach=True,
                ports={f"{service_object['defaultPort']}/tcp": port},
                name=service_id,
                volumes=volumes,
                environment=env_variables,
                device_requests=device_requests,
                labels=labels,  # Add this line
            )
            logger.info(f"Started container {container.name}")

            for command in exec_commands:
                container.exec_run(command)
            return port
        except Exception as error:
            logger.error(f"Failed to start {error}")
            port += 1


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


def get_system_stats_all():
    total, used, _ = shutil.disk_usage("/")

    memory_info = psutil.virtual_memory()
    memory_limit = memory_info.total / (1024.0**3)
    memory_usage = memory_info.used / (1024.0**3)

    cpu_percentage = psutil.cpu_percent(interval=1)

    return {
        "cpu_percentage": round(cpu_percentage, 2),
        "memory_usage": round(memory_usage, 2),
        "memory_limit": round(memory_limit, 2),
        "memory_percentage": round(memory_info.percent, 2),
        "storage_percentage": round((used / total) * 100, 2),
        "storage_usage": used // (2**30),
        "storage_limit": total // (2**30),
    }


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


def get_free_total_memory():
    if utils.is_gpu_available():
        gpu_values = get_gpu_stats_all()
        free_memory = gpu_values["total_memory"] - gpu_values["used_memory"]
        return free_memory, gpu_values["total_memory"]
    else:
        values = get_system_stats_all()
        free_memory = values["memory_limit"] - values["memory_usage"]
        return free_memory, values["memory_limit"]


def get_free_storage():
    values = get_system_stats_all()
    free_storage = values["storage_limit"] - values["storage_usage"]
    return free_storage
