from fastapi import APIRouter, HTTPException

from app.user.auth.auth import verify_password, hash_password
from app.user.dao import UserDAO
from app.user.models import User
from app.user.schema import SUserCreate

router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post("/reg")
async def register(user_data: SUserCreate):
    exist_user = await UserDAO.fetch_one(email=user_data.email)
    if exist_user:
        raise HTTPException(status_code=409)
    await UserDAO.add(
        email=user_data.email, hashed_password=hash_password(user_data.password)
    )


@router.post("/signup")
async def signup(user_data: SUserCreate):
