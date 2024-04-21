import datetime
from typing import Optional

from pydantic import BaseModel


class STaskCreate(BaseModel):
    title: str
    description: str
    deadline: Optional[datetime.datetime]
