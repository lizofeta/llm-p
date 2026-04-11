# Асинхронный engine SQLAlchemy и фабрика сессий

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    async_sessionmaker,
    AsyncSession
    )

from app.core.config import get_db_url
from app.core.config import get_settings

# Настройки
settings = get_settings()
DB_URL = get_db_url(settings)

# async engine
engine = create_async_engine(
       DB_URL,
       echo=settings.app_debug
)

# фабрика сессий 
AsyncSessionLocal = async_sessionmaker(
       bind=engine,
       expire_on_commit=False,
       autoflush=False
)

# зависимость для FastApi - дает сессию БД на один HTTP-запрос
async def get_db() -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSessionLocal() as session:
             yield session
