from abc import ABC, abstractmethod
from typing import Optional
from src.application.auth.dto.auth_dto import UserCreate
from src.application.auth.dto.token_dto import TokenPair, TokenRefresh

class AbstractAuthService(ABC):
    @abstractmethod
    async def register(self, dto: UserCreate) -> None:
        """
        Register a new user. Raises on duplicates.
        """
        pass

    @abstractmethod
    async def login(self, email: str, password: str) -> TokenPair:
        """
        Authenticate user with email and password, returning access and refresh tokens.
        """
        pass

    @abstractmethod
    async def refresh(self, dto: TokenRefresh) -> TokenPair:
        """
        Refresh authentication tokens given a valid refresh token.
        """
        pass