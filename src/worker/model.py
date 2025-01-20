from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class Worker(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
        index=True,
    )
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    resumes: Mapped[list["Resume"]] = relationship(
        back_populates="workers",
        order_by="Resume.id",
    )

    projects: Mapped[list["Project"]] = relationship(
        back_populates="worker_in",
        secondary="workers_projects",
    )
