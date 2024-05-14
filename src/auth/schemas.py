from pydantic import BaseModel, EmailStr


class ClientRegistrationResponse(BaseModel):
    id: int


class ClientRegistration(BaseModel):
    email: EmailStr
    name: str
    password: str


class ClientInfoResponse(BaseModel):
    email: EmailStr
    name: str
    iat: int


class ClientAuthentication(BaseModel):
    email: EmailStr
    password: str


class JWTResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
