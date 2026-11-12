from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

engine = create_async_engine(
    settings.DB.url,
    echo=settings.DB.ECHO,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

class Base(AsyncAttrs, DeclarativeBase):
    """Базовый декларативный класс для всех моделей."""
    pass

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency для внедрения сессии БД в эндпоинты FastAPI"""
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
