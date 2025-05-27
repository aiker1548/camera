from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.services import AuthService
from src.auth.schemas import UserCreate, TokenPair, TokenRefresh, LoginRequest
from src.dependencies.service import get_auth_service

router = APIRouter()

@router.post("/register", status_code=201)
async def register(
    user: UserCreate,
    service: AuthService = Depends(get_auth_service)
):
    try:
        await service.register(user)
        return {"detail": "User registered"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenPair)
async def login(
    data: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    try:
        return await service.login(data.email, data.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/refresh", response_model=TokenPair)
async def refresh(
    data: TokenRefresh,
    service: AuthService = Depends(get_auth_service)
):
    try:
        return await service.refresh(data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))