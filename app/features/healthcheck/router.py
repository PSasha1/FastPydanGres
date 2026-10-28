from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db_session
from app.features.healthcheck.schemas import (
    HealthCheckResponse,
    ServiceStatus,
    DBConnectionStatus
)

router = APIRouter(prefix="/health", tags=["Health"])

type DatabaseSession = Annotated[AsyncSession, Depends(get_db_session)]

@router.get(
    "",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Проверка жизнеспособности сервиса",
)
async def healthcheck(session: DatabaseSession) -> HealthCheckResponse:
    db_status = DBConnectionStatus.CONNECTED
    app_status = ServiceStatus.OK

    try:
        # Проверяем реально соединение с Postgres
        await session.execute(text(f"SELECT 1"))
    except Exception as e:
        db_status = DBConnectionStatus.DISCONNECTED
        app_status = ServiceStatus.DEGRADED

    return HealthCheckResponse(
        status=app_status,
        database=db_status,
        environment=settings.ENVIRONMENT,
    )