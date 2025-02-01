from fastapi import APIRouter, Depends

from auth import utils
from auth.schema import TokenSchema
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
