import uuid
from typing import Self, Dict, Any

from aiohttp import ClientSession
from .config import MlSettings

from application.video.interfaces.ml_client import MLBackendClient
from shared_kernel.loggers.main import get_infrastructure_logger


class MLBackendClientImpl(MLBackendClient):
    def __init__(self, config: MlSettings):
        self._logger = get_infrastructure_logger()
        self.config = config
        self.session: ClientSession | None = None

    async def __aenter__(self) -> Self:
        self.session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def start_video_processing(
            self,
            task_id: uuid.UUID,
            video_path: str,
            first_frame_path: str,
    ) -> Dict[str, Any]:
        """Запускает предобработку видео на ML backend"""
        if not self.session:
            self._logger.exception("Client session is not initialized, use context manager")
            raise

        url = f"{self.config.url}/api/start_processing"
        payload = {
            "task_id": str(task_id),
            "video_path": video_path,
            "first_frame_path": first_frame_path
        }

        async with self.session.post(url, json=payload) as response:
            response.raise_for_status()
            return await response.json()

    async def get_processing_status(self, task_id: str) -> Dict[str, Any]:
        """Получает статус предобработки видео"""
        if not self.session:
            raise RuntimeError("Client session is not initialized, use context manager")

        url = f"{self.config.url}/api/processing_status/{task_id}"

        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.json()