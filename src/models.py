from enum import Enum

from pydantic import EmailStr
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Worker(Base):
    __table_name__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    email: EmailStr = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)


class Workload(Enum):
    fulltime = "fulltime"
    parttime = "parttime"


class Resume(Base):
    __table_name__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column()
    salary: Mapped[int | None] = mapped_column()
    workload: Mapped[Workload]
