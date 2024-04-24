import datetime

import pytest
from httpx import AsyncClient
from app.task.schemas import STask


async def test_task_get_all(auth_ac: AsyncClient):
    result = await auth_ac.get(url="/tasks/all")
    assert result.status_code == 200
    assert len(result.json()) == 3
    assert STask.model_validate(result.json()[0]["Task"])


async def test_task_get_free(auth_ac: AsyncClient):
    result = await auth_ac.get(url="/tasks/free")
    assert result.status_code == 200
    assert len(result.json()) == 1
    task = result.json()[0]["Task"]

    assert STask.model_validate(task)
    assert not task["assigned_user"]


async def test_task_add_new(auth_ac: AsyncClient):
    result = await auth_ac.post(
        url="/tasks/",
        json={
            "title": "Какая-то задача",
            "description": "Новая задача",
            "deadline": str(datetime.datetime.now(datetime.UTC)),
        },
    )
    assert result.status_code == 201


@pytest.mark.parametrize(
    "task_id, status_code",
    [("GG", 422), (999, 400), (3, 200)],
)
async def test_task_take(task_id, status_code, auth_ac: AsyncClient):
    result = await auth_ac.patch(url=f"/tasks/{task_id}")
    assert result.status_code == status_code


@pytest.mark.parametrize(
    "task_id, status_code",
    [
        (1, 200),
        ("GG", 422),
    ],
)
async def test_task_delete(task_id, status_code, auth_ac: AsyncClient):
    result = await auth_ac.delete(url=f"/tasks/{task_id}")
    assert result.status_code == status_code
