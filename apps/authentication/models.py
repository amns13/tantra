from __future__ import annotations

import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.urls import reverse


class UserManager(BaseUserManager):
    """Manager class for custom User model."""

    def create_user(self, username: str, email: str,
                    password: str, **extra_fields: bool) -> User:
        """Create a user.

        Args:
            username (str): username of the user. It should be unique.
            email (str): Email of the user. It should be unique
            password (str): password of the user.

        Returns:
            User: Created user object.
        """
        if username is None:
            raise TypeError("Users must have a username")

        if email is None:
            raise TypeError("Users must have an email")

        if password is None:
            raise TypeError("Users must have a password")

        user: User = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username: str, email: str,
                         password: str, **extra_fields: bool) -> User:
        """Function to create a superuser.

        Args:
            username (str): Username of the superuser.
            email (str): Email of the superuser.
            password (str): Password of the superuser.

        Returns:
            User: Created superuser.
        """
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model"""
    # first_name and last_name are not required as this classs uses full_name.
    first_name = None
    last_name = None

    id = models.UUIDField(
        "Unique ID",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="A unique Primary Key of the object.")
    full_name = models.CharField(
        "Full Name",
        max_length=127,
        blank=True,
        help_text="Full Name of the user.")

    objects = UserManager()

    def __str__(self) -> str:
        return self.username

    def get_full_name(self) -> str:
        return self.full_name
