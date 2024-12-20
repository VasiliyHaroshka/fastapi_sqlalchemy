from pydantic import BaseModel

class BaseSchema(BaseModel):
    pass

class WorkerGetSchema(BaseSchema):
    name: str