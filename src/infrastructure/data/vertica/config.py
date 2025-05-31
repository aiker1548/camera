from pydantic_settings import BaseSettings


class VerticaSettings(BaseSettings):
    host: str = "localhost"
    port: int = 5433
    user: str = "user"
    password: str = "password"
    db_name: str = "db"
    load_balance: bool = True
    timeout: int = 30
    debug: bool = True

