from typing import Any

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from src.auth.crud import get_client_by_login
from src.auth.schemas import AuthClient, Client
from src.auth.utils import validate_password, decode_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def validate_client_creation(
    auth_data: AuthClient,
) -> AuthClient:

    if await get_client_by_login(auth_data.login):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login is already taken. ",
        )

    return auth_data


async def validate_client_auth(
    auth_data: AuthClient,
) -> AuthClient:
    client: dict[str, Any] | None = await get_client_by_login(auth_data.login)

    if not client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid login. ",
        )

    if not validate_password(
        auth_data.password,
        client["password_hash"],
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password. ",
        )

    return auth_data


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme)
) -> dict:
    try:
        payload = decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid. "
        )

    return payload


async def validate_token_type(
    token_payload: dict,
    token_type: str,
) -> bool:
    current_token_type = token_payload.get("type")

    if current_token_type == token_type:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token type. "
    )


async def get_user_by_token_sub(token_payload: dict) -> Client:
    login: str | None = token_payload.get("sub")
    client: dict[str, Any] | None = await get_client_by_login(login)

    if client:
        return Client(
            login=login,
            password=client.get("password_hash")
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token is invalid. "
    )


async def get_current_auth_client(
    token_payload: dict = Depends(get_current_token_payload),
) -> Client:
    await validate_token_type(token_payload, "access")
    return await get_user_by_token_sub(token_payload)


async def get_current_auth_client_for_refresh(
    token_payload: dict = Depends(get_current_token_payload),
) -> Client:
    await validate_token_type(token_payload, "refresh")
    return await get_user_by_token_sub(token_payload)
