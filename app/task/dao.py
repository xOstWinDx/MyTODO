import datetime

from fastapi import HTTPException
from sqlalchemy import select, update, delete

from app.dao.base import BaseDAO
from app.database import get_async_session
from app.task.models import Task


class TaskDAO(BaseDAO):
    model = Task

    @classmethod
    async def fetch_all(cls, **filter_by):
        async with get_async_session() as session:
            res = await session.execute(select(cls.model).filter_by(**filter_by))
            res: list[dict[str, Task]] = res.mappings().all()
            if res:
                print(res)
                for task in res:
                    if not task["Task"].status:
                        task["Task"].__setattr__(
                            "expire",
                            task["Task"].deadline < datetime.datetime.now(datetime.UTC),
                        )
        return res

    @classmethod
    async def update(cls, ID, **data):

        async with get_async_session() as session:
            if "status" in data:
                r = await session.execute(
                    update(cls.model)
                    .values(status=data["status"])
                    .filter_by(ID=ID, assigned_user=data["user_id"])
                    .returning(cls.model)
                )
                r = r.scalar()
            else:
                r = await session.execute(
                    update(cls.model)
                    .values(**data)
                    .filter_by(ID=ID)
                    .returning(cls.model)
                )
                r = r.scalar()
            await session.commit()
        if not r:

            raise HTTPException(status_code=400, detail="Не верные данные")

        return r

    @classmethod
    async def delete(
        cls,
        task_id: int,
        user_id: int,
        isadmin: bool = False,
    ):
        async with get_async_session() as session:
            if isadmin:
                await session.execute(delete(cls.model).filter_by(ID=task_id))
            else:
                await session.execute(
                    delete(cls.model).filter_by(ID=task_id, created_by=user_id)
                )
            await session.commit()
        return "ok"
