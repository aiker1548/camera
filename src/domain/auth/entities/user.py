import dataclasses
from datetime import datetime
from typing import Optional
import uuid

from src.domain.value_objects.auth.email import EmailDescriptor
from src.domain.value_objects.auth.string import NonEmptyStringDescriptor


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
        id: Optional[uuid.UUID] = None,
        org: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.id: uuid.UUID = id or uuid.uuid4()
        self.email = email         
        self.password_hash: str = password_hash
        self.fio = fio            
        self.org = org            
        self.created_at: datetime = created_at or datetime.now()

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
