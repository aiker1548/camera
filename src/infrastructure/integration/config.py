from pydantic import HttpUrl, SecretStr
from pydantic_settings import BaseSettings

class MlSettings(BaseSettings):
    url: HttpUrl

