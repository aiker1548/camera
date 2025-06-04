from uuid import UUID, uuid4
from datetime import datetime
from typing import List, Optional, Tuple

from src.application.video.interfaces.repo import AbstractVideoRepository
from src.application.video.dto.video_filters import VideoFiltersDTO
from src.application.video.dto.pagination import PaginationParams
from src.domain.video.entities.video import Video as VideoDomain
from src.application.video.dto.video import CreateVideoDTO
from src.application.video.dto.enums import TimeOfDay, TracingStatus


class VideoService:
    def __init__(self, repository: AbstractVideoRepository):
        self._repo = repository

    async def get_video(self, video_id: UUID) -> Optional[VideoDomain]:
        return await self._repo.get_by_id(video_id)

    async def list_videos(
        self,
        filters: Optional[VideoFiltersDTO],
        pagination: Optional[PaginationParams]
    ) -> Tuple[List[VideoDomain], int]:
        videos, total_count = await self._repo.list_all(filters=filters, pagination=pagination)
        return {
            "videos": videos,
            "total_count": total_count,
            "pagination": pagination.to_dict()
        }


    async def create_video(self, dto: CreateVideoDTO) -> VideoDomain:
        new_video = VideoDomain(
            id=dto.id or uuid4(),
            name=dto.name,
            duration=dto.duration or 0,
            resolution_width=dto.resolution_width or 0,
            resolution_height=dto.resolution_height or 0,
            fps=dto.fps or 0,
            time_of_day=self.time_of_day(),
            tracing=dto.tracing or TracingStatus.RUN,
            counter=0,
            author_id=dto.author_id,
            camera_id=dto.camera_id,
            upload_time=dto.upload_time or datetime.utcnow(),
            preview_url=dto.preview_url or "",
        )
        created = await self._repo.create(new_video)
        await self._repo.enqueue_for_processing(created.id)
        return created

    async def update_video_after_processing(
        self,
        video_id: UUID,
        duration: float,
        width: int,
        height: int,
        fps: int,
        time_of_day: str,
        tracing: str,
        preview_url: str
    ) -> VideoDomain:
        video = await self._repo.get_by_id(video_id)
        if not video:
            raise ValueError("Video not found")

        video.duration = duration
        video.resolution_width = width
        video.resolution_height = height
        video.fps = fps
        video.time_of_day = time_of_day
        video.tracing = tracing
        video.preview_url = preview_url

        updated = await self._repo.update(video)
        await self._repo.update_processing_status(video_id, tracing)
        return updated

    async def delete_video(self, video_id: UUID) -> None:
        await self._repo.delete(video_id)

    @staticmethod
    def time_of_day() -> TimeOfDay:
        if datetime.now().hour >= 12 and datetime.now().hour < 18:
            return TimeOfDay.DAY
        elif datetime.now().hour >= 18 and datetime.now().hour < 23:
            return TimeOfDay.EVENING
        elif datetime.now().hour >= 23 and datetime.now().hour < 6:
            return TimeOfDay.NIGHT
        elif datetime.now().hour >= 6 and datetime.now().hour < 12:
            return TimeOfDay.MORNING