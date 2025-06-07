from typing import Any, Optional

class LongitudeDescriptor:
    def __set_name__(self, owner: Any, name: str):
        self.name = name

    def __get__(self, instance: Any, owner: Any) -> Optional[float]:
        return instance.__dict__.get(self.name)

    def __set__(self, instance: Any, value: float) -> None:
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be between -180 and 180.")
        instance.__dict__[self.name] = value
