from fastapi import APIRouter, Depends

from app.task.dao import TaskDAO
from app.task.schemas import STaskCreate
from app.user.dependencies import get_current_user
from app.user.models import User


router = APIRouter(prefix="/tasks", tags=["Задачи"])


@router.post("/")
async def add_task(
    task_data: STaskCreate,
    assigned_user: int = None,
    user: User = Depends(get_current_user),
):
    await TaskDAO.add(
        title=task_data.title,
        description=task_data.description,
        created_by=user.ID,
        deadline=task_data.deadline,
        assigned_user=assigned_user,
    )


@router.get("/all")
async def get_all_tasks(user: User = Depends(get_current_user)):
    return await TaskDAO.fetch_all()


@router.get("/free")
async def get_free_tasks(user: User = Depends(get_current_user)):
    return await TaskDAO.fetch_all(assigned_user=None)


@router.patch("/{task_id}")
async def take_task(task_id: int, user: User = Depends(get_current_user)):
    return await TaskDAO.update(task_id, assigned_user=user.ID)
