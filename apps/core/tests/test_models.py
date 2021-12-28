from django.db import connection
from django.db.models.base import ModelBase
from django.db.utils import OperationalError
from django.test import TestCase

from ..models import BaseModel


class AbstractModelMixinTestCase(TestCase):
    """
    Base class for tests of model mixins/abstract models.
    To use, subclass and specify the mixin class variable.
    A model using the mixin will be made available in self.model
    """

    @classmethod
    def setUpClass(cls):
        # Create a dummy model which extends the mixin. A RuntimeWarning will
        # occur if the model is registered twice
        if not hasattr(cls, 'model'):
            cls.model = ModelBase(
                '__TestModel__' +
                cls.mixin.__name__, (cls.mixin,),
                {'__module__': cls.mixin.__module__}
            )

        # Create the schema for our test model. If the table already exists,
        # will pass
        try:
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(cls.model)
            super(AbstractModelMixinTestCase, cls).setUpClass()
        except OperationalError:
            pass

    @classmethod
    def tearDownClass(self):
        # Delete the schema for the test model. If no table, will pass
        try:
            with connection.schema_editor() as schema_editor:
                schema_editor.delete_model(self.model)
            super(AbstractModelMixinTestCase, self).tearDownClass()
        except OperationalError:
            pass


class BaseModelTestCase(AbstractModelMixinTestCase):
    """Test abstract model."""
    mixin = BaseModel

    def setUp(self):
        self.model.objects.create()

    def test_object_created(self):
        obj = self.model.objects.first()
        self.assert_(obj.is_active)

    def test_object_deleted(self):
        obj = self.model.objects.first()
        obj_id = obj.pk
        obj.delete()
        deleted_obj = self.model.objects.get(pk=obj_id)
        self.assertFalse(deleted_obj.is_active)
