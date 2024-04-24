from email.message import EmailMessage
from typing import Annotated
import pytz

from pydantic import EmailStr
import datetime
from app.config import settings
from app.task.models import Task
from app.task.schemas import STask
import locale

locale.setlocale(locale.LC_ALL, "")


def create_task_email_template(
    task: Annotated[dict, STask],
    email_to: EmailStr,
):
    email = EmailMessage()
    email["Subject"] = "Новая задача"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to
    newdata = task["deadline"].astimezone(tz=pytz.timezone("Europe/Moscow"))

    email.set_content(
        f"""
                <h1>На вас назначена новая задача: {task.get('title')}</h1>
                <p>{task['description']}</p>
                <p>Выполнить задачу нужно до: {newdata.strftime("%H:%M   %d.%m.%y (%A)")}</p>
            """,
        subtype="html",
    )
    return email
