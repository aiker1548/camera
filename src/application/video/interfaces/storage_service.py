from abc import ABC, abstractmethod
from uuid import UUID
from pathlib import Path
from fastapi import UploadFile
from minio import Minio
from pika.channel import Channel as PikaChannel

class AbstractVideoStorageService(ABC):
    @abstractmethod
    async def upload_file_and_enqueue(
        self,
        file: UploadFile,
        camera_id: UUID,
        author_id: UUID
    ) -> UUID:
        """
        Validate, store upload file to object storage, create video entry via video service,
        and enqueue processing task. Returns the new video UUID.
        """
        pass

    @property
    @abstractmethod
    def minio_client(self) -> Minio:
        """Get underlying Minio client instance."""
        pass

    @property
    @abstractmethod
    def rabbit_channel(self) -> PikaChannel:
        """Get underlying RabbitMQ channel for task enqueueing."""
        pass
