from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings

engine = create_async_engine(
    url=settings.db_url,
    echo=True,
)

SessionLocal = async_sessionmaker(
    engine,
    autoflush=True,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
