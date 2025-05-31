from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime

from src.infrastructure.data.postgres.base import Base

class CameraModel(Base):
    __tablename__ = "d_camera"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="Идентификатор камеры")
    camera_id = Column(String, nullable=False, comment="Номер камеры")
    camera_class_cd = Column(Integer, comment="Идентификатор класса камеры")
    camera_class = Column(String, comment="Класс камеры")
    model = Column(String, comment="Модель")
    camera_name = Column(String, nullable=False, comment="Название камеры")
    camera_place = Column(String, comment="Адрес")
    camera_place_cd = Column(Integer, comment="Идентификатор адреса")
    serial_number = Column(String, comment="Серийный номер")
    camera_type_cd = Column(Integer, comment="Идентификатор типа камеры")
    camera_type = Column(String, comment="Тип камеры")
    camera_latitude = Column(Float, comment="Широта")
    camera_longitude = Column(Float, comment="Долгота")
    archive = Column(Boolean, default=False, comment="Признак архивной записи")
    azimuth = Column(Integer, comment="Азимут")
    process_dttm = Column(DateTime, default=datetime.utcnow, comment="Дата и время добавления записи")
