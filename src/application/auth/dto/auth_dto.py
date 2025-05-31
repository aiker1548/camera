from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=8, description="Пароль пользователя")

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=8, description="Пароль пользователя")
    fio: str = Field(..., description="ФИО пользователя")
    org: Optional[str] = Field(None, description="Организация пользователя")


class UserRead(BaseModel):
    id: str = Field(..., description="UUID пользователя")
    email: EmailStr = Field(..., description="Email пользователя")
    fio: str = Field(..., description="ФИО пользователя")
    org: Optional[str] = Field(None, description="Организация пользователя")
    created_at: datetime = Field(..., description="Дата создания учётной записи")

    class Config:
        orm_mode = True