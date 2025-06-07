import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ----------------------------------------
    # 1) Postgres / SQLAlchemy
    # ----------------------------------------
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://user:password@localhost:5432/dbname"
    )
    DATABASE_ENGINE_POOL_SIZE: int = int(os.getenv("DATABASE_ENGINE_POOL_SIZE", 10))
    DATABASE_ENGINE_POOL_TIMEOUT: int = int(os.getenv("DATABASE_ENGINE_POOL_TIMEOUT", 30))
    DATABASE_ENGINE_POOL_RECYCLE: int = int(os.getenv("DATABASE_ENGINE_POOL_RECYCLE", 1800))
    DATABASE_ENGINE_MAX_OVERFLOW: int = int(os.getenv("DATABASE_ENGINE_MAX_OVERFLOW", 20))
    DATABASE_ENGINE_POOL_PING: bool = os.getenv("DATABASE_ENGINE_POOL_PING", "true").lower() in ("true", "1", "t")
    DATABASE_URL_ALT: str = os.getenv("DATABASE_URL_ALT", "")

    # ----------------------------------------
    # 2) JWT / Авторизация
    # ----------------------------------------
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "supersecretkey")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    # ----------------------------------------
    # 3) Minio S3
    # ----------------------------------------
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin123")
    MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "false").lower() in ("true", "1", "t")
    MINIO_VIDEO_BUCKET: str = os.getenv("MINIO_VIDEO_BUCKET", "videos")
    MINIO_PREVIEW_BUCKET: str = os.getenv("MINIO_PREVIEW_BUCKET", "previews")

    # ----------------------------------------
    # 4) RabbitMQ
    # ----------------------------------------
    RABBIT_HOST: str = os.getenv("RABBIT_HOST", "localhost")
    RABBIT_PORT: int = int(os.getenv("RABBIT_PORT", 5672))
    RABBIT_USER: str = os.getenv("RABBIT_USER", "guest")
    RABBIT_PASS: str = os.getenv("RABBIT_PASS", "guest")
    RABBIT_QUEUE_VIDEO_TASKS: str = os.getenv("RABBIT_QUEUE_VIDEO_TASKS", "video_tasks")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Создаём один общий экземпляр настроек
config = Settings()
