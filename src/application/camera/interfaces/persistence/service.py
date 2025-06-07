from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, Dict, Any

from src.application.camera.dto.filters import CameraFilters
from src.domain.camera.entities.camera import Camera

class AbstractCameraService(ABC):
    @abstractmethod
    async def get_cameras_geojson(self, filters: CameraFilters) -> Dict[str, Any]:
        """
        Retrieve cameras matching filters and return a GeoJSON FeatureCollection.
        """
        pass

    @abstractmethod
    async def get_camera(self, camera_id: UUID) -> Optional[Camera]:
        """
        Fetch a single camera entity by its UUID.
        """
        pass

    @abstractmethod
    async def create_camera(self, camera: Camera) -> Camera:
        """
        Create a new camera entity.
        """
        pass

    @abstractmethod
    async def update_camera(self, camera_id: UUID, updated_data: Dict[str, Any]) -> Optional[Camera]:
        """
        Update fields of an existing camera by its UUID.
        """
        pass

    @abstractmethod
    async def delete_camera(self, camera_id: UUID) -> None:
        """
        Delete a camera entity by its UUID.
        """
        pass
