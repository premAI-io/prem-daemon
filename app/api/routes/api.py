from fastapi import APIRouter

from app.api.routes import chat, info
from app.core.config import MODEL_ID
from app.core.utils import get_model_info

router = APIRouter()

if MODEL_ID == "controller":
    router.include_router(info.router, tags=["info"], prefix="/v1")
elif "chat" in get_model_info(MODEL_ID).get("modelTypes"):
    router.include_router(chat.router, tags=["chat"], prefix="/v1")
