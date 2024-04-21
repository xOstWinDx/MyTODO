from fastapi import FastAPI
from app.user.router import router as user_router
from app.task.router import router as task_router
from app.task.me.router import router as me_router

app = FastAPI(title="Моё TODO приложение")

app.include_router(user_router)
app.include_router(task_router)
app.include_router(me_router)
