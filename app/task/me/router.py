from fastapi import APIRouter, Depends

from app.task.dao import TaskDAO
from app.user.dependencies import get_current_user
from app.user.models import User

router = APIRouter(prefix="/me", tags=["Я"])


@router.patch("/{task_id}")
async def task_complete(task_id: int, user: User = Depends(get_current_user)):
    return await TaskDAO.update(task_id, user_id=user.ID, status=True)


@router.get("/assigned")
async def get_my_assigned_tasks(user: User = Depends(get_current_user)):
    return user.tasks


@router.get("/created")
async def get_my_created_task(user: User = Depends(get_current_user)):
    return await TaskDAO.fetch_all(created_by=user.ID)
