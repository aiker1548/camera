from fastapi import APIRouter, Depends, HTTPException, status

from src.application.auth.interfaces.service import AbstractAuthService
from src.application.auth.dto.auth_dto import UserCreate, LoginRequest
from src.application.auth.dto.token_dto import TokenPair, TokenRefresh
from src.presentation.api.routes.auth.dependencies.auth_dep import get_auth_service


router = APIRouter()

@router.post("/register", status_code=201)
async def register(
    user: UserCreate,
    service: AbstractAuthService = Depends(get_auth_service)
):
    try:
        await service.register(user)
        return {"detail": "User registered"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenPair)
async def login(
    data: LoginRequest,
    service: AbstractAuthService = Depends(get_auth_service)
):
    try:
        return await service.login(data.email, data.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/refresh", response_model=TokenPair)
async def refresh(
    data: TokenRefresh,
    service: AbstractAuthService = Depends(get_auth_service)
):
    try:
        return await service.refresh(data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))