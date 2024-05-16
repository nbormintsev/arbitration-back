from datetime import datetime
from typing import Any

from fastapi import APIRouter, status, Depends

from src.auth.dependencies import get_current_token_payload
from src.auth.service import validate_token_type
from src.clients.crud import (
    create_client_settings,
    create_client_device,
)
from src.clients.schemas import (
    SettingsCreationResponse,
    SettingsCreation,
    SettingsInfoResponse,
    SettingsUpdate,
    DeviceCreationResponse,
    DeviceCreation,
    DeviceInfo,
)
from src.clients.service import (
    get_current_auth_client_settings,
    update_current_auth_client_settings,
    get_current_auth_client_devices,
    change_client_password, remove_current_auth_client_device,
)

router = APIRouter()


@router.post(
    path="/settings",
    status_code=status.HTTP_201_CREATED,
    response_model=SettingsCreationResponse,
)
async def add_new_client_settings(
    settings: SettingsCreation,
) -> SettingsCreationResponse:
    settings_id: int = await create_client_settings(
        client_id=settings.client_id,
        notification_min_spread=settings.notification_min_spread,
        language=settings.language,
        timezone_offset=settings.timezone_offset,
    )

    return SettingsCreationResponse(id=settings_id)


@router.get(path="/settings", response_model=SettingsInfoResponse)
async def get_authenticated_client_settings(
    token_payload: dict[str, Any] = Depends(get_current_token_payload),
) -> SettingsInfoResponse:
    validate_token_type("access", token_payload.get("type"))
    client_settings: dict[str, Any] = await get_current_auth_client_settings(
        token_payload,
    )

    return SettingsInfoResponse(
        notification_min_spread=client_settings.get("notification_min_spread"),
        language=client_settings.get("language"),
        timezone_offset=client_settings.get("timezone_offset"),
    )


@router.put(path="/settings", response_model=SettingsCreationResponse)
async def update_authenticated_client_settings(
    settings: SettingsUpdate,
    token_payload: dict[str, Any] = Depends(get_current_token_payload),
) -> SettingsCreationResponse:
    validate_token_type("access", token_payload.get("type"))
    settings_id: int = await update_current_auth_client_settings(
        settings,
        token_payload,
    )

    return SettingsCreationResponse(id=settings_id)


@router.post(
    path="/devices",
    status_code=status.HTTP_201_CREATED,
    response_model=DeviceCreationResponse,
)
async def add_new_client_device(
    device: DeviceCreation,
) -> DeviceCreationResponse:
    utc_now = datetime.utcnow()
    device_id: int = await create_client_device(
        client_id=device.client_id,
        device_hash=device.device_hash,
        device_name=device.device_name,
        last_online=utc_now,
    )

    return DeviceCreationResponse(id=device_id)


@router.get(path="/devices")
async def get_authenticated_client_devices(
    token_payload: dict[str, Any] = Depends(get_current_token_payload),
) -> list[DeviceInfo]:
    validate_token_type("access", token_payload.get("type"))
    client_devices: list[DeviceInfo] = await get_current_auth_client_devices(
        token_payload,
    )

    return client_devices


@router.delete(path="/devices")
async def remove_authenticated_client_device(
    device_id: int,
    token_payload: dict[str, Any] = Depends(get_current_token_payload),
) -> DeviceInfo:
    validate_token_type("access", token_payload.get("type"))

    return await remove_current_auth_client_device(device_id)


@router.put(
    path="/password",
    response_model=SettingsCreationResponse,
)
async def change_authenticated_client_password(
    password: str,
    token_payload: dict[str, Any] = Depends(get_current_token_payload),
) -> SettingsCreationResponse:
    validate_token_type("access", token_payload.get("type"))
    client_id = await change_client_password(
        token_payload.get("sub"),
        password,
    )

    return SettingsCreationResponse(id=client_id)
