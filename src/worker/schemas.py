from pydantic import BaseModel

class BaseSchema(BaseModel):
    pass

class WorkerGetSchema(BaseSchema):
    name: str

class WorkerCreateSchema(WorkerGetSchema):
    name: str
    email: str
    hashed_password: str