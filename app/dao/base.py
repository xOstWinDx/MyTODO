from app.database import get_async_session
from sqlalchemy import insert, select


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, **data):
        async with get_async_session() as session:
            await session.execute(insert(cls.model).values(**data))
            await session.commit()

    @classmethod
    async def fetch_one(cls, **filter_by):
        async with get_async_session() as session:
            res = await session.execute(select(cls.model).filter_by(**filter_by))
            res = res.scalar_one_or_none()
        return res
