from typing import Optional
from datetime import datetime
import uuid

from src.domain.value_objects.camera.latitube import LatitudeDescriptor
from src.domain.value_objects.camera.longitude import LongitudeDescriptor
from src.domain.value_objects.camera.string import NonEmptyStringDescriptor
from src.infrastructure.data.postgres.models.camera import Camera as CameraModel


class Camera:
    """
    Доменная сущность: Камера наблюдения.
    """

    camera_id = NonEmptyStringDescriptor()
    camera_class_cd: Optional[int] = None
    camera_class = NonEmptyStringDescriptor()
    model = NonEmptyStringDescriptor()
    camera_name = NonEmptyStringDescriptor()
    camera_place = NonEmptyStringDescriptor()
    camera_place_cd: Optional[int] = None
    serial_number = NonEmptyStringDescriptor()
    camera_type_cd: Optional[int] = None
    camera_type = NonEmptyStringDescriptor()
    camera_latitude = LatitudeDescriptor()
    camera_longitude = LongitudeDescriptor()
    archive: bool = False
    azimuth: Optional[int] = None
    process_dttm: Optional[datetime] = None

    def __init__(
        self,
        id: Optional[uuid.UUID] = None,
        camera_id: Optional[str] = None,
        camera_class_cd: Optional[int] = None,
        camera_class: Optional[str] = None,
        model: Optional[str] = None,
        camera_name: Optional[str] = None,
        camera_place: Optional[str] = None,
        camera_place_cd: Optional[int] = None,
        serial_number: Optional[str] = None,
        camera_type_cd: Optional[int] = None,
        camera_type: Optional[str] = None,
        camera_latitude: Optional[float] = None,
        camera_longitude: Optional[float] = None,
        archive: bool = False,
        azimuth: Optional[int] = None,
        process_dttm: Optional[datetime] = None,
    ):
        self.id = id or uuid.uuid4()
        self.camera_id = camera_id or ""
        self.camera_class_cd = camera_class_cd
        self.camera_class = camera_class or ""
        self.model = model or ""
        self.camera_name = camera_name or ""
        self.camera_place = camera_place or ""
        self.camera_place_cd = camera_place_cd
        self.serial_number = serial_number or ""
        self.camera_type_cd = camera_type_cd
        self.camera_type = camera_type or ""
        self.camera_latitude = camera_latitude
        self.camera_longitude = camera_longitude
        self.archive = archive
        self.azimuth = azimuth
        self.process_dttm = process_dttm or datetime.now()

    @classmethod
    def from_orm(cls, orm_obj: CameraModel) -> "Camera":
        return cls(
            id=orm_obj.id,
            camera_id=orm_obj.camera_id,
            camera_class_cd=orm_obj.camera_class_cd,
            camera_class=orm_obj.camera_class,
            model=orm_obj.model,
            camera_name=orm_obj.camera_name,
            camera_place=orm_obj.camera_place,
            camera_place_cd=orm_obj.camera_place_cd,
            serial_number=orm_obj.serial_number,
            camera_type_cd=orm_obj.camera_type_cd,
            camera_type=orm_obj.camera_type,
            camera_latitude=orm_obj.camera_latitude,
            camera_longitude=orm_obj.camera_longitude,
            archive=orm_obj.archive,
            azimuth=orm_obj.azimuth,
            process_dttm=orm_obj.process_dttm,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "camera_id": self.camera_id,
            "camera_class_cd": self.camera_class_cd,
            "camera_class": self.camera_class,
            "model": self.model,
            "camera_name": self.camera_name,
            "camera_place": self.camera_place,
            "camera_place_cd": self.camera_place_cd,
            "serial_number": self.serial_number,
            "camera_type_cd": self.camera_type_cd,
            "camera_type": self.camera_type,
            "camera_latitude": self.camera_latitude,
            "camera_longitude": self.camera_longitude,
            "archive": self.archive,
            "azimuth": self.azimuth,
            "process_dttm": self.process_dttm,
        }