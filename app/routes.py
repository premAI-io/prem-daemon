import logging

from fastapi import APIRouter, HTTPException

from app import models
from app.core import services, utils

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=models.HealthResponse)
async def health():
    return models.HealthResponse(status=True)


@router.get("/apps/", response_model=list[models.AppResponse])
async def apps():
    return services.get_apps()


@router.get("/services/", response_model=list[models.ServiceResponse])
async def services_all():
    return services.get_services()


@router.get(
    "/services/{service_id}",
    response_model=models.ServiceResponse,
    responses={
        400: {"model": models.ErrorResponse, "description": "Service not found."}
    },
)
async def service_by_id(service_id: str):
    service_object = services.get_service_by_id(service_id)
    if service_object is None:
        raise HTTPException(status_code=400, detail={"message": "Service not found."})
    return service_object


@router.get("/services-by-app/{app_id}", response_model=list[models.ServiceResponse])
async def services_by_app(app_id: str):
    return services.get_services(app_id)


@router.get(
    "/download-service/{service_id}",
    response_model=models.SuccessResponse,
    responses={
        400: {
            "model": models.ErrorResponse,
            "description": "Failed to download image or service not found.",
        }
    },
)
async def download_service(service_id: str):
    service_object = services.get_service_by_id(service_id)
    if service_object is None:
        raise HTTPException(
            status_code=400,
            detail={"message": "Service not found."},
        )

    client = utils.get_docker_client()
    try:
        client.images.pull(service_object["dockerImage"])
    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=400,
            detail={"message": f"Failed to download image {error}"},
        ) from error
    return {"message": "Image downloaded successfully."}


@router.post(
    "/run-service/",
    response_model=models.SuccessResponse,
    responses={
        400: {
            "model": models.ErrorResponse,
            "description": "Failed to start container or service not found.",
        }
    },
)
async def run_service(body: models.ServiceInput):
    service_object = services.get_service_by_id(body.id)
    if service_object is None:
        raise HTTPException(
            status_code=400,
            detail={"message": "Service not found."},
        )

    client = utils.get_docker_client()
    try:
        client.containers.run(
            service_object["dockerImage"],
            detach=True,
            ports={
                f"{service_object['defaultPort']}/tcp": service_object["defaultPort"]
            },
            name=service_object["id"],
        )
    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=400,
            detail={"message": f"Failed to start container {error}"},
        ) from error

    return {
        "message": f"Service started successfully. Container running on port {service_object['defaultPort']}."
    }


@router.get(
    "/stop-service/{service_id}",
    response_model=models.SuccessResponse,
    responses={
        400: {
            "model": models.ErrorResponse,
            "description": "Failed to stop container or service not found.",
        }
    },
)
async def stop_service(service_id: str):
    service_object = services.get_service_by_id(service_id)
    if service_object is None:
        raise HTTPException(
            status_code=400,
            detail={"message": "Service not found."},
        )

    client = utils.get_docker_client()
    try:
        client.containers.get(service_object["id"]).remove(force=True)
    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=400,
            detail={"message": f"Failed to stop container {error}"},
        ) from error
    return {"message": f"Service {service_object['id']} successfully."}


@router.get("/remove-service/{service_id}")
async def remove_service(service_id):
    service_object = services.get_service_by_id(service_id)
    if service_object is None:
        raise HTTPException(
            status_code=400,
            detail={"message": "Service not found."},
        )

    client = utils.get_docker_client()
    try:
        client.images.remove(service_object["dockerImage"], force=True)
    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=400,
            detail={"message": f"Failed to remove image {error}"},
        ) from error
    return {"message": f"Service {service_object['id']} removed successfully."}


@router.get(
    "/stats/{service_id}",
    response_model=models.ContainerStatsResponse,
    responses={
        400: {
            "model": models.ErrorResponse,
            "description": "Failed to get stats or service not found.",
        }
    },
)
async def stats_by_service(service_id: str):
    service_object = services.get_service_by_id(service_id)
    if service_object is None:
        raise HTTPException(
            status_code=400,
            detail={"message": "Service not found."},
        )

    try:
        stats = services.get_docker_stats(service_object["id"])
    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=400,
            detail={"message": f"Failed to remove image {error}"},
        ) from error
    stats["id"] = service_object["id"]
    return stats


@router.get("/stats/", response_model=list[models.ContainerStatsResponse])
async def stats():
    results = []
    for service in utils.SERVICES:
        try:
            stats = services.get_docker_stats(service["id"])
        except Exception as error:
            logger.error(error)
        stats["id"] = service["id"]
        results.append(stats)
    return results
