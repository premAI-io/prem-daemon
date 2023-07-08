import logging

from fastapi import FastAPI

from app.core import config, utils

logger = logging.getLogger(__name__)


def create_start_app_handler(app: FastAPI):
    def start_app() -> None:
        utils.add_services_from_registry(config.PREM_REGISTRY_URL)

    return start_app
