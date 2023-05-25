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
    apps: list[str]
    dockerImage: str
    defaultPort: int
    running: bool
    downloaded: bool
    supported: bool


class AppResponse(BaseModel):
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


class OSStatsResponse(BaseModel):
    cpu_percentage: float
    memory_usage: float
    memory_limit: float
    memory_percentage: float
    storage_usage: float
    storage_limit: float
    storage_percentage: float
