import logging

from fastapi import FastAPI

from app.core import utils

logger = logging.getLogger(__name__)


def create_start_app_handler(app: FastAPI):
    def start_app() -> None:
        utils.get_services()

    return start_app
