from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    host: str
    username: str
    password: SecretStr
    database: str
    echo: bool = True

    @property
    def full_url(self) -> PostgresDsn:
        return PostgresDsn(
            f"postgresql+asyncpg://{self.username}:{self.password.get_secret_value()}@{self.host}/{self.database}"
        )
