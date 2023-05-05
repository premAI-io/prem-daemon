from fastapi import APIRouter

from app.core.utils import get_model_info, get_models_info
from app.models.info import HealthResponse

router = APIRouter()


@router.get("/", response_model=HealthResponse, name="health:get-data")
async def health():
    return HealthResponse(status=True)


@router.get("/models/")
async def get_models():
    return get_models_info()


@router.get("/models/{model_id}")
async def get_model(model_id: str):
    return get_model_info(model_id)
