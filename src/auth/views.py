from typing import Any

from fastapi import APIRouter, Depends, status

from src.auth.dependencies import (
    validate_client_creation,
    validate_access_token,
    validate_refresh_token,
)
from src.auth.schemas import (
    ClientRegistrationResponse,
    ClientRegistration,
    ClientInfoResponse,
    ClientAuthentication,
    ValidatedClientAuthentication,
    JWTResponse,
)
from src.auth.service import (
    create_client,
    get_current_active_auth_client,
    create_access_token,
    create_refresh_token,
    auth_client,
)

router = APIRouter()


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ClientRegistrationResponse,
)
async def register_client(
    client_data: ClientRegistration = Depends(validate_client_creation),
) -> ClientRegistrationResponse:
    client_id: int = await create_client(client_data)

    return ClientRegistrationResponse(id=client_id)


@router.get(path="/me", response_model=ClientInfoResponse)
async def get_authenticated_client_info(
    token_payload: dict[str, Any] = Depends(validate_access_token),
) -> ClientInfoResponse:
    client: dict[str, Any] = await get_current_active_auth_client(token_payload)

    return ClientInfoResponse(
        email=client.get("email"),
        name=client.get("name"),
        iat=token_payload.get("iat"),
    )


@router.post(path="/tokens", response_model=JWTResponse)
async def authenticate_client(
    auth_data: ClientAuthentication | ValidatedClientAuthentication = Depends(
        auth_client,
    ),
) -> JWTResponse:
    access_token: str = create_access_token(auth_data.id)
    refresh_token: str = create_refresh_token(auth_data.id)

    return JWTResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.put(
    path="/tokens",
    response_model=JWTResponse,
    response_model_exclude_none=True,
)
async def refresh_access_token(
    token_payload: dict[str, Any] = Depends(validate_refresh_token),
):
    client: dict[str, Any] = await get_current_active_auth_client(token_payload)
    access_token: str = create_access_token(client.get("id"))

    return JWTResponse(
        access_token=access_token,
    )
