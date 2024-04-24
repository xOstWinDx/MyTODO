from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.database import get_async_session
from app.user.models import User


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def fetch_all_with_tasks(cls, **filter_by):
        async with get_async_session() as session:
            res = await session.execute(
                select(cls.model)
                .options(selectinload(User.tasks))
                .filter_by(**filter_by)
            )
            res = res.mappings().all()

        return res

    @classmethod
    async def fetch_one_or_none_with_tasks(cls, **filter_by):
        async with get_async_session() as session:
            res = await session.execute(
                select(cls.model)
                .options(selectinload(User.tasks))
                .filter_by(**filter_by)
            )
            res = res.scalar_one_or_none()
        return res
