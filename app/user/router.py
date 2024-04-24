from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi_cache.decorator import cache

from app.user.auth import hash_password, auth_user, create_access_token
from app.user.dao import UserDAO
from app.user.dependencies import get_current_user, get_current_user_admin
from app.user.models import User
from app.user.schemas import SUserCreate, SUser, SUserWithTask

router = APIRouter(prefix="/auth", tags=["Пользователи"])


@router.post("/reg", status_code=201)
async def register(user_data: SUserCreate):
    exist_user = await UserDAO.fetch_one_or_none(email=user_data.email)
    if exist_user:
        raise HTTPException(status_code=409)
    await UserDAO.add(
        email=user_data.email, hashed_password=hash_password(user_data.hashed_password)
    )


@router.post("/signup")
async def signup(response: Response, user_data: SUserCreate):
    user = await auth_user(user_data.email, user_data.hashed_password)
    response.set_cookie(
        key="token", value=create_access_token(user), max_age=3600, httponly=True
    )


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("token")


@router.get("/")
@cache(expire=10)
async def get_all_users(
    withtasks: bool = False, user: User = Depends(get_current_user_admin)
) -> list[dict[str, SUserWithTask]] | list[dict[str, SUser]]:
    if withtasks:
        users: list[dict[str, SUserWithTask]] = await UserDAO.fetch_all_with_tasks()
    else:
        users: list[dict[str, SUser]] = await UserDAO.fetch_all()
    return users
