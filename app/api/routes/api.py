from fastapi import APIRouter

from app.api.routes import chat, info
from app.core import config
from app.core.utils import get_model_info

router = APIRouter()

if config.MODEL_ID == "controller":
    router.include_router(info.router, tags=["info"], prefix="/v1")
elif "chat" in get_model_info(config.MODEL_ID).get("modelTypes"):
    router.include_router(chat.router, tags=["chat"], prefix="/v1")
