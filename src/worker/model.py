from pydantic import EmailStr
from sqlalchemy.orm import Mapped, mapped_column, relationship

from resume.model import Resume
from database import Base


class Worker(Base):
    __table_name__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
        index=True,
    )
    email: EmailStr = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)

    resumes: Mapped[list["Resume"]] = relationship(
        back_populates="workers",
        order_by="Resume.id",
    )
