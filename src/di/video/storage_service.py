import os
import uuid
from pathlib import Path
from fastapi import UploadFile
from minio import Minio
from pika.channel import Channel as PikaChannel
from pika import BasicProperties as PikaBasicProperties
import json

from src.application.video.dto.video import CreateVideoDTO
from src.di.video.service import VideoService

class VideoStorageService:
    def __init__(
        self,
        minio_client: Minio,
        rabbit_channel: PikaChannel,
        video_service: VideoService
    ):
        self._minio = minio_client
        self._rabbit_channel = rabbit_channel
        self._video_service = video_service

        self._video_bucket = os.getenv("MINIO_VIDEO_BUCKET", "videos")
        self._preview_bucket = os.getenv("MINIO_PREVIEW_BUCKET", "previews")

        if not self._minio.bucket_exists(self._video_bucket):
            self._minio.make_bucket(self._video_bucket)
        if not self._minio.bucket_exists(self._preview_bucket):
            self._minio.make_bucket(self._preview_bucket)

    async def upload_file_and_enqueue(self, file: UploadFile, camera_id: uuid.UUID, author_id: uuid.UUID) -> uuid.UUID:
        video_id = uuid.uuid4()
        filename = f"video-{video_id}.mp4"
        temp_dir = Path("/tmp")
        temp_dir.mkdir(exist_ok=True)
        temp_path = temp_dir / filename

        with temp_path.open("wb") as buffer:
            contents = await file.read()
            buffer.write(contents)

        self._minio.fput_object(
            bucket_name=self._video_bucket,
            object_name=filename,
            file_path=str(temp_path),
            content_type=file.content_type
        )
        temp_path.unlink(missing_ok=True)

        
        dto = CreateVideoDTO(
            id=video_id,
            name=filename,
            author_id=author_id,
            camera_id=camera_id,
            tracing="RUN"
        )
        created_video = await self._video_service.create_video(dto)

        queue_name = "video_tasks"
        self._rabbit_channel.queue_declare(queue=queue_name, durable=True)
        payload = {
            "video_id": str(video_id),
            "camera_id": str(camera_id),
            "author_id": str(author_id),
            "object_name": filename
        }
        body = json.dumps(payload).encode("utf-8")
        self._rabbit_channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=body,
            properties=PikaBasicProperties(delivery_mode=2)
        )

        return created_video.id
