from typing import List

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: bool


class ErrorResponse(BaseModel):
    message: str


class SuccessResponse(BaseModel):
    message: str


class RunServiceInput(BaseModel):
    id: str


class ServiceInput(BaseModel):
    id: str
    name: str
    modelInfo: dict
    interfaces: list[str]
    dockerImages: dict
    defaultPort: int
    defaultExternalPort: int
    runningPort: int = None
    volumePath: str = None
    volumeName: str = None
    envVariables: list[str] = None
    promptTemplate: str = None


class ServiceResponse(BaseModel):
    id: str
    name: str
    description: str = None
    documentation: str = None
    icon: str = None
    modelInfo: dict
    interfaces: list[str]
    dockerImage: str
    dockerImageSize: int
    defaultPort: int
    defaultExternalPort: int
    runningPort: int = None
    command: str = None
    volumePath: str = None
    volumeName: str = None
    running: bool
    downloaded: bool
    downloadedDockerImage: str = None
    needsUpdate: bool = False
    supported: bool
    enoughMemory: bool = True
    enoughSystemMemory: bool = True
    enoughStorage: bool = True
    beta: bool = False
    comingSoon: bool = False
    envVariables: list[str] = None
    execCommands: list[str] = None
    promptTemplate: str = None
    baseUrl: str = None


class RegistryInput(BaseModel):
    url: str


class RegistryResponse(BaseModel):
    url: str


class InterfaceResponse(BaseModel):
    id: str
    name: str
    playground: bool
    documentation: str
    icon: str


class ContainerStatsResponse(BaseModel):
    id: str
    cpu_percentage: float
    memory_usage: float
    memory_limit: float
    memory_percentage: float
    storage_percentage: float
    storage_usage: float
    storage_limit: float


class OSStatsResponse(BaseModel):
    cpu_percentage: float
    memory_usage: float
    memory_limit: float
    memory_percentage: float
    storage_usage: float
    storage_limit: float
    storage_percentage: float


class SingleGPUStats(BaseModel):
    gpu_name: str = None
    total_memory: float = None
    used_memory: float = None
    free_memory: float = None
    utilised_memory: float = None
    load: float = None


class GPUStatsResponse(BaseModel):
    total_memory: float = None
    used_memory: float = None
    free_memory: float = None
    average_utilised_memory: float = None
    average_load: float = None
    gpus: list[SingleGPUStats]
