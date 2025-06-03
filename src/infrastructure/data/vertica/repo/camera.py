from typing import Generator

from pydantic import BaseModel

from infrastructure.data.vertica.client import SyncVertica
from infrastructure.data.vertica.convertors import convert_camera_entity_to_dto
from application.camera.dto.camera import CameraDTO
from shared_kernel.loggers.main import get_infrastructure_logger

logger = get_infrastructure_logger()


class CameraSourceReader:
    def __init__(self, client: SyncVertica):
        self.client = client

    def fetch_all(self) -> list[CameraDTO]:
        """
        Получает список всех активных камер (period_to_dt = '9999-12-31')
        """

        query = """
        SELECT camera_id, camera_class_cd, camera_class, id, model, camera_name,
               camera_place, camera_place_cd, serial_number, camera_type_cd, camera_type,
               camera_latitude, camera_longitude, archive, azimuth, violations,
               violation_limit, process_dttm
        FROM codd_data.d_camera
        WHERE period_to_dt = '9999-12-31'
        AND camera_name IS NOT NULL 
        AND camera_longitude IS NOT NULL
        AND camera_latitude IS NOT NULL
        OFFSET 1
        """

        result = self.client.fetch_many(query=query)
        return [convert_camera_entity_to_dto(row) for row in result]

    def fetch_by_chunks(self, chunk_size: int = 100) -> Generator[list[CameraDTO], None, None]:
        """
        Генератор для загрузки данных кусками
        """
        query = """
        SELECT COUNT(*) AS cnt 
        FROM codd_data.d_camera 
        WHERE period_to_dt = '9999-12-31'
        AND camera_name IS NOT NULL 
        AND camera_longitude IS NOT NULL
        AND camera_latitude IS NOT NULL
        """
        total_count = self.client.fetch_one(query=query)["cnt"]

        for offset in range(0, total_count, chunk_size):
            yield self.fetch_chunk(limit=chunk_size, offset=offset)

    def fetch_chunk(self, limit: int, offset: int) -> list[CameraDTO]:
        """
        Получает часть списка камер
        """
        query = f"""
        SELECT camera_id, camera_class_cd, camera_class, id, model, camera_name,
               camera_place, camera_place_cd, serial_number, camera_type_cd, camera_type,
               camera_latitude, camera_longitude, archive, azimuth, violations,
               violation_limit, process_dttm
        FROM codd_data.d_camera
        WHERE period_to_dt = '9999-12-31'
        AND camera_name IS NOT NULL
        AND camera_longitude IS NOT NULL
        AND camera_latitude IS NOT NULL
        ORDER BY id
        LIMIT {limit} OFFSET {offset}
        """
        result = self.client.fetch_many(query=query)
        return [convert_camera_entity_to_dto(row) for row in result]

    def fetch_districts_all(self):
        data_query = "SELECT * FROM dict.d_division_district"
        rows = self.client.fetch_many(data_query)

        return rows
