import logging

from fastapi import FastAPI

from app.core import config, utils

logger = logging.getLogger(__name__)


def create_start_app_handler(app: FastAPI):
    def start_app() -> None:
        for registry in config.PREM_REGISTRY_URL.strip().split():
            utils.add_services_from_registry(registry)

    return start_app
