from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from src.application.camera.dto.camera import CameraCreate, CameraRead, CameraUpdate
from src.di.cameras.service import CameraService
from src.domain.camera.entities.camera import Camera
from src.presentation.api.routes.camera.dependencies.camera_dep import get_service

router = APIRouter(prefix="/cameras", tags=["Cameras"])


@router.get("/", response_model=List[CameraRead])
async def list_cameras(
    name: str | None = None,
    type: str | None = None,
    class_: str | None = None,
    model: str | None = None,
    service: CameraService = Depends(get_service)
):
    filters = {}
    if name:
        filters["name"] = name
    if type:
        filters["type"] = type
    if class_:
        filters["class_"] = class_
    if model:
        filters["model"] = model
    return await service.list_cameras(**filters)

@router.get("/geojson", response_model=dict)
async def get_cameras_geojson(service: CameraService = Depends(get_service)):
    cameras = await service.list_cameras()
    features = []
    for camera in cameras:
        feature = {
            "type": "Feature",
            "properties": {
                "camera_id": camera.camera_id,        
                "has_video": False
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

@router.get("/{camera_id}", response_model=CameraRead)
async def get_camera(camera_id: UUID, service: CameraService = Depends(get_service)):
    camera = await service.get_camera(camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera



@router.post("/", response_model=CameraRead, status_code=201)
async def create_camera(data: CameraCreate, service: CameraService = Depends(get_service)):
    camera = Camera(
        camera_id=data.camera_id,
        camera_class_cd=data.camera_class_cd,
        camera_class=data.camera_class,
        model=data.model,
        camera_name=data.camera_name,
        camera_place=data.camera_place,
        camera_place_cd=data.camera_place_cd,
        serial_number=data.serial_number,
        camera_type_cd=data.camera_type_cd,
        camera_type=data.camera_type,
        camera_latitude=data.camera_latitude,
        camera_longitude=data.camera_longitude,
        archive=data.archive if data.archive is not None else False,
        azimuth=data.azimuth,
    )
    return await service.create_camera(camera)



@router.delete("/{camera_id}", status_code=204)
async def delete_camera(camera_id: UUID, service: CameraService = Depends(get_service)):
    await service.delete_camera(camera_id)



@router.put("/{camera_id}", response_model=CameraRead)
async def update_camera(
    camera_id: UUID,
    data: CameraUpdate,
    service: CameraService = Depends(get_service)
):
    camera = await service.get_camera(camera_id)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    updated_camera = await service.update_camera(camera_id, data.model_dump())
    return updated_camera



