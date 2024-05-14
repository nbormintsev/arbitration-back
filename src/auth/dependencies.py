from typing import Any

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from src.auth.crud import get_client_by_email
from src.auth.schemas import ClientRegistration, ClientAuthentication
from src.auth.service import is_client_banned
from src.auth.utils import decode_jwt, validate_password

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
):
    try:
        token_payload = decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid."
        )

    return token_payload


async def validate_client_authentication(
    client_data: ClientAuthentication,
) -> ClientAuthentication:
    client: dict[str, Any] | None = await get_client_by_email(client_data.email)

    if not client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid login.",
        )

    if is_client_banned(client):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have been banned.",
        )

    if not validate_password(client_data.password, client["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password.",
        )

    return client_data
