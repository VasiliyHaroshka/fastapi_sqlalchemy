from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250))

