from fastapi import APIRouter, status, Depends
from fastapi.security import HTTPBearer

from src.auth import service
from src.auth.dependencies import (
    validate_client_creation,
    validate_client_auth,
    get_current_token_payload,
    get_current_auth_client_for_refresh,
)
from src.auth.schemas import (
    ClientResponse,
    RegisterClient,
    AuthClient,
    JWTData,
)
from src.auth.service import create_access_token

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(dependencies=[Depends(http_bearer)])


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ClientResponse,
)
async def register_client(
    client_data: RegisterClient = Depends(validate_client_creation),
) -> dict[str, int]:
    client_id = await service.register_client(client_data)

    return {
        "id": client_id,
    }


@router.get(path="/me")
async def auth_client_self_check_info(
    payload: dict = Depends(get_current_token_payload),
    client_data: AuthClient = Depends(service.get_current_active_auth_client),
):
    return {
        "email": client_data.email,
        "iat": payload.get("iat"),
        "timezone": None,
        "currency": None,
        "locale": None,
    }


@router.post(path="/tokens")
async def auth_client_issue_jwt(
    auth_data: AuthClient = Depends(validate_client_auth)
) -> JWTData:
    access_token = service.create_access_token(auth_data.email)
    refresh_token = service.create_refresh_token(auth_data.email)

    return JWTData(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.put(
    path="/tokens",
    response_model=JWTData,
    response_model_exclude_none=True,
)
async def auth_refresh_jwt(
    client_data: AuthClient = Depends(get_current_auth_client_for_refresh),
):
    access_token = create_access_token(client_data.email)

    return JWTData(
        access_token=access_token,
    )
