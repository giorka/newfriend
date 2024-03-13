from typing import NoReturn

from celery import shared_task


@shared_task
def send_email_message(email: str, subject: str, message: str) -> NoReturn:
    ...
