from pydantic import BaseModel

from resume.model import Workload


class GetResumesByNameSchema(BaseModel):
    title: str


class CreateResumeSchema(GetResumesByNameSchema):
    description: str
    salary: int | None
    workload: Workload
