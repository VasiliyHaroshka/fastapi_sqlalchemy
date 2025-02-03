from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select

from auth.error import unactive_exception
from config import settings
from database.database import SessionLocal, get_db
from error import Missing
from user.model import User
from user.schemas import UserSchema

http_bearer = HTTPBearer()  # получение токена из заголовка Authorization


def encode_jwt_token(
        payload: dict,
        private_key: str = settings.jwt_auth.private_key_path.read_text(),
        algorithm: str = settings.jwt_auth.algorithm,
        expire_minutes: int = settings.jwt_auth.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None
):
    """Return encoded jwt token"""
    now = datetime.now()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    payload["exp"] = expire
    payload["iat"] = now
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


def check_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    """Check weather matches user's password and hash password"""
    return bcrypt.checkpw(password.encode(), hashed_password)


def get_payload_from_credentials(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> UserSchema:
    token = credentials.credentials
    payload = decode_jwt_token(token=token)
    return payload


async def get_current_auth_user(
        payload: dict = Depends(get_payload_from_credentials),
        db: SessionLocal = Depends(get_db),
) -> UserSchema:
    username: str = payload.get("sub")
    query = select(User).filter_by(username=username)
    result = await db.execute(query)
    user = result.scalars().one()
    if not user:
        raise Missing(msg=f"User with username = {user.username} is not found")
    return user


