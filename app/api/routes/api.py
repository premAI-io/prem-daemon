from fastapi import APIRouter

from app.core.utils import get_services_info, get_service_info
from app.models.info import HealthResponse

router = APIRouter()


@router.get("/", response_model=HealthResponse, name="health:get-data")
async def health():
    return HealthResponse(status=True)


@router.get("/services/")
async def get_models():
    return get_services_info()


@router.get("/services/{service_id}")
async def get_model(service_id: str):
    return get_service_info(service_id)
