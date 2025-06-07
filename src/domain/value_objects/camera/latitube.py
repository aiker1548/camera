from typing import Any, Optional

class LatitudeDescriptor:
    def __set_name__(self, owner: Any, name: str):
        self.name = name

    def __get__(self, instance: Any, owner: Any) -> Optional[float]:
        return instance.__dict__.get(self.name)

    def __set__(self, instance: Any, value: float) -> None:
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be between -90 and 90.")
        instance.__dict__[self.name] = value