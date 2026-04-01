# Dependency Injection (фабрика зависимостей)

from fastapi import Depends
from typing import Annotated

from app.core.config import get_settings, Settings


SettingsDep = Annotated[Settings, Depends(get_settings)]
