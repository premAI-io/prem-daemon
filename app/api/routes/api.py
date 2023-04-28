from fastapi import APIRouter

from api.routes import chat

router = APIRouter()
router.include_router(chat.router, tags=["predictor"], prefix="/v1")
