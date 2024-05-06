from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status

from src.auth.config import auth_config
from src.auth.crud import add_client, get_client_status
from src.auth.dependencies import get_current_auth_client
from src.auth.schemas import AuthClient, Client
from src.auth.utils import hash_password, encode_jwt


async def register_client(
    auth_data: AuthClient,
) -> int:
    return await add_client(
        login=auth_data.login,
        password_hash=hash_password(auth_data.password),
    )


def create_jwt(token_type: str, token_data: dict) -> str:
    payload = {"type": token_type}
    payload.update(token_data)
    return encode_jwt(payload)


def create_access_token(login: str) -> str:
    utc_now = datetime.utcnow()
    token_data = {
        "sub": login,
        "iat": utc_now,
        "exp": utc_now + timedelta(
            minutes=auth_config.access_token_expiration_time,
        ),
    }
    return create_jwt(
        token_type="access",
        token_data=token_data,
    )


def create_refresh_token(login: str) -> str:
    utc_now = datetime.utcnow()
    token_data = {
        "sub": login,
        "exp": utc_now + timedelta(
            days=auth_config.refresh_token_expiration_time,
        ),
    }
    return create_jwt(
        token_type="refresh",
        token_data=token_data,
    )


async def get_current_active_auth_client(
    client_data: Client = Depends(get_current_auth_client)
):
    if not await get_client_status(client_data.login):
        return client_data

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User inactive. "
    )
