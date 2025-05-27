from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.infrastructure.db_user_repository import UserRepository
from src.auth.services import AuthService
from src.dependencies.db import get_async_session

async def get_auth_service(
    db: AsyncSession = Depends(get_async_session)
) -> AuthService:
    user_repo = UserRepository(db)
    return AuthService(user_repo=user_repo)