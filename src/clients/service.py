from typing import Any

from fastapi import HTTPException, status

from src.auth.utils import hash_password
from src.clients.crud import (
    get_client_settings_by_id,
    update_client_settings,
    get_client_devices_by_id,
    remove_client_device,
    update_client_password,
)
from src.clients.schemas import SettingsUpdate, DeviceInfo


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
) -> list[DeviceInfo]:
    device_list: list[dict[str, Any]] = await get_client_devices_by_id(
        token_payload.get("sub"),
    )

    if not device_list:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid."
        )

    return [
        DeviceInfo(
            id=device.get("id"),
            device_name=device.get("device_name"),
            last_login_date=device.get("last_online"),
        ) for device in device_list
    ]


async def remove_current_auth_client_device(
    token_payload: dict[str, Any],
    device_id: int,
) -> DeviceInfo:
    device: dict[str, Any] = await remove_client_device(
        token_payload.get("sub"),
        device_id,
    )

    return DeviceInfo(
        id=device.get("id"),
        device_name=device.get("device_name"),
        last_login_date=device.get("last_online"),
    )


async def change_client_password(
    client_id: int,
    password: str,
) -> int:
    return await update_client_password(
        client_id,
        hash_password(password),
    )
