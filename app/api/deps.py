# Dependency Injection (фабрика зависимостей)

from fastapi import Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings, Settings
from app.db.session import get_db


SettingsDep = Annotated[Settings, Depends(get_settings)]
DBDep = Annotated[AsyncSession, Depends(get_db)]
