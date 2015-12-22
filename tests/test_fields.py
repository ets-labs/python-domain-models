"""Domain model fields tests."""

import datetime
import time

import six
import unittest2 as unittest

from domain_models import model
from domain_models import fields
from domain_models import errors


class RelatedModel(model.DomainModel):
    """Example model that is used for testing relations."""


class ExampleModel(model.DomainModel):
    """Example model."""

    field = fields.Field()
    field_default = fields.Field(default=123)
    field_default_callable = fields.Field(default=time.time)

    bool_field = fields.Bool()

    int_field = fields.Int()
    float_field = fields.Float()

    string_field = fields.String()
    binary_field = fields.Binary()

    date_field = fields.Date()
    datetime_field = fields.DateTime()

    model_field = fields.Model(RelatedModel)


class FieldTest(unittest.TestCase):
    """Base field tests."""

    def test_get_set(self):
        """Test getting and setting of field value."""
        model = ExampleModel()
        model.field = 123
        self.assertEquals(model.field, 123)

    def test_reset_value(self):
        """Test resetting of value."""
        model = ExampleModel()

        model.field = 'Some value'
        model.field = None

        self.assertIsNone(model.field)

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


class BoolTest(unittest.TestCase):
    """Bool field tests."""

    def test_set_value(self):
        """Test setting of correct value."""
        model = ExampleModel()

        model.bool_field = True

        self.assertIs(model.bool_field, True)

    def test_set_value_conversion_int(self):
        """Test setting of correct value."""
        model = ExampleModel()

        model.bool_field = 1

        self.assertIs(model.bool_field, True)

    def test_set_value_conversion_str(self):
        """Test setting of correct value."""
        model = ExampleModel()

        model.bool_field = '1'

        self.assertIs(model.bool_field, True)

    def test_set_value_conversion_empty_str(self):
        """Test setting of correct value."""
        model = ExampleModel()

        model.bool_field = ''

        self.assertIs(model.bool_field, False)

    def test_reset_value(self):
        """Test resetting of value."""
        model = ExampleModel()

        model.bool_field = True
        model.bool_field = None

        self.assertIsNone(model.bool_field)


class IntTest(unittest.TestCase):
    """Int field tests."""

    def test_set_value(self):
        """Test setting of correct value."""
        model = ExampleModel()
        number = 2

        model.int_field = number

        self.assertEqual(model.int_field, number)

    def test_set_value_conversion_float(self):
        """Test setting of correct value."""
        model = ExampleModel()

        model.int_field = 1.0

        self.assertEqual(model.int_field, 1)

    def test_set_value_conversion_str(self):
        """Test setting of correct value."""
        model = ExampleModel()

        model.int_field = '1'

        self.assertEqual(model.int_field, 1)

    def test_reset_value(self):
        """Test resetting of value."""
        model = ExampleModel()
        number = 2

        model.int_field = number
        model.int_field = None

        self.assertIsNone(model.int_field)

    def test_set_incorrect(self):
        """Test setting of incorrect value."""
        model = ExampleModel()

        with self.assertRaises(TypeError):
            model.int_field = object()

        with self.assertRaises(ValueError):
            model.int_field = ''


class FloatTest(unittest.TestCase):
    """Float field tests."""

    def test_set_value(self):
        """Test setting of correct value."""
        model = ExampleModel()
        number = 2.22

        model.float_field = number

        self.assertEqual(model.float_field, number)

    def test_set_value_conversion_str(self):
        """Test setting of correct value."""
        model = ExampleModel()

        model.float_field = '2.22'

        self.assertEqual(model.float_field, 2.22)

    def test_reset_value(self):
        """Test resetting of value."""
        model = ExampleModel()
        number = 2.22

        model.float_field = number
        model.float_field = None

        self.assertIsNone(model.float_field)

    def test_set_incorrect(self):
        """Test setting of incorrect value."""
        model = ExampleModel()

        with self.assertRaises(TypeError):
            model.float_field = object()


class StringTest(unittest.TestCase):
    """String field tests."""

    def test_set_value(self):
        """Test setting of correct value."""
        model = ExampleModel()
        data = 'Hello, world!'

        model.string_field = data

        self.assertEqual(model.string_field, data)

    def test_set_value_conversion_float(self):
        """Test setting of correct value."""
        model = ExampleModel()

        model.string_field = 2.22

        self.assertEqual(model.string_field, '2.22')

    def test_reset_value(self):
        """Test resetting of value."""
        model = ExampleModel()
        data = 'Hello, world!'

        model.string_field = data
        model.string_field = None

        self.assertIsNone(model.string_field)


class BinaryTest(unittest.TestCase):
    """Binary field tests."""

    def test_set_value(self):
        """Test setting of correct value."""
        model = ExampleModel()
        data = six.b('Hello, world!')

        model.binary_field = data

        self.assertEqual(model.binary_field, data)

    def test_reset_value(self):
        """Test resetting of value."""
        model = ExampleModel()
        data = six.b('Hello, world!')

        model.binary_field = data
        model.binary_field = None

        self.assertIsNone(model.binary_field)


class DateTest(unittest.TestCase):
    """Date field tests."""

    def test_set_value(self):
        """Test setting of correct value."""
        model = ExampleModel()
        today = datetime.date.today()

        model.date_field = today

        self.assertEqual(model.date_field, today)

    def test_reset_value(self):
        """Test resetting of value."""
        model = ExampleModel()
        today = datetime.date.today()

        model.date_field = today
        model.date_field = None

        self.assertIsNone(model.date_field)

    def test_set_incorrect(self):
        """Test setting of incorrect value."""
        model = ExampleModel()
        some_object = object()

        with self.assertRaises(TypeError):
            model.date_field = some_object


class DateTimeTest(unittest.TestCase):
    """Date and time field tests."""

    def test_set_value(self):
        """Test setting of correct value."""
        model = ExampleModel()
        now = datetime.datetime.utcnow()

        model.datetime_field = now

        self.assertEqual(model.datetime_field, now)

    def test_reset_value(self):
        """Test resetting of value."""
        model = ExampleModel()
        now = datetime.datetime.utcnow()

        model.datetime_field = now
        model.datetime_field = None

        self.assertIsNone(model.datetime_field)

    def test_set_incorrect(self):
        """Test setting of incorrect value."""
        model = ExampleModel()
        some_object = object()

        with self.assertRaises(TypeError):
            model.datetime_field = some_object


class ModelTest(unittest.TestCase):
    """Date and time field tests."""

    def test_set_value(self):
        """Test setting of correct value."""
        model = ExampleModel()
        related_model = RelatedModel()

        model.model_field = related_model

        self.assertEqual(model.model_field, related_model)

    def test_reset_value(self):
        """Test resetting of value."""
        model = ExampleModel()
        related_model = RelatedModel()

        model.model_field = related_model
        model.model_field = None

        self.assertIsNone(model.model_field)

    def test_set_incorrect(self):
        """Test setting of incorrect value."""
        model = ExampleModel()
        some_object = object()

        with self.assertRaises(TypeError):
            model.model_field = some_object
