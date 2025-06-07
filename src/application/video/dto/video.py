from uuid import UUID, uuid4
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, Field

from src.shared_kernel.application.enums import TimeOfDay, TracingStatus


class CreateVideoDTO(BaseModel):
    """
    DTO для создания новой записи видео.
    Поля:
      - id: UUID (если None, будет сгенерирован внутри сервиса)
      - name: str — имя файла/видео (обязательно)
      - author_id: UUID — ID пользователя, загрузившего видео
      - camera_id: UUID — ID камеры, к которой привязано видео
      - duration: Optional[timedelta] — длительность (пока None, заполняет воркер)
      - resolution_width: Optional[int] — ширина примерно (None до обработки)
      - resolution_height: Optional[int] — высота (None до обработки)
      - fps: Optional[int] — кадры в секунду (None до обработки)
      - time_of_day: Optional[TimeOfDay] — время суток (None, воркер пересчитает)
      - tracing: Optional[TracingStatus] — статус трассировки ("RUN" при создании)
      - preview_url: Optional[str] — URL до превью (пусто при создании)
      - upload_time: Optional[datetime] — время загрузки (если None, сервис ставит now)
    """
    id: Optional[UUID] = Field(
        default=None,
        description="UUID видео (если не передан, сгенерируется автоматически)"
    )
    name: str = Field(..., description="Имя файла/видео (должно содержать id)")
    author_id: UUID = Field(..., description="UUID пользователя, загрузившего видео")
    camera_id: UUID = Field(..., description="UUID камеры, к которой прикреплено видео")

    duration: Optional[timedelta] = Field(
        default=None,
        description="Длительность видео (None до фоновой обработки)"
    )
    resolution_width: Optional[int] = Field(
        default=None,
        description="Ширина видео (None до фоновой обработки)"
    )
    resolution_height: Optional[int] = Field(
        default=None,
        description="Высота видео (None до фоновой обработки)"
    )
    fps: Optional[int] = Field(
        default=None,
        description="Количество кадров в секунду (None до фоновой обработки)"
    )
    time_of_day: Optional[TimeOfDay] = Field(
        default=None,
        description="Время суток (None до фоновой обработки)"
    )
    tracing: Optional[TracingStatus] = Field(
        default=TracingStatus.RUN,
        description="Статус трассировки (по умолчанию RUN)"
    )
    preview_url: Optional[str] = Field(
        default=None,
        description="URL до превью (пусто при создании)"
    )
    upload_time: Optional[datetime] = Field(
        default=None,
        description="Время загрузки (если не задано, сервис назначит текущее)"
    )

    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "video-3fa85f64-5717-4562-b3fc-2c963f66afa6.mp4",
                "author_id": "11111111-1111-1111-1111-111111111111",
                "camera_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "tracing": "RUN"
            }
        }
