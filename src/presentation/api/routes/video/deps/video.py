from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.video.service.service import VideoService
from src.application.video.service.storage_service import VideoStorageService
from src.infrastructure.data.postgres.repositories.video_repository import PostgresVideoRepository
from src.presentation.api.routes.tools.dependencies.tools_dep import get_async_session
from src.infrastructure.data.minio.base import get_minio_client
from src.infrastructure.data.rabbitmq.base import get_rabbit_channel

def get_video_service(
    session: AsyncSession = Depends(get_async_session)
) -> VideoService:
    """
    Возвращает VideoService, создавая под капотом PostgresVideoRepository.
    """
    repo = PostgresVideoRepository(session)
    return VideoService(repo)

def get_video_storage_service(
    video_service: VideoService = Depends(get_video_service),
    minio_client: get_minio_client = Depends(get_minio_client),
    rabbit_channel: get_rabbit_channel = Depends(get_rabbit_channel)
) -> VideoStorageService:
    """
    Возвращает VideoStorageService, создавая под капотом Minio-клиент, RabbitMQ-канал и VideoService.
    Предполагается, что:
      - minio_client, rabbit_channel уже инициализированы в main.py
      - bucket’ы Minio созданы
    """
    return VideoStorageService(minio_client, rabbit_channel, video_service)