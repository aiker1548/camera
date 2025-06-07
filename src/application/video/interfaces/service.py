from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional, Tuple

from src.application.video.dto.video_filters import VideoFiltersDTO
from src.application.video.dto.pagination import PaginationParams
from src.application.video.dto.video import CreateVideoDTO
from src.domain.video.entities.video import Video as VideoDomain
from src.shared_kernel.application.enums import TimeOfDay, TracingStatus

class AbstractVideoService(ABC):
    @abstractmethod
    async def get_video(self, video_id: UUID) -> Optional[VideoDomain]:
        """Fetch a single video by its UUID."""
        pass

    @abstractmethod
    async def list_videos(
        self,
        filters: Optional[VideoFiltersDTO] = None,
        pagination: Optional[PaginationParams] = None
    ) -> Tuple[List[VideoDomain], int]:
        """List videos with optional filters and pagination, returning list and total count."""
        pass

    @abstractmethod
    async def create_video(self, dto: CreateVideoDTO) -> VideoDomain:
        """Create a new video from the provided DTO."""
        pass

    @abstractmethod
    async def update_video_after_processing(
        self,
        video_id: UUID,
        duration: float,
        width: int,
        height: int,
        fps: int,
        time_of_day: TimeOfDay,
        tracing: TracingStatus,
        preview_url: str
    ) -> VideoDomain:
        """Update video metadata after processing is complete."""
        pass

    @abstractmethod
    async def delete_video(self, video_id: UUID) -> None:
        """Delete a video by its UUID."""
        pass

    @staticmethod
    @abstractmethod
    def time_of_day() -> TimeOfDay:
        """Determine time of day based on current time."""
        pass
