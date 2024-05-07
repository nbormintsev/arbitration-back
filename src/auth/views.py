from fastapi import APIRouter, status, Depends
from fastapi.security import HTTPBearer

from src.auth import service
from src.auth.dependencies import (
    validate_client_creation,
    validate_client_auth,
    get_current_token_payload,
    get_current_auth_client_for_refresh,
)
from src.auth.schemas import AuthClient, JWTData, Client
from src.auth.service import create_access_token

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(dependencies=[Depends(http_bearer)])


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
)
async def register_client(
    auth_data: AuthClient = Depends(validate_client_creation),
) -> dict[str, int]:
    client_id = await service.register_client(auth_data)
    return {
        "id": client_id,
    }


@router.post(path="/login")
async def auth_client_issue_jwt(
    auth_data: AuthClient = Depends(validate_client_auth)
) -> JWTData:
    access_token = service.create_access_token(auth_data.login)
    refresh_token = service.create_refresh_token(auth_data.login)
    return JWTData(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    path="/refresh",
    response_model=JWTData,
    response_model_exclude_none=True,
)
async def auth_refresh_jwt(
    client_data: Client = Depends(get_current_auth_client_for_refresh),
):
    access_token = create_access_token(client_data.login)
    return JWTData(
        access_token=access_token,
    )


@router.get(path="/clients/me")
async def auth_client_self_check_info(
    payload: dict = Depends(get_current_token_payload),
    client_data: Client = Depends(service.get_current_active_auth_client),
):
    return {
        "login": client_data.login,
        "iat": payload.get("iat"),
        "timezone": None,
        "currency": None,
        "locale": None,
    }
