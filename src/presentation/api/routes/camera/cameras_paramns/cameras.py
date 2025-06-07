from fastapi import Query
from pydantic import BaseModel, Field

from src.application.camera.dto.filters import CameraFilters


class FilterCamerasParams(BaseModel):
    camera_id__subtext: str | None = Query(None)
    camera_place__subtext: str | None = Query(None)
    count_videos__le: int | None = Query(None)
    count_videos__ge: int | None = Query(None)
    camera_model__in: list[str] = Field(Query(default_factory=list, description="Фильтр по модели камеры"))
    camera_type__in: list[str] = Field(Query(default_factory=list, description="Фильтр по типу камеры"))
    camera_class__in: list[str] = Field(Query(default_factory=list, description="Фильтр по классу камеры"))

    def build_camera_filters(self) -> CameraFilters:
        return CameraFilters(
            camera_id__subtext=self.camera_id__subtext,
            camera_place__subtext=self.camera_place__subtext,
            count_videos__le=self.count_videos__le,
            count_videos__ge=self.count_videos__ge,
            camera_model__in=self.camera_model__in,
            camera_type__in=self.camera_type__in,
            camera_class__in=self.camera_class__in,
        )
