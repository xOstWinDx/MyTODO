from fastapi import HTTPException
from starlette import status


class AuthException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectEmailOrPasswordException(AuthException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Не верный Email или Password"


class InvalidTokenException(AuthException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Невалидный токен"


class MissTokenException(AuthException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Вы не авторизованы"


class IncorrectTokenException(AuthException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверный токен"


class NoAccessException(AuthException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "У вас нет доступа :("
