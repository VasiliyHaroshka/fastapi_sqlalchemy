from datetime import datetime, timedelta

from jwt.exceptions import InvalidTokenError

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from config import settings
from database.database import SessionLocal, get_db
from error import Missing
from user.model import User
from user.schemas import UserSchema

oauth2 = OAuth2PasswordBearer(
    tokenUrl="auth/login/",  # адрес для выпуска токена
)


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


def get_current_token(
        token: str = Depends(oauth2),
) -> UserSchema:
    try:
        payload = decode_jwt_token(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return payload


async def get_current_auth_user(
        payload: dict = Depends(get_current_token),
        db: SessionLocal = Depends(get_db),
) -> UserSchema:
    user_id: int = payload.get("sub")
    query = select(User).filter_by(id=user_id)
    result = await db.execute(query)
    user = result.scalars().one()
    if not user:
        raise Missing(msg=f"User with username = {user.username} is not found")
    return user


def create_token(data: dict, token_type: str) -> str:
    payload = {"token_type": token_type}
    payload.update(data)
    return encode_jwt_token(payload=payload)


def create_access_token(user: UserSchema) -> str:
    payload = {
        "sub": user.id,
        "username": user.username,
        "email": user.email,
    }
    return create_token(token_type="access", data=payload)


def create_refresh_token(user: UserSchema) -> str:
    payload = {
        "sub": user.id,
    }
    return create_token(token_type="refresh", data=payload)
