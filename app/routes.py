import json
import logging

import docker
from fastapi import APIRouter, HTTPException, Request
from sse_starlette.sse import EventSourceResponse
from starlette.responses import StreamingResponse

from app import schemas
from app.core import services, utils

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=schemas.HealthResponse)
async def health():
    return schemas.HealthResponse(status=True)


@router.get("/interfaces/", response_model=list[schemas.InterfaceResponse])
async def apps():
    return utils.get_apps()


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
    return {"message": "Download image successfully."}


@router.get("/download-service-stream/{service_id}")
async def download_service_stream(service_id: str):
    service_object = services.get_service_by_id(service_id)
    if service_object is None:
        raise HTTPException(
            status_code=400,
            detail={"message": "Service not found."},
        )

    client = utils.get_docker_client()

    def generator():
        for line in client.api.pull(
            service_object["dockerImage"], stream=True, decode=True
        ):
            yield (json.dumps(line) + "\n")

    return StreamingResponse(generator(), media_type="text/event-stream")


async def generator(service_object, request):
    total_downloaded = 0
    partial_downloaded = 0

    client = utils.get_docker_client()
    for line in client.api.pull(
        service_object["dockerImage"], stream=True, decode=True
    ):
        if (
            len(line.get("progressDetail", {}).keys()) == 0
            and line.get("status") == "Download complete"
        ):
            total_downloaded += partial_downloaded
            partial_downloaded = 0

        partial_downloaded = line.get("progressDetail", {}).get("total", 0)

        line["percentage"] = round(
            (total_downloaded / service_object["dockerImageSize"]) * 100, 2
        )
        print(line)
        yield (json.dumps(line) + "\n")


@router.get("/download-service-stream-sse/{service_id}")
async def download_service_stream_sse(service_id: str, request: Request):
    service_object = services.get_service_by_id(service_id)
    if service_object is None:
        raise HTTPException(
            status_code=400,
            detail={"message": "Service not found."},
        )
    event_generator = generator(service_object, request)
    return EventSourceResponse(event_generator)


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
    if service_object["running"]:
        return {
            "message": f"Service already running on port {service_object['runningPort']}."
        }

    if service_object is None:
        raise HTTPException(
            status_code=400,
            detail={"message": "Service not found."},
        )

    port = services.run_container_with_retries(service_object)
    if port is None:
        raise HTTPException(
            status_code=400,
            detail={
                "message": f"Failed to create container for {service_object['id']}"
            },
        )

    return {
        "message": f"Service started successfully. Container running on port {port}."
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
        if isinstance(error, docker.errors.ImageNotFound):
            logger.warning(error)
            return {"message": f"Container {service_object['id']} not found."}
        logger.error(error)
        raise HTTPException(
            status_code=400,
            detail={"message": f"Failed to stop container {error}"},
        ) from error
    return {"message": f"Service {service_object['id']} successfully."}


@router.get(
    "/stop-all-services/",
    response_model=schemas.SuccessResponse,
    responses={
        400: {
            "model": schemas.ErrorResponse,
            "description": "Failed to stop container or service not found.",
        }
    },
)
async def stop_all_services():
    try:
        services.stop_all_running_services()
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail={"message": f"Failed to stop container {error}"},
        ) from error
    return {"message": "All services stopped successfully."}


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
        if isinstance(error, docker.errors.ImageNotFound):
            logger.warning(error)
            return {"message": f"Image {service_object['dockerImage']} not found."}
        raise HTTPException(
            status_code=400,
            detail={"message": f"Failed to remove image {error}"},
        ) from error
    return {"message": f"Service {service_object['id']} removed successfully."}


@router.get("/remove-volume/{volume_name}")
async def remove_volume(volume_name):
    client = utils.get_docker_client()
    try:
        client.volumes.get(volume_name).remove(force=True)
    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=400,
            detail={"message": f"Failed to remove image {error}"},
        ) from error
    return {"message": f"Volume {volume_name} removed successfully."}


@router.get("/system-prune/")
async def system_prune():
    try:
        services.system_prune()
    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=400,
            detail={"message": f"Failed to prune docker {error}"},
        ) from error
    return {"message": "System pruned successfully."}


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
        stats = services.get_system_stats_all()
    except Exception as error:
        logger.error(error)
        stats = {}
    return stats


@router.get("/gpu-stats-all/", response_model=schemas.GPUStatsResponse)
async def gpu_stats_all():
    try:
        stats = services.get_gpu_stats_all()
    except Exception as error:
        logger.error(error)
        stats = {}
    return schemas.GPUStatsResponse(**stats)
