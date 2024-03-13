from typing import NoReturn

from celery import shared_task
from django.core.mail import send_mail

from server import settings


@shared_task
def send_email_message(email_address: str, subject: str, message: str) -> NoReturn:
    send_mail(
        subject=subject,
        message=message,
        html_message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email_address]
    )
