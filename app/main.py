from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import engine
from app.core.docs import router as docs_router
from app.features.healthcheck.router import router as health_router


BASE_DIR = Path(__file__).resolve().parent

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Lifespan-обработчик для FastAPI.
    Код до yield выполняется при старте приложения,
    код после yield — при завершении.
    Таблицы создаются через `alembic upgrade head`
    """
    # Таблицы уже созданы через alembic (запускается отдельно перед стартом сервера)
    # Startup: Можно добавить проверку: все ли миграции применены, проверку коонекта и тд
    yield
    # Shutdown: закрытие пула соединение с Postgres
    await engine.dispose()

def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
    )
    static_dir = BASE_DIR / "static"
    if static_dir.exists() and settings.DOCS_OFFLINE:
        application.mount("/static", StaticFiles(directory=static_dir), name="static")

    # Подключение общего api_router:
    application.include_router(docs_router)
    application.include_router(health_router, prefix='/api/v1')

    return application

app = create_app()
