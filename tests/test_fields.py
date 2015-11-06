"""Domain model fields tests."""

import time

import unittest2 as unittest

from domain_models import model
from domain_models import fields
from domain_models import errors


class ExampleModel(model.DomainModel):
    """Example model."""

    field = fields.Field()
    field_default = fields.Field(default=123)
    field_default_callable = fields.Field(default=time.time)


class FieldTest(unittest.TestCase):
    """Base field tests."""

    def test_get_set(self):
        """Test getting and setting of field value."""
        model = ExampleModel()
        model.field = 123
        self.assertEquals(model.field, 123)

    def test_model_cls_could_not_be_rebound(self):
        """Test that field model class could not be rebound."""
        class Model(model.DomainModel):
            """Test model."""

        field = fields.Field()

        field.bind_model_cls(Model)
        with self.assertRaises(errors.Error):
            field.bind_model_cls(Model)

    def test_field_default(self):
        """Test field default value."""
        model = ExampleModel()
        self.assertEquals(model.field_default, 123)

    def test_field_default_callable(self):
        """Test field default callable value."""
        model1 = ExampleModel()
        time.sleep(0.1)
        model2 = ExampleModel()

        self.assertGreater(model2.field_default_callable,
                           model1.field_default_callable)
