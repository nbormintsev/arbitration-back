from typing import Any

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from src.auth.crud import get_client_by_email
from src.auth.schemas import ClientRegistration
from src.auth.utils import decode_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/tokens")


async def validate_client_creation(
    client_data: ClientRegistration,
) -> ClientRegistration:

    if await get_client_by_email(client_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already taken.",
        )

    return client_data


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme)
) -> dict[str, Any]:
    try:
        token_payload: dict[str, Any] = decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid."
        )

    return token_payload
