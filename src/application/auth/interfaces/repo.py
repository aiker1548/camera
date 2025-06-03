from abc import ABC, abstractmethod
from typing import Optional

from src.domain.auth.entities.user import User as DomainUser

class IUserRepository(ABC):
    """
    Интерфейс репозитория пользователей.
    Определяет контракты для работы с доменной сущностью User.
    """

    @abstractmethod
    async def add(self, user: DomainUser) -> None:
        """Сохраняет нового пользователя."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[DomainUser]:
        """Возвращает пользователя по email или None, если не найден."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[DomainUser]:
        """Возвращает пользователя по ID или None, если не найден."""
        raise NotImplementedError
    