from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt

from app.config import settings
from app.exceptions import IncorrectEmailOrPasswordException
from app.user.dao import UserDAO
from app.user.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user: User):
    payload = {"uid": user.ID}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


async def auth_user(email: str, password: str):
    exist_user: User = await UserDAO.fetch_one_or_none(email=email)
    if not exist_user:
        raise IncorrectEmailOrPasswordException
    if not verify_password(password, exist_user.hashed_password):
        raise IncorrectEmailOrPasswordException
    return exist_user
