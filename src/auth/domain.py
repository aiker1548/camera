import re
import uuid
from datetime import datetime, timedelta
from typing import Optional, Any


# --- DESCRIPTORS FOR FIELD VALIDATION ---
class EmailDescriptor:
    """Дескриптор для валидации email."""
    EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    def __set_name__(self, owner: Any, name: str):
        self.name = name

    def __get__(self, instance: Any, owner: Any) -> str:
        return instance.__dict__.get(self.name)

    def __set__(self, instance: Any, value: str) -> None:
        if not value or not self.EMAIL_REGEX.match(value):
            raise ValueError(f"Invalid email format: {value}")
        instance.__dict__[self.name] = value.lower()


class NonEmptyStringDescriptor:
    """Дескриптор для строковых полей, которые не должны быть пустыми."""
    def __set_name__(self, owner: Any, name: str):
        self.name = name

    def __get__(self, instance: Any, owner: Any) -> Optional[str]:
        return instance.__dict__.get(self.name)

    def __set__(self, instance: Any, value: Optional[str]) -> None:
        if value is not None:
            text = value.strip()
            if not text:
                raise ValueError(f"{self.name} must be a non-empty string")
            instance.__dict__[self.name] = text
        else:
            instance.__dict__[self.name] = None


# --- DOMAIN ENTITIES ---
class User:
    """
    Доменная сущность "Пользователь".

    Поля валидируются через дескрипторы.
    """
    email = EmailDescriptor()
    fio = NonEmptyStringDescriptor()
    org = NonEmptyStringDescriptor()

    MIN_PASSWORD_HASH_LENGTH = 8

    def __init__(
        self,
        email: str,
        password_hash: str,
        fio: str,
        org: Optional[str] = None
    ):
        self.id: uuid.UUID = uuid.uuid4()
        self.email = email         # через EmailDescriptor
        self.password_hash: str = password_hash
        self.fio = fio             # через NonEmptyStringDescriptor
        self.org = org             # через NonEmptyStringDescriptor
        self.created_at: datetime = datetime.time()

    def change_password(self, new_password_hash: str):
        """
        Изменяет хэш пароля. Проверяет минимальную длину.
        """
        if not new_password_hash or len(new_password_hash) < self.MIN_PASSWORD_HASH_LENGTH:
            raise ValueError("Password hash is too short or invalid")
        self.password_hash = new_password_hash

    def update_profile(self, fio: Optional[str] = None, org: Optional[str] = None):
        """
        Обновляет ФИО и организацию через дескрипторы.
        """
        if fio is not None:
            self.fio = fio
        if org is not None:
            self.org = org


# --- VALUE OBJECTS FOR TOKENS ---
class AccessToken:
    """
    Value Object для краткоживущего Access Token.

    Атрибуты:
        token: строка токена.
        expires_at: момент истечения.
    """
    def __init__(self, token: str, ttl_seconds: int = 3600):  # 1 час по умолчанию
        if not token or not token.strip():
            raise ValueError("Access token must be provided")
        self.token: str = token
        self.expires_at: datetime = datetime.utcnow() + timedelta(seconds=ttl_seconds)

    def is_expired(self) -> bool:
        return datetime.time() >= self.expires_at

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AccessToken):
            return False
        return self.token == other.token and self.expires_at == other.expires_at


class RefreshToken:
    """
    Value Object для долгоживущего Refresh Token.

    См. AccessToken, но с другим TTL.
    """
    def __init__(self, token: str, ttl_seconds: int = 7 * 24 * 3600):  # 7 дней
        if not token or not token.strip():
            raise ValueError("Refresh token must be provided")
        self.token: str = token
        self.expires_at: datetime = datetime.utcnow() + timedelta(seconds=ttl_seconds)

    def is_expired(self) -> bool:
        return datetime.time() >= self.expires_at

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, RefreshToken):
            return False
        return self.token == other.token and self.expires_at == other.expires_at
