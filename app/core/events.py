import logging
from collections.abc import Callable

from fastapi import FastAPI

from app.core import config
from app.core.utils import check_model_ready, download_model, load_model

logger = logging.getLogger(__name__)


def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        if config.MODEL_ID != "controller":
            ready, _ = check_model_ready()
            if not ready:
                download_model()
            load_model()

    return start_app
