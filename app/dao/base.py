from fastapi import HTTPException

from app.database import get_async_session
from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, **data):
        try:
            async with get_async_session() as session:
                r = await session.execute(
                    insert(cls.model).values(**data).returning(cls.model)
                )
                r = r.scalar_one_or_none()
                await session.commit()
            if not r:
                raise HTTPException(status_code=400, detail="Не верные данные")
            return r
        except SQLAlchemyError:
            raise HTTPException(status_code=400, detail="Не верные данные")

    @classmethod
    async def fetch_one_or_none(cls, **filter_by):
        async with get_async_session() as session:
            res = await session.execute(select(cls.model).filter_by(**filter_by))
            res = res.scalar_one_or_none()
        return res

    @classmethod
    async def fetch_all(cls, **filter_by):
        async with get_async_session() as session:
            res = await session.execute(select(cls.model).filter_by(**filter_by))
            res = res.mappings().all()

        return res

    @classmethod
    async def update(cls, ID, **data):
        async with get_async_session() as session:
            await session.execute(update(cls.model).values(**data).filter_by(ID=ID))
            await session.commit()

        return "ok"
