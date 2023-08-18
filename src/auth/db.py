from fastapi_users.db import (
    SQLAlchemyUserDatabase
)
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.auth import User
from db import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
