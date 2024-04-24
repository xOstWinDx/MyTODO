from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from app.user.auth import auth_user, create_access_token
from app.user.dependencies import get_current_user_admin


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await auth_user(email=email, password=password)
        token = create_access_token(user)
        request.session.update({"token": token})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False
        user = await get_current_user_admin(token=token)
        return True
