from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends


from src.infrastructure.services.jwt_provider import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")


async def get_current_user(
        token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload is None or "sub" not in payload:
        raise ValueError("Invalid authentication token")
    return payload
