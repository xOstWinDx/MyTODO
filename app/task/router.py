from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from starlette import status

from app.task.dao import TaskDAO
from app.task.models import Task
from app.task.schemas import STaskCreate, STask
from app.user.dao import UserDAO
from app.user.dependencies import get_current_user, get_current_user_admin
from app.user.models import User
from app.back_tasks.celeryconf import send_notify

router = APIRouter(prefix="/tasks", tags=["Задачи"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_task(
    task_data: STaskCreate,
    assigned_user: int = None,
    user: User = Depends(get_current_user_admin),
):
    task: Task = await TaskDAO.add(
        **task_data.model_dump(),
        assigned_user=assigned_user,
        created_by=user.ID,
    )
    user: User = await UserDAO.fetch_one_or_none(ID=task.assigned_user)
    send_notify.delay(email=user.email, task=STask.model_validate(task).model_dump())


@router.get("/all")
@cache(expire=10)
async def get_all_tasks(user: User = Depends(get_current_user)):
    return await TaskDAO.fetch_all()


@router.get("/free")
@cache(expire=10)
async def get_free_tasks(user: User = Depends(get_current_user)):
    return await TaskDAO.fetch_all(assigned_user=None)


@router.patch("/{task_id}/set")
async def set_task(
    task_id: int, assigned_user_id: int, user: User = Depends(get_current_user_admin)
):
    task = await TaskDAO.update(task_id, assigned_user=assigned_user_id)
    user: User = await UserDAO.fetch_one_or_none(ID=task.assigned_user)
    send_notify.delay(email=user.email, task=STask.model_validate(task).model_dump())

    return task


@router.patch("/{task_id}")
async def take_task(task_id: int, user: User = Depends(get_current_user)):
    return await TaskDAO.update(task_id, assigned_user=user.ID)


@router.delete("/{task_id}")
async def take_task(task_id: int, user: User = Depends(get_current_user)):
    return await TaskDAO.delete(task_id, user.ID, user.is_admin)
