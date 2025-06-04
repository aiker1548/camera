import json
import asyncio
from pathlib import Path
from uuid import UUID


from pika.adapters.asyncio_connection import AsyncioConnection
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from moviepy.video.io.VideoFileClip import VideoFileClip

from src.infrastructure.data.postgres.repositories.video_repository import PostgresVideoRepository
from src.shared_kernel.config import config 
from src.infrastructure.data.minio.base import minio_client
from src.infrastructure.data.postgres.base import AsyncSessionMaker
from src.infrastructure.data.rabbitmq.base import RABBIT_PARAMS
from src.application.video.dto.enums import TracingStatus


asyncio_conn: AsyncioConnection | None = None


async def process_video_message(body: bytes):
    data = json.loads(body)
    video_id = data["video_id"]
    object_name = data["object_name"]

    print(f"[Consumer] Received task for video_id = {video_id}")

    temp_dir = Path("/tmp")
    temp_dir.mkdir(exist_ok=True)

    local_video_path = temp_dir / object_name

    try:
        minio_client.fget_object(config.MINIO_VIDEO_BUCKET, object_name, str(local_video_path))
    except Exception as e:
        print(f"[Consumer] Ошибка скачивания видео {video_id}: {e}")
        async with AsyncSessionMaker() as session:
            repo = PostgresVideoRepository(session)
            await repo.update_processing_status(UUID(video_id), "Error")
        return

    try:
        with VideoFileClip(str(local_video_path)) as clip:
            duration = clip.duration
            width, height = clip.size
            fps = clip.fps

            preview_filename = f"preview-{video_id}.jpg"
            preview_local_path = temp_dir / preview_filename
            clip.save_frame(str(preview_local_path), t=0.0)

        if not minio_client.bucket_exists(config.MINIO_PREVIEW_BUCKET):
            minio_client.make_bucket(config.MINIO_PREVIEW_BUCKET)

        minio_client.fput_object(
            bucket_name=config.MINIO_PREVIEW_BUCKET,
            object_name=preview_filename,
            file_path=str(preview_local_path),
            content_type="image/jpeg"
        )
        preview_url = f"{config.MINIO_PREVIEW_BUCKET}/{preview_filename}"

    except Exception as exc:
        print(f"[Consumer] Ошибка при обработке видео {video_id}: {exc}")
        async with AsyncSessionMaker() as session:
            repo = PostgresVideoRepository(session)
            await repo.update_processing_status(UUID(video_id), "Error")
        local_video_path.unlink(missing_ok=True)
        return

    async with AsyncSessionMaker() as session:
        repo = PostgresVideoRepository(session)
        video = await repo.get_by_id(UUID(video_id))
        if video:
            video.duration = duration
            video.resolution_width = width
            video.resolution_height = height
            video.fps = fps
            video.tracing = TracingStatus.DONE
            video.preview_url = preview_url
            video.counter += 1

            await repo.update(video)
            await repo.update_processing_status(UUID(video_id), "DONE")
        else:
            print(f"[Consumer] Видео {video_id} не найдено в БД")

    local_video_path.unlink(missing_ok=True)
    preview_local_path.unlink(missing_ok=True)

    print(f"[Consumer] Finished processing video_id = {video_id}")


def start_video_consumer():
    """
    Инициализирует AsyncioConnection и подписку на очередь.
    Не блокирует, поскольку работа идёт в том же asyncio-loop, что и FastAPI.
    """
    global asyncio_conn

    def on_connection_open(connection):
        # вызывается, когда соединение успешно открылось
        print("[Consumer] AsyncioConnection open")
        connection.channel(on_open_callback=on_channel_open)

    def on_channel_open(ch):
        print("[Consumer] Channel open, declaring queue")
        global channel  
        channel = ch
        channel.queue_declare(
            queue=config.RABBIT_QUEUE_VIDEO_TASKS,
            durable=True,
            callback=on_queue_declared
        )

    # В on_queue_declared
    def on_queue_declared(frame):
        print(f"[Consumer] Queue declared: {config.RABBIT_QUEUE_VIDEO_TASKS}")
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=config.RABBIT_QUEUE_VIDEO_TASKS,
            on_message_callback=on_message
        )

    def on_message(channel, method, properties, body):
        # На каждое сообщение создаём таск для async-обработчика
        print(f"[Consumer] Received message: {body.decode()}")
        asyncio.create_task(process_video_message(body))
        channel.basic_ack(delivery_tag=method.delivery_tag)

    asyncio_conn = AsyncioConnection(
        parameters=RABBIT_PARAMS,
        on_open_callback=on_connection_open
    )


def stop_video_consumer():
    """
    Закрывает AsyncioConnection (вызывается при shutdown).
    """
    global asyncio_conn
    if asyncio_conn and not asyncio_conn.is_closed:
        asyncio_conn.close()
        print("[Consumer] Connection closed")
