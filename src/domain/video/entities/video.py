from uuid import UUID
from datetime import datetime, timedelta
from pydantic import BaseModel

from src.application.video.dto.enums import TimeOfDay, TracingStatus


class Video(BaseModel):
    id: UUID
    name: str
    duration: timedelta
    resolution_width: int
    resolution_height: int
    fps: int
    time_of_day: TimeOfDay
    tracing: TracingStatus
    counter: int
    author_id: UUID
    camera_id: UUID
    upload_time: datetime
    preview_url: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        from_attributes = True