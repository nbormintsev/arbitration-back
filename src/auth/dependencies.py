from typing import Any

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from src.auth.crud import get_client_by_email
from src.auth.schemas import RegisterClient, AuthClient
from src.auth.utils import validate_password, decode_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/tokens")


async def validate_client_creation(
    client_data: RegisterClient,
) -> RegisterClient:

    if await get_client_by_email(client_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already taken.",
        )

    return client_data


async def validate_client_auth(
    client_data: AuthClient,
) -> AuthClient:
    client: dict[str, Any] | None = await get_client_by_email(client_data.email)

    if not client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid login.",
        )

    if not validate_password(client_data.password, client["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password.",
        )

    return client_data


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme)
) -> dict:
    try:
        payload = decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid."
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
        detail="Invalid token type."
    )


async def get_user_by_token_sub(token_payload: dict) -> AuthClient:
    email: str | None = token_payload.get("sub")
    client: dict[str, Any] | None = await get_client_by_email(email)

    if client:
        return AuthClient(
            email=email,
            password=client.get("password_hash")
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token is invalid."
    )


async def get_current_auth_client(
    token_payload: dict = Depends(get_current_token_payload),
) -> AuthClient:
    await validate_token_type(token_payload, "access")

    return await get_user_by_token_sub(token_payload)


async def get_current_auth_client_for_refresh(
    token_payload: dict = Depends(get_current_token_payload),
) -> AuthClient:
    await validate_token_type(token_payload, "refresh")

    return await get_user_by_token_sub(token_payload)
