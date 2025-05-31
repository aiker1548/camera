from pydantic import BaseModel, Field
from datetime import datetime

class TokenPair(BaseModel):
    access_token: str = Field(..., description="JWT Access Token")
    access_expires_at: datetime = Field(..., description="Время истечения Access Token")
    refresh_token: str = Field(..., description="JWT Refresh Token")
    refresh_expires_at: datetime = Field(..., description="Время истечения Refresh Token")


class TokenRefresh(BaseModel):
    refresh_token: str = Field(..., description="JWT Refresh Token для обновления pair")
