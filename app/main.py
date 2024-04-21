from fastapi import FastAPI
from app.user.router import router as user_router

app = FastAPI(title="Моё TODO приложение")

app.include_router(user_router)
