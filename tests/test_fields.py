"""Domain model fields tests."""

import unittest2 as unittest

from domain_models import model
from domain_models import fields


class ExampleModel(model.DomainModel):
    """Example model."""

    field = fields.Field()


class FieldTest(unittest.TestCase):
    """Base field tests."""

    def test_get_set(self):
        """Test getting and setting of field value."""
        model = ExampleModel()
        model.field = 123
        self.assertEquals(model.field, 123)
