import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class STaskCreate(BaseModel):
    title: str
    description: str
    deadline: Optional[datetime.datetime]


class STask(STaskCreate):
    model_config = ConfigDict(from_attributes=True)
    ID: int
    created_at: datetime.datetime
    status: bool
    assigned_user: Optional[int] = None
    created_by: int
