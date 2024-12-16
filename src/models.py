from datetime import datetime
from enum import Enum

from pydantic import EmailStr
from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Worker(Base):
    __table_name__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    email: EmailStr = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)

    resumes: Mapped[list["Resume"]] = relationship(back_populates="workers", order_by="Resume.id")


class Workload(Enum):
    fulltime = "fulltime"
    parttime = "parttime"


class Resume(Base):
    __table_name__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column()
    salary: Mapped[int | None] = mapped_column()
    workload: Mapped[Workload]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.now)
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))

    worker: Mapped["Worker"] = relationship(back_populates="resumes")
