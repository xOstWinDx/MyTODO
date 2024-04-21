import datetime

from sqlalchemy import select, update

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
                await session.execute(
                    update(cls.model)
                    .values(status=data["status"])
                    .filter_by(ID=ID, assigned_user=data["user_id"])
                )
            else:
                await session.execute(update(cls.model).values(**data).filter_by(ID=ID))
            await session.commit()

        return "ok"
