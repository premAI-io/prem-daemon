import logging

from fastapi import APIRouter, HTTPException

from app import schemas
from app.core import services, utils

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=schemas.HealthResponse)
async def health():
    return schemas.HealthResponse(status=True)


@router.get("/interfaces/", response_model=list[schemas.InterfaceResponse])
async def apps():
    return services.get_apps()


@router.get("/services/", response_model=list[schemas.ServiceResponse])
async def services_all():
    return services.get_services()


@router.get(
    "/services/{service_id}",
    response_model=schemas.ServiceResponse,
    responses={
        400: {"model": schemas.ErrorResponse, "description": "Service not found."}
    },
)
async def service_by_id(service_id: str):
    service_object = services.get_service_by_id(service_id)
    if service_object is None:
        raise HTTPException(status_code=400, detail={"message": "Service not found."})
    return service_object


@router.get(
    "/services-by-interface/{interface_id}",
    response_model=list[schemas.ServiceResponse],
)
async def services_by_interface(interface_id: str):
    return services.get_services(interface_id)


@router.get(
    "/download-service/{service_id}",
    response_model=schemas.SuccessResponse,
    responses={
        400: {
            "model": schemas.ErrorResponse,
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
    response_model=schemas.SuccessResponse,
    responses={
        400: {
            "model": schemas.ErrorResponse,
            "description": "Failed to start container or service not found.",
        }
    },
)
async def run_service(body: schemas.ServiceInput):
    service_object = services.get_service_by_id(body.id)
    if service_object is None:
        raise HTTPException(
            status_code=400,
            detail={"message": "Service not found."},
        )

    free_port = services.get_free_port(service_object["defaultPort"])

    client = utils.get_docker_client()
    try:
        client.containers.run(
            service_object["dockerImage"],
            detach=True,
            ports={f"{service_object['defaultPort']}/tcp": free_port},
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
    response_model=schemas.SuccessResponse,
    responses={
        400: {
            "model": schemas.ErrorResponse,
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
    response_model=schemas.ContainerStatsResponse,
    responses={
        400: {
            "model": schemas.ErrorResponse,
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
        stats["id"] = service_object["id"]
        return stats
    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=400,
            detail={"message": f"Failed to remove image {error}"},
        ) from error


@router.get("/stats/", response_model=list[schemas.ContainerStatsResponse])
async def stats():
    results = []
    for service in utils.SERVICES:
        try:
            stats = services.get_docker_stats(service["id"])
            stats["id"] = service["id"]
            results.append(stats)
        except Exception as error:
            logger.error(error)
    return results


@router.get("/stats-all/", response_model=schemas.OSStatsResponse)
async def stats_all():
    try:
        stats = services.get_docker_stats_all()
    except Exception as error:
        logger.error(error)
        stats = {}
    return stats
