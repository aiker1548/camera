from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field
from uuid import UUID

class CameraBase(BaseModel):
    camera_id: Optional[str] = Field(None, description="Номер камеры")
    camera_class_cd: Optional[int] = Field(None, description="Идентификатор класса камеры")
    camera_class: Optional[str] = Field(None, description="Класс камеры")
    model: Optional[str] = Field(None, description="Модель")
    camera_name: str = Field(..., description="Название камеры")
    camera_place: Optional[str] = Field(None, description="Адрес")
    camera_place_cd: Optional[int] = Field(None, description="Идентификатор адреса")
    serial_number: Optional[str] = Field(None, description="Серийный номер")
    camera_type_cd: Optional[int] = Field(None, description="Идентификатор типа камеры")
    camera_type: Optional[str] = Field(None, description="Тип камеры")
    camera_latitude: float = Field(..., description="Широта")
    camera_longitude: float = Field(..., description="Долгота")
    archive: Optional[bool] = Field(False, description="Признак архивной записи")
    azimuth: Optional[int] = Field(None, description="Азимут")

class CameraCreate(CameraBase):
    pass

class CameraRead(CameraBase):
    id: UUID
    process_dttm: Optional[datetime] = None

    class Config:
        orm_mode = True

class CameraUpdate(CameraBase):
    pass
