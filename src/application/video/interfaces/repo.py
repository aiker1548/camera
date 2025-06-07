from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from src.domain.video.entities.video import Video  
from src.application.video.dto.video_filters import VideoFiltersDTO 
from src.application.video.dto.pagination import PaginationParams 

class AbstractVideoRepository(ABC):
    """
    Абстрактный репозиторий для работы с сущностью Video.
    Внедряется в сервисы/используется в бизнес-логике.
    """

    @abstractmethod
    async def get_by_id(self, video_id: UUID) -> Optional[Video]:
        """
        Получить видео по его UUID.
        Возвращает доменную сущность Video или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def list_all(self, 
                       filters: Optional[VideoFiltersDTO] = None, 
                       pagination: Optional[PaginationParams] = None
                      ) -> Tuple[List[Video], int]:
        """
        Вернуть список Video, применив опциональные фильтры и пагинацию.
        Возвращает кортеж (список сущностей, общее количество под фильтром).
        VideoFiltersDTO содержит:
          - date_from: Optional[datetime]
          - date_to: Optional[datetime]
          - duration_from: Optional[timedelta]
          - duration_to: Optional[timedelta]
          - time_of_day: Optional[List[TimeOfDay]]
          - tracing: Optional[List[TracingStatus]]
          - author_ids: Optional[List[UUID]]
          - camera_ids: Optional[List[UUID]]
          - name_substring: Optional[str]
        PaginationParams содержит:
          - offset: int
          - limit: int
          - sort_by: Optional[str] (например, "upload_time" или "duration")
          - sort_desc: bool
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, video: Video) -> Video:
        """
        Создать новую запись Video в БД.
        Возвращает сохранённую сущность (с уже заполненным id, upload_time и т.д.).
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, video: Video) -> Video:
        """
        Обновить существующее Video (например, после фоновой обработки).
        Возвращает обновлённую сущность.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, video_id: UUID) -> None:
        """
        Удалить видео по ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def enqueue_for_processing(self, video_id: UUID) -> None:
        """
        Поставить запись о видео в очередь обработки (в таблицу video_processing_queue),
        присвоить status='Pending'.
        """
        raise NotImplementedError

    @abstractmethod
    async def update_processing_status(self, 
                                       video_id: UUID, 
                                       status: str 
                                      ) -> None:
        """
        Обновить статус обработки видео в таблице очереди.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_next_in_queue(self) -> Optional[UUID]:
        """
        Взять ID следующего видео из очереди со статусом 'Pending' (по порядку created_at).
        Возвращает либо UUID видео, либо None, если очередь пуста.
        """
        raise NotImplementedError
