from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base
from worker.model import Worker


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
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.now,
    )
    worker_id: Mapped[int] = mapped_column(
        ForeignKey("workers.id",
                   ondelete="CASCADE",
                   )
    )

    worker: Mapped["Worker"] = relationship(back_populates="resumes")
