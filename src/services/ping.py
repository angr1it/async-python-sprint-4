from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text


async def ping(db: AsyncSession) -> bool:
    try:
        await db.execute(text('SELECT 1'))
        return True
    except Exception as ex:
        print(ex)
        return False
