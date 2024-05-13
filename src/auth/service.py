from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status

from src.auth.config import auth_config
from src.auth.crud import add_client, get_client_status
from src.auth.dependencies import get_current_auth_client
from src.auth.schemas import RegisterClient, AuthClient
from src.auth.utils import hash_password, encode_jwt


async def register_client(
    client_data: RegisterClient,
) -> int:
    return await add_client(
        email=client_data.email,
        name=client_data.name,
        password_hash=hash_password(client_data.password),
    )


def create_jwt(token_type: str, token_data: dict) -> str:
    payload = {"type": token_type}
    payload.update(token_data)

    return encode_jwt(payload)


def create_access_token(email: str) -> str:
    utc_now = datetime.utcnow()
    token_data = {
        "sub": email,
        "iat": utc_now,
        "exp": utc_now + timedelta(
            minutes=auth_config.access_token_expiration_time,
        ),
    }

    return create_jwt(
        token_type="access",
        token_data=token_data,
    )


def create_refresh_token(email: str) -> str:
    utc_now = datetime.utcnow()
    token_data = {
        "sub": email,
        "exp": utc_now + timedelta(
            days=auth_config.refresh_token_expiration_time,
        ),
    }

    return create_jwt(
        token_type="refresh",
        token_data=token_data,
    )


async def get_current_active_auth_client(
    client_data: AuthClient = Depends(get_current_auth_client)
):
    if not await get_client_status(client_data.email):
        return client_data

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User inactive. "
    )
