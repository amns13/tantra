from typing import Optional, Sequence

from celery import shared_task
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_email(subject: str,
               body: str,
               from_email: str,
               to: Optional[Sequence[str]] = None,
               attachment_body: Optional[str] = None,
               attachment_mime_type: Optional[str] = None):
    email = EmailMultiAlternatives(
        subject=subject, body=body, from_email=from_email, to=to
    )
    if attachment_body and attachment_mime_type:
        email.attach_alternative(attachment_body, attachment_mime_type)

    email.send()
