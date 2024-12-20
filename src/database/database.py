from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from config import Settings

engine = create_async_engine(
    url=Settings.db_url,
    echo=True,
)

SessionLocal = async_sessionmaker(
    engine,
    autoflush=True,
    expire_on_commit=False,
)


class Base(declarative_base):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
