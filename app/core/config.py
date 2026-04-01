# Конфигурация приложения (env -> Settings)

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # Настройка загрузки и обработки настроек из .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        case_sensitive=False
    )

    # Настройки приложения 
    app_name: str
    env: str = 'dev'
    app_debug : bool = True

    # JWT
    jwt_secret: str
    jwt_alg: str
    access_token_expire_minutes: int = 60

    # DB
    db_path: str 

    # OpenRouter
    openrouter_api_key: str
    openrouter_base_url: str
    openrouter_model: str
    openrouter_site_url: str
    openrouter_app_name: str

@lru_cache
def get_settings():
    return Settings()

def get_db_url(settings: Settings) -> str:
    return f"sqlite+aiosqlite:///{settings.db_path}"
