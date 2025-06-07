from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CameraFilters:
    camera_id__subtext: str 
    camera_place__subtext: str 
    count_videos__le: int 
    count_videos__ge: int 
    camera_model__in: list[str] 
    camera_type__in: list[str] 
    camera_class__in: list[str] 

