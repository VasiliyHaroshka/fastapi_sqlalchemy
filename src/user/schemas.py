from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel


class UserSchema(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: bytes
    email: str | None
    is_active: bool = True
