from datetime import datetime
from typing import Tuple
from src.auth.domain import User as DomainUser
from src.auth.repositories import IUserRepository
from src.auth.infrastructure.password_hasher import hash_password, verify_password
from src.auth.infrastructure.jwt_provider import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from src.auth.infrastructure.db_user_repository import UserRepository
from src.auth.schemas import UserCreate, TokenPair, TokenRefresh
#from src.shared.messaging.producer import send_event

class AuthService:
    """
    Сервис аутентификации и управления пользователями.
    """
    def __init__(
        self,
        user_repo: IUserRepository = None
    ):
        self.user_repo: IUserRepository = user_repo or UserRepository()

    async def register(self, dto: UserCreate) -> None:
        # Проверим, что пользователя с таким email ещё нет
        existing_user = await self.user_repo.get_by_email(dto.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        # Хешируем пароль и создаём доменного пользователя
        pwd_hash = hash_password(dto.password)
        user = DomainUser(
            email=dto.email,
            password_hash=pwd_hash,
            fio=dto.fio,
            org=dto.org,
        )
        # Сохраняем в репозитории
        await self.user_repo.add(user)
        # Отправляем событие о регистрации (пример)
        #await send_event("user.registered", {"user_id": str(user.id), "email": user.email})

    async def login(self, email: str, password: str) -> TokenPair:
        user = await self.user_repo.get_by_email(email)
        if user is None:
            raise ValueError("Invalid credentials")
        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")
        # Генерируем токены
        access_token, access_exp = create_access_token(subject=str(user.id))
        refresh_token, refresh_exp = create_refresh_token(subject=str(user.id))
        return TokenPair(
            access_token=access_token,
            access_expires_at=access_exp,
            refresh_token=refresh_token,
            refresh_expires_at=refresh_exp,
        )

    async def refresh(self, dto: TokenRefresh) -> TokenPair:
        payload = decode_token(dto.refresh_token)
        if payload is None or "sub" not in payload:
            raise ValueError("Invalid refresh token")
        user_id = payload["sub"]
        # Проверяем, есть ли пользователь
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        # Генерируем новую пару токенов
        access_token, access_exp = create_access_token(subject=user_id)
        refresh_token, refresh_exp = create_refresh_token(subject=user_id)
        return TokenPair(
            access_token=access_token,
            access_expires_at=access_exp,
            refresh_token=refresh_token,
            refresh_expires_at=refresh_exp,
        )