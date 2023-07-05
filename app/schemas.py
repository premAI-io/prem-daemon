from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: bool


class ErrorResponse(BaseModel):
    message: str


class SuccessResponse(BaseModel):
    message: str


class ServiceInput(BaseModel):
    id: str


class ServiceResponse(BaseModel):
    id: str
    name: str
    description: str
    documentation: str
    icon: str
    modelInfo: dict
    interfaces: list[str]
    dockerImage: str
    dockerImageSize: int
    defaultPort: int
    defaultExternalPort: int
    runningPort: int = None
    volumePath: str = None
    volumeName: str = None
    running: bool
    downloaded: bool
    downloadedDockerImage: str = None
    needsUpdate: bool = False
    supported: bool
    enoughMemory: bool = True
    enoughSystemMemory: bool = True
    beta: bool = False
    comingSoon: bool = False
    envVariables: list[str] = None
    promptTemplate: str = None


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


class GPUStatsResponse(BaseModel):
    gpu_name: str = None
    total_memory: float = None
    used_memory: float = None
    memory_percentage: float = None
