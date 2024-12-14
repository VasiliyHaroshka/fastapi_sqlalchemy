from sqlalchemy import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import Settings

engine = create_async_engine(
    Settings.db_url,
    echo=True,
)

session_local = async_sessionmaker(
    engine,
    autoflush=True,
    expire_on_commit=False,
)
