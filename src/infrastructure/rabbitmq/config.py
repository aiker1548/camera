from pydantic_settings import BaseSettings


class RabbitMQSettings(BaseSettings):
    url: str
    exchange: str
    routing_key: str
    queue: str
