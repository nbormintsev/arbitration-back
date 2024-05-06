from pydantic import BaseModel, ConfigDict


class AuthClient(BaseModel):
    login: str
    password: str


class Client(BaseModel):
    model_config = ConfigDict(strict=True)

    login: str
    password: bytes


class JWTData(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
