from fastapi import APIRouter, Depends, UploadFile, Form
from uuid import UUID

from src.application.video.dto.video_filters import VideoFiltersDTO
from src.application.video.dto.pagination import PaginationParams 
from src.application.video.service.storage_service import VideoStorageService
from src.application.video.service.service import VideoService
from src.presentation.api.routes.video.deps.video import get_video_storage_service
from src.presentation.api.routes.video.deps.video import get_video_service

router = APIRouter(prefix="/videos", tags=["Videos"])

@router.post("/")
async def upload_video(
    file: UploadFile,
    camera_id: UUID = Form(...),
    author_id: UUID = Form(...),
    storage_service: VideoStorageService = Depends(get_video_storage_service),
):
    video_id = await storage_service.upload_file_and_enqueue(file, camera_id, author_id)
    return video_id


@router.get("/")
async def get_videos(
    video_params: VideoFiltersDTO = Depends(VideoFiltersDTO.as_query_dep),
    pagination: PaginationParams = Depends(),
    video_service: VideoService = Depends(get_video_service)
):
    videos = await video_service.list_videos(filters=video_params, pagination=pagination)
    return videos
    
