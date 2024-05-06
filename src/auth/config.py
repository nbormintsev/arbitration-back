from os import getenv

from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    algorithm: str = getenv("JWT_ALGORITHM")
    access_token_expiration_time: int = 15  # minutes
    refresh_token_expiration_time: int = 30  # days


auth_config = AuthConfig()
