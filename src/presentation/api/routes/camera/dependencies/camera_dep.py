from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.camera.service.service import CameraService
from src.infrastructure.data.postgres.repositories.camera_repository import PostgresCameraRepository
from src.presentation.api.routes.tools.dependencies.tools_dep import get_async_session


def get_service(session: AsyncSession = Depends(get_async_session)) -> CameraService:
    repo = PostgresCameraRepository(session)
    return CameraService(repo)
