from typing import Any, Optional


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