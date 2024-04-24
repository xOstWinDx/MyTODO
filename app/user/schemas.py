from typing import Annotated

from annotated_types import MinLen
from pydantic import BaseModel, EmailStr, ConfigDict

from app.task.models import Task
from app.task.schemas import STask


class SUserCreate(BaseModel):
    email: EmailStr
    hashed_password: Annotated[str, MinLen(8)]


class SUser(SUserCreate):
    ID: int
    is_admin: bool


class SUserWithTask(SUser):
    model_config = ConfigDict(from_attributes=True)
    tasks: list[STask]
