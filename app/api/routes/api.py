from fastapi import APIRouter

from app.core import config
from app.api.routes import info, chat
from app.core.utils import get_model_info

router = APIRouter()
router.include_router(info.router, tags=["info"], prefix="/v1")

if get_model_info(config.MODEL_ID).get("modelType") == "chat":
    router.include_router(chat.router, tags=["chat"], prefix="/v1")
