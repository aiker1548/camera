from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.data.postgres.repositories.user_repository import UserRepository
from src.di.auth.services import AuthService
from src.presentation.api.routes.tools.dependencies.tools_dep import get_async_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")


async def get_auth_service(
    db: AsyncSession = Depends(get_async_session)
) -> AuthService:
    user_repo = UserRepository(db)
    return AuthService(user_repo=user_repo)


async def get_current_user(
        token: str = Depends(oauth2_scheme)):
    pass
