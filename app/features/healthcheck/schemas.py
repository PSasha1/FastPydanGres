from enum import StrEnum
from pydantic import BaseModel, Field


class ServiceStatus(StrEnum):
    OK = 'ok'
    DEGRADED = 'degraded'
    ERROR = 'error'


class DBConnectionStatus(StrEnum):
    CONNECTED = 'connected'
    DISCONNECTED = 'disconnected'

class HealthCheckResponse(BaseModel):
    status: ServiceStatus = Field(...)
    database: DBConnectionStatus = Field(...)
    environment: str = Field(...)