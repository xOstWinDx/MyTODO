import datetime

import pytest
from sqlalchemy import insert

from app.config import settings
from app.database import Base, engine, get_async_session
from app.main import lifespan
from app.user.models import User  # noqa
from app.task.models import Task  # noqa
from app.main import app as fastapi_app

from httpx import AsyncClient, ASGITransport


@pytest.fixture(scope="session", autouse=True)
async def test_prepare_data_base():
    assert settings.MODE == "TEST"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with get_async_session() as session:
        user1 = insert(User).values(
            email="test@test.ru",
            hashed_password="$2b$12$qqzxuoVN4NP/0wIdj57ltO9LLBoov.YE9b6MdvJGecvb3wPqT.6Di",  # noqa testtest
            is_admin=False,
        )
        user2 = insert(User).values(
            email="admin@test.ru",
            hashed_password="$2b$12$qqzxuoVN4NP/0wIdj57ltO9LLBoov.YE9b6MdvJGecvb3wPqT.6Di",  # noqa testtest
            is_admin=True,
        )

        task1 = insert(Task).values(
            title="Полить цветы",
            description="Необходимо полить все цветы в комнате",
            created_at=datetime.datetime.now(datetime.UTC),
            created_by=1,
            deadline=datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=2),
            assigned_user=2,
            status=False,
        )

        task2 = insert(Task).values(
            title="Выкинуть мусор",
            description="Необходимо выкинуть весь мусор",
            created_at=datetime.datetime.now(datetime.UTC),
            created_by=2,
            deadline=datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
            assigned_user=2,
            status=False,
        )
        task3 = insert(Task).values(
            title="Выполнить задачу №5",
            description="Необходимо выполнить поставленную задачу",
            created_at=datetime.datetime.now(datetime.UTC),
            created_by=2,
            deadline=datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
            assigned_user=None,
            status=False,
        )

        await session.execute(user1)
        await session.execute(user2)
        await session.execute(task1)
        await session.execute(task2)
        await session.execute(task3)
        await session.commit()
    yield
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def ac():
    async with lifespan(fastapi_app):
        async with AsyncClient(
            transport=ASGITransport(app=fastapi_app), base_url="http://test"
        ) as ac:
            yield ac


@pytest.fixture(scope="session")
async def auth_ac():
    async with lifespan(fastapi_app):
        async with AsyncClient(
            transport=ASGITransport(app=fastapi_app), base_url="http://test"
        ) as aca:
            r = await aca.post(
                url="/auth/signup",
                json={
                    "email": "admin@test.ru",
                    "hashed_password": "testtest",
                },
            )
            assert r.status_code == 200
            assert aca.cookies["token"]
            yield aca
