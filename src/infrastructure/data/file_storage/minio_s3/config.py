
from pydantic_settings import BaseSettings


class MinioS3Settings(BaseSettings):
    bucket: str
    ssl: bool
    host: str
    port: int
    user: str
    password: str
