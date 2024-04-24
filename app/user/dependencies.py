from typing import Callable

from fastapi import Depends, Request, HTTPException
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import (
    InvalidTokenException,
    IncorrectTokenException,
    NoAccessException,
    MissTokenException,
)
from app.user.dao import UserDAO
from app.user.models import User


def get_access_token(request: Request):
    token = request.cookies.get("token", None)
    if not token:
        raise MissTokenException
    return token


def get_user(is_admin: bool = False) -> Callable:

    async def inner(token: str = Depends(get_access_token)):

        try:
            token = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        except JWTError:
            raise InvalidTokenException

        if "uid" not in token:
            raise IncorrectTokenException

        user: User = await UserDAO.fetch_one_or_none_with_tasks(ID=token["uid"])
        if not user:
            raise IncorrectTokenException

        if is_admin and not user.is_admin:
            raise NoAccessException
        return user

    return inner


get_current_user = get_user()
get_current_user_admin = get_user(is_admin=True)
