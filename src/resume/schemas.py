from pydantic import BaseModel

from resume.model import Workload


class GetResumesByNameSchema(BaseModel):
    title: str


class CreateResumeSchema(GetResumesByNameSchema):
    description: str
    salary: int | None
    workload: Workload


class UpdateResumeSchema(BaseModel):
    title: str | None
    description: str | None
    salary: int | None
    workload: Workload | None
