import uuid

from django.db import models


class BaseModel(models.Model):
    """Base Model. Consists of common fields used across all other models."""
    id = models.UUIDField(
        "Unique ID",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="A unique Primary Key of the object.")
    created_at = models.DateTimeField(
        "Creation Time",
        auto_now_add=True,
        help_text="Creation time of the object. Automatically set at the time of creation.")
    last_modified_at = models.DateTimeField(
        "Last Modification Time",
        auto_now=True,
        help_text="Updated everytime any model field is updated.")
    is_active = models.BooleanField(
        "Is Active",
        default=True,
        help_text="Used to implement soft delete. If false, then object is considered deleted.")

    class Meta:
        abstract = True
