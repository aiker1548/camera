from uuid import UUID
from typing import List, Optional

from src.application.camera.interfaces.persistence.repo import AbstractCameraRepository
from src.domain.camera.entities.camera import Camera
from src.application.camera.dto.filters import CameraFilters


class CameraService:
    def __init__(self, repository: AbstractCameraRepository):
        self.repository = repository

    async def get_cameras_geojson(self, filters: CameraFilters) -> dict:
            cameras = await self.repository.get_all(filters)
            features = []
            for camera in cameras:
                feature = {
                    "type": "Feature",
                    "properties": {
                        "camera_id": camera.camera_id,
                        "has_video": (True if camera.videos else False)
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            camera.camera_longitude,
                            camera.camera_latitude
                        ]
                    }
                }
                features.append(feature)
            return {
                "type": "FeatureCollection",
                "features": features
            }
        

    async def get_camera(self, camera_id: UUID) -> Optional[Camera]:
        return await self.repository.get_by_id(camera_id)

    async def create_camera(self, camera: Camera) -> Camera:
        return await self.repository.create(camera)

    async def delete_camera(self, camera_id: UUID) -> None:
        await self.repository.delete(camera_id)

    async def update_camera(self, camera_id: UUID, updated_data: dict) -> Optional[Camera]:
        return await self.repository.update(camera_id, updated_data)