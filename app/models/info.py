from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: bool
