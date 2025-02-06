from fastapi import APIRouter, Depends

from auth import utils
from auth.schema import TokenSchema
from auth.utils import get_current_auth_user, get_current_token
from auth.validators import user_validator
from user.schemas import UserSchema

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login/", response_model=TokenSchema)
def login(user: UserSchema = Depends(user_validator)):
    payload = {
        "sub": user.id,
        "username": user.username,
        "email": user.email,
    }
    access_token = utils.encode_jwt_token(payload=payload)
    return TokenSchema(
        access_token=access_token,
        token_type="Bearer",
    )


@router.get("/me")
def self_info(
        user: UserSchema = Depends(get_current_auth_user),
        payload: dict = Depends(get_current_token),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "login_at": iat,
    }
