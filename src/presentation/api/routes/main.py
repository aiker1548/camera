from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.presentation.api.routes.camera.camera import router as camera_router
from src.presentation.api.routes.auth.auth import router as user_router
from src.presentation.api.routes.video.video import router as video_router  

from src.infrastructure.data.postgres.base import AsyncSessionMaker
from src.infrastructure.middlewares.db_session import DBSessionMiddleware

from src.shared_kernel.config import config
from src.presentation.worker.tasks.videos import start_video_consumer


def create_app():
    # ----------------------------------------
    # 1. Устанавливаем SQLAlchemy-движок (через Middleware)
    # ----------------------------------------
    # Предполагается, что AsyncSessionMaker внутри настраивает AsyncEngine из config.DATABASE_URL
    app = FastAPI(version="1.0.0")

    # ----------------------------------------
    # 2. CORS
    # ----------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ----------------------------------------
    # 3. DBSessionMiddleware (создаёт AsyncSession на каждый запрос)
    # ----------------------------------------
    app.add_middleware(DBSessionMiddleware, session_maker=AsyncSessionMaker)

    # ----------------------------------------
    # 4. Подключаем роутеры
    # ----------------------------------------
    app.include_router(user_router, tags=["users"])
    app.include_router(camera_router, prefix="/cameras", tags=["Cameras"])
    app.include_router(video_router, tags=["Videos"])

    # ----------------------------------------
    # 5. Событие startup: запускаем консьюмера
    # ----------------------------------------
    @app.on_event("startup")
    async def on_startup():
        print("[App] Starting RabbitMQ consumer")
        start_video_consumer()
    



    return app


app = create_app()

