from django.db import models

from . import model_mixins


class BaseModel(model_mixins.IDModelMixin, model_mixins.CurrentUserModelMixin,
                model_mixins.SoftDeleteModelMixin, model_mixins.TimeStampModelMixin):
    """Base Model from which all other models inherit"""

    class Meta:
        abstract = True

    def delete(self):
        self.is_active = False
        self.save()
