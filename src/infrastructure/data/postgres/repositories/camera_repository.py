from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from sqlalchemy.orm import aliased, joinedload

from src.infrastructure.data.postgres.models.camera import Camera as CameraModel
from src.infrastructure.data.postgres.models.video import Video 
from src.domain.camera.entities.camera import Camera
from src.application.camera.interfaces.persistence.repo import AbstractCameraRepository
from src.application.camera.dto.filters import CameraFilters
from src.domain.video.entities.video import Video as VideoDomain

class PostgresCameraRepository(AbstractCameraRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, filters: CameraFilters) -> List[Camera]:
        # Создаем запрос с жадной загрузкой видео
        query = select(CameraModel).options(joinedload(CameraModel.videos))

        # Применение фильтров
        if filters.camera_id__subtext is not None:
            query = query.where(CameraModel.camera_id.ilike(f"%{filters.camera_id__subtext}%"))
        if filters.camera_place__subtext is not None:
            query = query.where(CameraModel.camera_place.ilike(f"%{filters.camera_place__subtext}%"))
        if filters.camera_model__in != []:
            query = query.where(CameraModel.model.in_(filters.camera_model__in))
        if filters.camera_type__in != []:
            query = query.where(CameraModel.camera_type.in_(filters.camera_type__in))
        if filters.camera_class__in != []:
            query = query.where(CameraModel.camera_class.in_(filters.camera_class__in))
        
        # Фильтры по количеству видео
        if (filters.count_videos__le is not None) or (filters.count_videos__ge is not None):
            video_alias = aliased(Video)
            query = query.outerjoin(video_alias, CameraModel.videos)
            query = query.group_by(CameraModel.id)
            if filters.count_videos__le is not None:
                query = query.having(func.count(video_alias.id) <= filters.count_videos__le)
            if filters.count_videos__ge is not None:
                query = query.having(func.count(video_alias.id) >= filters.count_videos__ge)

        # Выполнение запроса
        result = await self.session.execute(query)
        models = result.unique().scalars().all() 
        return [self._to_domain(m) for m in models]

    async def get_by_id(self, camera_id: UUID) -> Optional[Camera]:
        result = await self.session.execute(
            select(CameraModel).where(CameraModel.id == camera_id)
        )
        model = result.scalar_one_or_none()
        await self.session.refresh(model, attribute_names=["videos"])
        return self._to_domain(model) if model else None

    async def create(self, camera: Camera) -> Camera:
        model = CameraModel(**camera.to_dict())
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        await self.session.refresh(model, attribute_names=["videos"])
        return self._to_domain(model)

    async def delete(self, camera_id: UUID) -> None:
        await self.session.execute(delete(CameraModel).where(CameraModel.id == camera_id))
        await self.session.commit()

    async def update(self, camera_id: UUID, updated_data: dict) -> Optional[Camera]:
        model = await self.session.get(CameraModel, camera_id)
        if model:
            for key, value in updated_data.items():
                if key == "camera_id":
                    model.camera_id = value
                elif key == "camera_class_cd":
                    model.camera_class_cd = value
                elif key == "camera_class":
                    model.camera_class = value
                elif key == "model":
                    model.model = value
                elif key == "camera_name":
                    model.camera_name = value
                elif key == "camera_place":
                    model.camera_place = value
                elif key == "camera_place_cd":
                    model.camera_place_cd = value
                elif key == "serial_number":
                    model.serial_number = value
                elif key == "camera_type_cd":
                    model.camera_type_cd = value
                elif key == "camera_type":
                    model.camera_type = value
                elif key == "camera_latitude":
                    model.camera_latitude = value
                elif key == "camera_longitude":
                    model.camera_longitude = value
                elif key == "archive":
                    model.archive = value
                elif key == "azimuth":
                    model.azimuth = value
            await self.session.commit()
            await self.session.refresh(model)
            await self.session.refresh(model, attribute_names=["videos"])
            return self._to_domain(model)
        return None

    def _to_domain(self, model: CameraModel) -> Camera:
        return Camera(
            id=model.id,
            camera_id=model.camera_id,
            camera_class_cd=model.camera_class_cd,
            camera_class=model.camera_class,
            model=model.model,
            camera_name=model.camera_name,
            camera_place=model.camera_place,
            camera_place_cd=model.camera_place_cd,
            serial_number=model.serial_number,
            camera_type_cd=model.camera_type_cd,
            camera_type=model.camera_type,
            camera_latitude=model.camera_latitude,
            camera_longitude=model.camera_longitude,
            archive=model.archive,
            azimuth=model.azimuth,
            process_dttm=model.process_dttm,
            videos=[VideoDomain.from_orm(v) for v in model.videos]
        )
    
