from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    algorithm: str = "RS256"
    access_token_expiration_time: int = 15  # minutes
    refresh_token_expiration_time: int = 30  # days


auth_config = AuthConfig()
