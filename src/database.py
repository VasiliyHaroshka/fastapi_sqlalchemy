from sqlalchemy import create_async_engine

from config import Settings

engine = create_async_engine(
    Settings.db_url,
    echo=True,
)
