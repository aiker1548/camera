from abc import ABC, abstractmethod
from typing import List, Optional

from uuid import UUID

from src.domain.camera.entities.camera import Camera

class AbstractCameraRepository(ABC):
    @abstractmethod
    async def get_all(self, **filters) -> List[Camera]:
        """Получить список всех камер с возможностью фильтрации."""
        ...

    @abstractmethod
    async def get_by_id(self, camera_id: UUID) -> Optional[Camera]:
        """Получить камеру по её идентификатору."""
        ...

    @abstractmethod
    async def create(self, camera: Camera) -> Camera:
        """Создать новую камеру."""
        ...

    @abstractmethod
    async def delete(self, camera_id: UUID) -> None:
        """Удалить камеру по идентификатору."""
        ...

    @abstractmethod
    async def update(self, camera_id: UUID, updated_data: dict) -> Optional[Camera]:
        """Обновить данные камеры по идентификатору."""
        ...