from typing import Optional

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def send_account_verification_mail(**kwargs) -> None:
    """Signal to send account verification email on sign up"""
    user: Optional[User] = kwargs.get("instance")
    if user and kwargs.get("created"):
        user.send_email_verification_email()
