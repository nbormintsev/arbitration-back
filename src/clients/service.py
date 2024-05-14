from typing import Any

from fastapi import HTTPException, status

from src.auth.utils import hash_password
from src.clients.crud import (
    get_client_settings_by_id,
    update_client_settings,
    get_client_devices_by_id,
    update_client_password,
)
from src.clients.schemas import SettingsUpdate
from src.clients.utils import devices_to_dict


async def get_current_auth_client_settings(
    token_payload: dict,
) -> dict[str, Any]:
    client_settings: dict[str, Any] | None = await get_client_settings_by_id(
        token_payload.get("sub"),
    )

    if not client_settings:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid."
        )

    return client_settings


async def update_current_auth_client_settings(
    settings: SettingsUpdate,
    token_payload: dict,
) -> int:
    client_settings: int = await update_client_settings(
        client_id=token_payload.get("sub"),
        notification_min_spread=settings.notification_min_spread,
        language=settings.language,
        timezone_offset=settings.timezone_offset
    )

    if not client_settings:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid."
        )

    return client_settings


async def get_current_auth_client_devices(
    token_payload: dict,
) -> dict[int, dict]:
    client_devices: list = await get_client_devices_by_id(
        token_payload.get("sub"),
    )

    if not client_devices:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid."
        )

    client_devices_dict: dict[int, dict] = devices_to_dict(client_devices)

    return client_devices_dict


async def change_client_password(
    client_id: int,
    password: str,
) -> int:
    password_hash: bytes = hash_password(password)
    return await update_client_password(
        client_id,
        password_hash,
    )
