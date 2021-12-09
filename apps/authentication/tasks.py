from django.core.mail import EmailMessage
from celery import shared_task


@shared_task
def send_email(mail_object: EmailMessage) -> None:
    mail_object.send()
