from datetime import datetime, timedelta
from typing import List, Optional

from uuid import UUID

from src.application.video.dto.enums import TimeOfDay, TracingStatus

class VideoFiltersDTO:
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    duration_from: Optional[timedelta]
    duration_to: Optional[timedelta]
    time_of_day: Optional[List[TimeOfDay]]
    tracing: Optional[List[TracingStatus]]
    author_ids: Optional[List[UUID]]
    camera_ids: Optional[List[UUID]]
    name_substring: Optional[str]

    def __init__(
        self,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        duration_from: Optional[timedelta] = None,
        duration_to: Optional[timedelta] = None,
        time_of_day: Optional[List[TimeOfDay]] = None,
        tracing: Optional[List[TracingStatus]] = None,
        author_ids: Optional[List[UUID]] = None,
        camera_ids: Optional[List[UUID]] = None,
        name_substring: Optional[str] = None,
    ):
        self.date_from = date_from
        self.date_to = date_to
        self.duration_from = duration_from
        self.duration_to = duration_to
        self.time_of_day = time_of_day
        self.tracing = tracing
        self.author_ids = author_ids
        self.camera_ids = camera_ids
        self.name_substring = name_substring