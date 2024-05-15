from datetime import timedelta
from typing import Any

from fastapi import HTTPException, status

from src.auth.config import auth_config
from src.auth.crud import add_client, get_client_by_email
from src.auth.schemas import ClientRegistration, ClientAuthentication
from src.auth.utils import hash_password, encode_jwt, validate_password
from src.crud import get_client_by_id


async def create_client(
    client_data: ClientRegistration,
) -> int:
    return await add_client(
        email=client_data.email,
        name=client_data.name,
        password_hash=hash_password(client_data.password),
    )


def validate_token_type(
    token_type: str,
    payload_token_type: str,
) -> bool:
    if payload_token_type == token_type:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token type."
    )


def is_client_banned(
    client: dict[str, Any],
) -> bool:
    is_banned: bool | None = client.get("is_banned")

    if is_banned:
        return True

    return False


async def get_current_active_auth_client(token_payload: dict) -> dict[str, Any]:
    client: dict[str, Any] | None = await get_client_by_id(
        token_payload.get("sub"),
    )

    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid."
        )

    if is_client_banned(client):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have been banned."
        )

    return client


async def auth_client(
    client_data: ClientAuthentication,
) -> dict[str, Any]:
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

    return client


def create_jwt(
    token_type: str,
    token_data: dict,
    expiration_time: timedelta,
) -> str:
    payload = {"type": token_type}
    payload.update(token_data)

    return encode_jwt(payload, expiration_time)


def create_access_token(client_id: str) -> str:
    token_data = {
        "sub": client_id,
    }
    expiration_time = timedelta(
        minutes=auth_config.access_token_expiration_time,
    )

    return create_jwt(
        token_type="access",
        token_data=token_data,
        expiration_time=expiration_time,
    )


def create_refresh_token(client_id: int) -> str:
    token_data = {
        "sub": client_id,
    }
    expiration_time = timedelta(
        days=auth_config.refresh_token_expiration_time,
    )

    return create_jwt(
        token_type="refresh",
        token_data=token_data,
        expiration_time=expiration_time,
    )
