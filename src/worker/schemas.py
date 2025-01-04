from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr


class BaseSchema(BaseModel):
    pass


class WorkerGetSchema(BaseSchema):
    name: Annotated[str, MinLen(3), MaxLen(50)]


class WorkerCreateSchema(WorkerGetSchema):
    email: EmailStr
    hashed_password: str
