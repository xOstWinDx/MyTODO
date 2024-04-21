from typing import Annotated

from annotated_types import MinLen
from pydantic import BaseModel, EmailStr


class SUserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, MinLen(8)]


class SUser(SUserCreate):
    ID: int
    is_admin: bool
