import uuid
from datetime import datetime, timedelta
from typing import Any

import bcrypt
import jwt

from src.auth.config import auth_config
from src.config import keys_manager


def hash_password(password: str) -> bytes:
    password_bytes = bytes(password, "utf-8")
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    password_bytes = bytes(password, "utf-8")

    return bcrypt.checkpw(password_bytes, hashed_password)


def encode_jwt(
    payload: dict[str, Any],
    expiration_time: timedelta,
) -> str:
    to_encode = payload.copy()
    utc_now = datetime.utcnow()
    exp = utc_now + expiration_time
    to_encode.update(
        jti=str(uuid.uuid4()),
        iat=utc_now,
        exp=exp,
    )

    return jwt.encode(
        payload=to_encode,
        key=keys_manager.private_key,
        algorithm=auth_config.algorithm,
    )


def decode_jwt(
    token: str | bytes,
) -> dict[str, Any]:
    return jwt.decode(
        jwt=token,
        key=keys_manager.public_key,
        algorithms=[auth_config.algorithm],
    )
