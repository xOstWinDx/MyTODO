import smtplib

from celery import Celery
from app.back_tasks.email_template import create_task_email_template
from app.config import settings

celery = Celery(
    "hello", broker="redis://localhost:6379", broker_connection_retry_on_startup=False
)


@celery.task
def send_notify(email: str, task: dict):
    email = create_task_email_template(task=task, email_to=email)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)
