from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer

from src.auth.dependencies import (
    validate_client_creation,
    get_current_token_payload,
)
from src.auth.schemas import (
    ClientRegistrationResponse,
    ClientRegistration,
    ClientInfoResponse,
    ClientAuthentication,
    JWTResponse,
)
from src.auth.service import (
    create_client,
    validate_token_type,
    get_current_active_auth_client,
    create_access_token,
    create_refresh_token,
    auth_client,
)

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(dependencies=[Depends(http_bearer)])


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
    token_payload: dict[str, Any] = Depends(get_current_token_payload),
) -> ClientInfoResponse:
    validate_token_type("access", token_payload.get("type"))
    client: dict[str, Any] = await get_current_active_auth_client(token_payload)

    return ClientInfoResponse(
        email=client.get("email"),
        name=client.get("name"),
        iat=token_payload.get("iat"),
    )


@router.post(path="/tokens", response_model=JWTResponse)
async def authenticate_client(
    auth_data: ClientAuthentication,
) -> JWTResponse:
    client: dict[str, Any] = await auth_client(auth_data)
    access_token: str = create_access_token(client.get("id"))
    refresh_token: str = create_refresh_token(client.get("id"))

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
    token_payload: dict[str, Any] = Depends(get_current_token_payload),
):
    validate_token_type("refresh", token_payload.get("type"))
    client: dict[str, Any] = await get_current_active_auth_client(token_payload)
    access_token: str = create_access_token(client.get("id"))

    return JWTResponse(
        access_token=access_token,
    )
