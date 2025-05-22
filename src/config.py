import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    
    #posrgres
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/dbname")
    DATABASE_ENGINE_POOL_SIZE: int = 10
    DATABASE_ENGINE_POOL_TIMEOUT: int = 30
    DATABASE_ENGINE_POOL_RECYCLE: int = 1800
    DATABASE_ENGINE_MAX_OVERFLOW: int = 20
    DATABASE_ENGINE_POOL_PING: bool = True
    DATABASE_URL_ALT: str = os.getenv("DATABASE_URL_ALT", "")

    class Config:
        env_file = "../env"  # Путь к файлу .env


# Загружаем конфигурацию
config = Settings()