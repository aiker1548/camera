
from pydantic_settings import BaseSettings


class FileUploadSettings(BaseSettings):
    max_file_size: int
    allowed_extensions: list[str]
    expiration_seconds: int

    max_total_errors: int = 10
