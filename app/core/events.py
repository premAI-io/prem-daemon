import logging

from fastapi import FastAPI

from app.core import config, utils

logger = logging.getLogger(__name__)


def create_start_app_handler(app: FastAPI):
    def start_app() -> None:
        container_name, new_container_name = utils.generate_container_name("premd")
        client = utils.get_docker_client()
        if utils.container_exists(container_name):
            container = client.containers.get(container_name)
            host_port = container.ports.get(f"{utils.DEFAULT_PORT}/tcp", [None])[0][
                "HostPort"
            ]
            if host_port != f"{utils.DEFAULT_PORT}":
                utils.check_host_port_availability(utils.DEFAULT_PORT)
                new_container = utils.create_new_container(
                    utils.PREMD_IMAGE,
                    "latest",
                    new_container_name,
                    container_name,
                    utils.DEFAULT_PORT,
                )
                utils.update_and_remove_old_container(container_name)
                new_container.start()
        for registry in config.PREM_REGISTRY_URL.strip().split():
            utils.add_services_from_registry(registry)

    return start_app
