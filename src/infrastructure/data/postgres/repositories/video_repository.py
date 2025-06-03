from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from uuid import UUID, uuid4
from typing import List, Optional, Tuple
from datetime import timedelta

from src.application.video.interfaces.repo import AbstractVideoRepository
from src.domain.video.entities.video import Video as VideoDomain
from src.infrastructure.data.postgres.models.video import Video as VideoModel
from src.infrastructure.data.postgres.models.VideoProcessingQueue import VideoProcessingQueue
from src.application.video.dto.video_filters import VideoFiltersDTO
from src.application.video.dto.pagination import PaginationParams


class PostgresVideoRepository(AbstractVideoRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, video_id: UUID) -> Optional[VideoDomain]:
        result = await self._session.execute(
            select(VideoModel).where(VideoModel.id == video_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_all(
        self,
        filters: Optional[VideoFiltersDTO] = None,
        pagination: Optional[PaginationParams] = None
    ) -> Tuple[List[VideoDomain], int]:
        query = select(VideoModel)
        count_q = select(func.count()).select_from(VideoModel)

        if filters:
            if filters.date_from:
                query = query.where(VideoModel.upload_time >= filters.date_from)
                count_q = count_q.where(VideoModel.upload_time >= filters.date_from)
            if filters.date_to:
                query = query.where(VideoModel.upload_time <= filters.date_to)
                count_q = count_q.where(VideoModel.upload_time <= filters.date_to)
            if filters.duration_from:
                query = query.where(VideoModel.duration >= filters.duration_from)
                count_q = count_q.where(VideoModel.duration >= filters.duration_from)
            if filters.duration_to:
                query = query.where(VideoModel.duration <= filters.duration_to)
                count_q = count_q.where(VideoModel.duration <= filters.duration_to)
            if filters.time_of_day:
                query = query.where(VideoModel.time_of_day.in_(filters.time_of_day))
                count_q = count_q.where(VideoModel.time_of_day.in_(filters.time_of_day))
            if filters.tracing:
                query = query.where(VideoModel.tracing.in_(filters.tracing))
                count_q = count_q.where(VideoModel.tracing.in_(filters.tracing))
            if filters.author_ids:
                query = query.where(VideoModel.author_id.in_(filters.author_ids))
                count_q = count_q.where(VideoModel.author_id.in_(filters.author_ids))
            if filters.camera_ids:
                query = query.where(VideoModel.camera_id.in_(filters.camera_ids))
                count_q = count_q.where(VideoModel.camera_id.in_(filters.camera_ids))
            if filters.name_substring:
                pattern = f"%{filters.name_substring}%"
                query = query.where(VideoModel.name.ilike(pattern))
                count_q = count_q.where(VideoModel.name.ilike(pattern))

        total = (await self._session.execute(count_q)).scalar_one()

        if pagination:
            if pagination.sort_by:
                col = getattr(VideoModel, pagination.sort_by, None)
                if col is not None:
                    query = query.order_by(col.desc() if pagination.sort_desc else col.asc())
            query = query.offset(pagination.offset).limit(pagination.limit)

        result = await self._session.execute(query)
        models = result.scalars().all()
        return [self._to_domain(m) for m in models], total

    async def create(self, video: VideoDomain) -> VideoDomain:
        model = VideoModel(
            id=video.id,
            name=video.name,
            duration=video.duration,
            resolution_width=video.resolution_width,
            resolution_height=video.resolution_height,
            fps=video.fps,
            time_of_day=video.time_of_day,
            tracing=video.tracing,
            counter=video.counter,
            author_id=video.author_id,
            camera_id=video.camera_id,
            upload_time=video.upload_time,
            preview_url=video.preview_url
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def update(self, video: VideoDomain) -> VideoDomain:
        stmt = (
            update(VideoModel)
            .where(VideoModel.id == video.id)
            .values(
                name=video.name,
                duration=timedelta(seconds=video.duration) ,
                resolution_width=video.resolution_width,
                resolution_height=video.resolution_height,
                fps=video.fps,
                time_of_day=video.time_of_day,
                tracing=video.tracing,
                counter=video.counter,
                preview_url=video.preview_url
            )
            .execution_options(synchronize_session="fetch")
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return await self.get_by_id(video.id)

    async def delete(self, video_id: UUID) -> None:
        await self._session.execute(delete(VideoModel).where(VideoModel.id == video_id))
        await self._session.commit()

    async def enqueue_for_processing(self, video_id: UUID) -> None:
        queue_model = VideoProcessingQueue(
            id=uuid4(),
            video_id=video_id,
            status="Pending"
        )
        self._session.add(queue_model)
        await self._session.commit()

    async def update_processing_status(self, video_id: UUID, status: str) -> None:
        stmt = (
            update(VideoProcessingQueue)
            .where(VideoProcessingQueue.video_id == video_id)
            .values(status=status)
            .execution_options(synchronize_session="fetch")
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_next_in_queue(self) -> Optional[UUID]:
        result = await self._session.execute(
            select(VideoProcessingQueue.video_id)
            .where(VideoProcessingQueue.status == "Pending")
            .order_by(VideoProcessingQueue.created_at.asc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    def _to_domain(self, model: VideoModel) -> VideoDomain:
        return VideoDomain(
            id=model.id,
            name=model.name,
            duration=model.duration,
            resolution_width=model.resolution_width,
            resolution_height=model.resolution_height,
            fps=model.fps,
            time_of_day=model.time_of_day,
            tracing=model.tracing,
            counter=model.counter,
            author_id=model.author_id,
            camera_id=model.camera_id,
            upload_time=model.upload_time,
            preview_url=model.preview_url,
        )
