from pydantic import BaseModel


class GetResumesByName(BaseModel):
    title: str
