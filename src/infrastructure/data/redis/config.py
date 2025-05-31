from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    host: str = "localhost:6379"
    db: int = 0

    @property
    def url(self):
        return f"redis://{self.host}/{self.db}"
