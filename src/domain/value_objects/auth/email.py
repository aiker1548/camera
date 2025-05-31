import re
from typing import Any

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
