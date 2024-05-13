from pydantic import BaseModel, EmailStr


class RegisterClient(BaseModel):
    name: str
    email: EmailStr
    password: str


class AuthClient(BaseModel):
    email: EmailStr
    password: str


class ClientResponse(BaseModel):
    id: int


class JWTData(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
