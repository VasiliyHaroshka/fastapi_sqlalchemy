from fastapi import Form, Depends
from sqlalchemy import select

from auth.error import unauth_exception
from auth.utils import check_password
from database.database import SessionLocal, get_db
from user.model import User


async def user_validator(
        username: str = Form(),
        password: str = Form(),
        db: SessionLocal = Depends(get_db)
):
    query = select(User).filter_by(username=username)
    result = await db.execute(query)
    user = result.scalars().one()
    if not user:
        raise unauth_exception()
    if not check_password(password=password, hashed_password=user.password):
        raise unauth_exception()
    if not user.is_active:
        raise unauth_exception()
    return user
