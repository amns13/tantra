from __future__ import annotations

from core.models import BaseModel
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
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
            raise TypeError(_("Users must have a username"))

        if email is None:
            raise TypeError(_("Users must have an email"))

        if password is None:
            raise TypeError(_("Users must have a password"))

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
    is_verified = models.BooleanField(
        _('verified'),
        default=False,
        help_text=_('Email verification status.'))

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self) -> str:
        return self.username
