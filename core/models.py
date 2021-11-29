from django.db import models

from . import mixins


class BaseModel(mixins.IDModelMixin, mixins.CurrentUserModelMixin,
                mixins.SoftDeleteModelMixin, mixins.TimeStampModelMixin):
    """Base Model from which all other models inherit"""

    class Meta:
        abstract = True

    def delete(self):
        self.is_active = False
        self.save()
