from __future__ import annotations

import uuid
from typing import Optional

from core.models import BaseModel
from core.utils import decode_token, get_token
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


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


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """Custom User model"""
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        error_messages={
            'unique': _('A user with that username already exists.')},
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            UnicodeUsernameValidator()])
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.')},
        help_text=_('Required. A valid email address.'))
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_verified = models.BooleanField(_('verification status'), default=False)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self) -> str:
        return self.username

    def get_email_verification_token(self) -> str:
        """Generates a token for email verification"""
        uuid = str(self.uuid)
        return get_token(
            settings.ACCOUNT_VERIFICATION_TOKEN_EXPIRY, verify_email=uuid)

    def get_password_reset_token(self) -> str:
        """Generates a token for password reset"""
        uuid = str(self.uuid)
        return get_token(settings.PASSWORD_RESET_TOKEN_EXPIRY,
                         reset_password=uuid)

    @staticmethod
    def verify_email_verification_token(token: str) -> Optional[User]:
        try:
            uuid = decode_token(token)['verify_email']
        except BaseException:
            return None
        return User.objects.filter(uuid=uuid).first()

    @staticmethod
    def verify_password_reset_token(token: str) -> Optional[User]:
        try:
            uuid = decode_token(token)['reset_password']
        except BaseException:
            return None
        return User.objects.filter(uuid=uuid).first()
