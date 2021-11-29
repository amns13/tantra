import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL


class IDModelMixin(models.Model):
    """Abstract class defining the id fields to be used by other models."""
    pkid = models.BigAutoField(
        _("primary Key"),
        primary_key=True,
        editable=False,
        help_text=_("Actual primary key"))
    uuid = models.UUIDField(
        _("unique id"),
        unique=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Unique ID for each instance. Used in Foreign Keys and in apis"))

    class Meta:
        abstract = True


class TimeStampModelMixin(models.Model):
    """Mixin declaring the timestamp fields."""
    created_at = models.DateTimeField(
        _("creation time"),
        auto_now_add=True,
        help_text=_("Creation time of the object. Automatically set at the time of creation."))
    updated_at = models.DateTimeField(
        _("last update time"),
        auto_now=True,
        help_text=_("Updated everytime any model field is updated."))

    class Meta:
        abstract = True


class SoftDeleteModelMixin(models.Model):
    """Mixin declaring is_active field for soft deleing"""
    is_active = models.BooleanField(
        _("is active"),
        default=True,
        help_text=_("Used to implement soft delete. If false, then object is considered deleted."))

    class Meta:
        abstract = True


class CurrentUserModelMixin(models.Model):
    """Mixin defining attributes to check the user who did the changes."""
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_('created by'),
        help_text=_('User who first creates this instance. This can be null.'),
        to_field=settings.DEFAULT_FK_REFERENCE_FIELD)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_('modified by'),
        help_text=_('User who last updated the instance.'),
        to_field=settings.DEFAULT_FK_REFERENCE_FIELD)

    class Meta:
        abstract = True
