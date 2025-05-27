from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth.routes import router as user_router
from src.middlewares import DBSessionMiddleware
from src.shared.database import AsyncSessionMaker

def create_app(session_maker=AsyncSessionMaker):
    app = FastAPI(title="Library Catalog API", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(DBSessionMiddleware, session_maker=session_maker)
    app.include_router(user_router, tags=["users"])
    return app

app = create_app()