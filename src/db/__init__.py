from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import app_settings


engine = create_async_engine(
    url=str(app_settings.database_dsn),
    echo=app_settings.echo_db_engine
)


async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=True
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
