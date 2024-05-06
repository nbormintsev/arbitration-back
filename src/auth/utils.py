import uuid
from datetime import datetime, timedelta

import bcrypt
import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
    RSAPublicKey,
)

from src.auth.config import auth_config


def generate_private_key() -> RSAPrivateKey:
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )


def generate_public_key(private_key: RSAPrivateKey) -> RSAPublicKey:
    return private_key.public_key()


_private_key: RSAPrivateKey = generate_private_key()
_public_key: RSAPublicKey = generate_public_key(_private_key)


def hash_password(password: str) -> bytes:
    password_bytes = bytes(password, "utf-8")
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    password_bytes = bytes(password, "utf-8")

    return bcrypt.checkpw(password_bytes, hashed_password)


def encode_jwt(
    payload: dict,
) -> str:
    to_encode = payload.copy()
    utc_now = datetime.utcnow()
    exp = utc_now + timedelta(minutes=auth_config.access_token_expiration_time)
    to_encode.update(
        jti=str(uuid.uuid4()),
        iat=utc_now,
        exp=exp,
    )

    return jwt.encode(
        payload=to_encode,
        key=_private_key,
        algorithm=auth_config.algorithm,
    )


def decode_jwt(
    token: str | bytes,
) -> dict:
    decoded = jwt.decode(
        jwt=token,
        key=_public_key,
        algorithms=[auth_config.algorithm],
    )

    return decoded
