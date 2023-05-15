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


class AppResponse(BaseModel):
    id: str
    name: str


class ContainerStatsResponse(BaseModel):
    id: str
    cpu_percentage: float
    memory_usage: float
    memory_limit: float
    memory_percentage: float
