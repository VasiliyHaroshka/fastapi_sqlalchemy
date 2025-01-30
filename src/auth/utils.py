import bcrypt
import jwt

from config import settings


def encode_jwt_token(
        payload: dict,
        private_key: str = settings.jwt_auth.private_key_path.read_text(),
        algorithm: str = settings.jwt_auth.algorithm,
):
    """Return encoded jwt token"""
    encoded = jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt_token(
        token: str | bytes,
        public_key: str = settings.jwt_auth.public_key_path,
        algorithm: str = settings.jwt_auth.algorithm,
):
    """Return decoded jwt token"""
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(password: str) -> bytes:
    """User's password encryption"""
    password_in_bytes: bytes = password.encode()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_in_bytes, salt)
