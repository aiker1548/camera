from fastapi import APIRouter, Depends, UploadFile, Form
from uuid import UUID
from src.di.video.storage_service import VideoStorageService

from src.presentation.api.routes.video.deps.video import get_video_storage_service 

router = APIRouter(prefix="/videos", tags=["Videos"])

@router.post("/")
async def upload_video(
    file: UploadFile,
    camera_id: UUID = Form(...),
    author_id: UUID = Form(...),
    storage_service: VideoStorageService = Depends(get_video_storage_service),
):
    video_id = await storage_service.upload_file_and_enqueue(file, camera_id, author_id)
    return {"video_id": video_id}
