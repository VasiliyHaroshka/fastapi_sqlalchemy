from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250))

    worker_in: Mapped[list["Workers"]] = relationship(
        back_populates="workers_projects",
        secondary="workers_projects",
    )


class WorkersProjects(Base):
    __tablename__ = "workers_projects"

    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id"), primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), primary_key=True)
