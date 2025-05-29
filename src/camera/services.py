from uuid import UUID
from typing import List, Optional
from src.camera.repositories import AbstractCameraRepository
from src.camera.domain import Camera


class CameraService:
    def __init__(self, repository: AbstractCameraRepository):
        self.repository = repository

    async def list_cameras(self, **filters) -> List[Camera]:
        return await self.repository.get_all(**filters)

    async def get_camera(self, camera_id: UUID) -> Optional[Camera]:
        return await self.repository.get_by_id(camera_id)

    async def create_camera(self, camera: Camera) -> Camera:
        return await self.repository.create(camera)

    async def delete_camera(self, camera_id: UUID) -> None:
        await self.repository.delete(camera_id)

    async def update_camera(self, camera_id: UUID, updated_data: dict) -> Optional[Camera]:
        return await self.repository.update(camera_id, updated_data)