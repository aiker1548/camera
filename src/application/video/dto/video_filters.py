from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from fastapi import Query

from src.application.video.dto.enums import TimeOfDay, TracingStatus

class VideoFiltersDTO(BaseModel):
    date_from: Optional[datetime] = Field(None, description="Дата начала")
    date_to: Optional[datetime] = Field(None, description="Дата конца")
    duration_from: Optional[int] = Field(None, description="Длительность от (секунды)")
    duration_to: Optional[int] = Field(None, description="Длительность до (секунды)")
    time_of_day: Optional[List[TimeOfDay]] = Field(default=None, description="Время суток")
    tracing: Optional[List[TracingStatus]] = Field(None, description="Статус трейсинга")
    author_ids: Optional[List[UUID]] = Field(None, description="ID авторов")
    camera_ids: Optional[List[UUID]] = Field(None, description="ID камер")
    name_substring: Optional[str] = Field(None, description="Подстрока имени")

    @classmethod
    def as_query_dep(
        cls,
        date_from: Optional[datetime] = Query(None),
        date_to: Optional[datetime] = Query(None),
        duration_from: Optional[int] = Query(None),
        duration_to: Optional[int] = Query(None),
        time_of_day: Optional[List[TimeOfDay]] = Query(None),
        tracing: Optional[List[TracingStatus]] = Query(None),
        author_ids: Optional[List[UUID]] = Query(None),
        camera_ids: Optional[List[UUID]] = Query(None),
        name_substring: Optional[str] = Query(None),
    ) -> "VideoFiltersDTO":
        return cls(
            date_from=date_from,
            date_to=date_to,
            duration_from=duration_from,
            duration_to=duration_to,
            time_of_day=time_of_day,
            tracing=tracing,
            author_ids=author_ids,
            camera_ids=camera_ids,
            name_substring=name_substring,
        )

