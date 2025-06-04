import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from minio import Minio
from pika.channel import Channel as PikaChannel
from pika import BasicProperties as PikaBasicProperties
import json

from src.application.video.dto.video import CreateVideoDTO
from src.application.video.service.service import VideoService
from src.application.video.dto.enums import TracingStatus
from src.shared_kernel.config import config

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

        self._video_bucket = config.MINIO_VIDEO_BUCKET
        self._preview_bucket = config.MINIO_PREVIEW_BUCKET

        if not self._minio.bucket_exists(self._video_bucket):
            self._minio.make_bucket(self._video_bucket)
        if not self._minio.bucket_exists(self._preview_bucket):
            self._minio.make_bucket(self._preview_bucket)

    async def upload_file_and_enqueue(self, file: UploadFile, camera_id: uuid.UUID, author_id: uuid.UUID) -> uuid.UUID:
        if not file.filename.lower().endswith(".mp4") or file.content_type != "video/mp4":
            raise HTTPException(status_code=400, detail="Файл должен быть в формате MP4")

        video_id = uuid.uuid4()
        filename = f"video-{video_id}.mp4"
        temp_dir = Path("/tmp")
        temp_dir.mkdir(exist_ok=True)
        temp_path = temp_dir / filename

        try:
            contents = await file.read()
            if not contents:
                raise HTTPException(status_code=400, detail="Файл пустой или поврежден")

            with temp_path.open("wb") as buffer:
                buffer.write(contents)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Не удалось прочитать файл")

        try:
            self._minio.fput_object(
                bucket_name=self._video_bucket,
                object_name=filename,
                file_path=str(temp_path),
                content_type=file.content_type
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail="Ошибка при загрузке в хранилище")
        finally:
            temp_path.unlink(missing_ok=True)

        dto = CreateVideoDTO(
            id=video_id,
            name=filename,
            author_id=author_id,
            camera_id=camera_id,
            tracing=TracingStatus.RUN
        )
        created_video = await self._video_service.create_video(dto)

        try:
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
        except Exception as e:
            raise HTTPException(status_code=500, detail="Ошибка при отправке в очередь")

        return {"video_id": created_video.id}

