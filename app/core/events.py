import logging

from fastapi import FastAPI

logger = logging.getLogger(__name__)


def create_start_app_handler(app: FastAPI):
    def start_app() -> None:
        pass

    return start_app
