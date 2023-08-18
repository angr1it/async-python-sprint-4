from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from db import get_async_session
from services.ping import ping
from auth.db import User
from api.auth import current_user

ping_router = APIRouter()


@ping_router.get('/')
async def get_ping(
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session)
):
    connect = await ping(db=db)
    if user:
        email = user.email
    else:
        email = None

    return {
        "status": "OK",
        "data": {
            "db_on": connect,
            "user": email
        },
        "description": None
    }
