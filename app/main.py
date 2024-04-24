from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqladmin import Admin
from redis import asyncio as aioredis

from app.admin.auth import AdminAuth
from app.admin.views import UserAdmin, TaskAdmin
from app.config import settings
from app.database import engine
from app.user.router import router as user_router
from app.task.router import router as task_router
from app.task.me.router import router as me_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(title="Моё TODO приложение", lifespan=lifespan)


app.include_router(user_router)
app.include_router(task_router)
app.include_router(me_router)

authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
admin = Admin(app, engine, authentication_backend=authentication_backend)


admin.add_view(UserAdmin)
admin.add_view(TaskAdmin)
