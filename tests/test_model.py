"""Model unittests."""

import six
import unittest2 as unittest

from domain_models import model
from domain_models import fields
from domain_models import errors


class BaseModelsTests(unittest.TestCase):
    """Basic model tests."""

    def test_set_and_get_attrs(self):
        """Test setting and getting of domain model attributes."""
        class User(model.DomainModel):
            """Test user domain model."""

            id = fields.Int()
            email = fields.String()
            first_name = fields.Unicode()
            last_name = fields.Unicode()
            gender = fields.String()
            birth_date = fields.String()

        user1 = User()
        user1.id = 1
        user1.email = 'example1@example.com'
        user1.first_name = 'John'
        user1.last_name = 'Smith'
        user1.gender = 'male'
        user1.birth_date = '05/04/1988'

        user2 = User()
        user2.id = 2
        user2.email = 'example2@example.com'
        user2.first_name = 'Jane'
        user2.last_name = 'Smith'
        user2.gender = 'female'
        user2.birth_date = '05/04/1985'

        self.assertEqual(user1.id, 1)
        self.assertEqual(user1.email, 'example1@example.com')
        self.assertEqual(user1.first_name, six.u('John'))
        self.assertEqual(user1.last_name, six.u('Smith'))
        self.assertEqual(user1.gender, 'male')
        self.assertEqual(user1.birth_date, '05/04/1988')

        self.assertEqual(user2.id, 2)
        self.assertEqual(user2.email, 'example2@example.com')
        self.assertEqual(user2.first_name, six.u('Jane'))
        self.assertEqual(user2.last_name, six.u('Smith'))
        self.assertEqual(user2.gender, 'female')
        self.assertEqual(user2.birth_date, '05/04/1985')

    def test_data_attr(self):
        """Test model's __data__ attribute."""
        class User(model.DomainModel):
            """Test user domain model."""

            id = fields.Int()
            email = fields.String()
            first_name = fields.Unicode()
            last_name = fields.Unicode()
            gender = fields.String()
            birth_date = fields.String()

        user1 = User()
        user1.id = 1
        user1.email = 'example1@example.com'
        user1.first_name = 'John'
        user1.last_name = 'Smith'
        user1.gender = 'male'
        user1.birth_date = '05/04/1988'

        user2 = User()
        user2.id = 2
        user2.email = 'example2@example.com'
        user2.first_name = 'Jane'
        user2.last_name = 'Smith'
        user2.gender = 'female'
        user2.birth_date = '05/04/1985'

        self.assertEquals(user1.__data__, dict(id=1,
                                               email='example1@example.com',
                                               first_name='John',
                                               last_name='Smith',
                                               gender='male',
                                               birth_date='05/04/1988'))
        self.assertEquals(user2.__data__, dict(id=2,
                                               email='example2@example.com',
                                               first_name='Jane',
                                               last_name='Smith',
                                               gender='female',
                                               birth_date='05/04/1985'))

    def test_not_valid_unique_key_field(self):
        """Test that error is raised when unique key is not correct."""
        with self.assertRaises(errors.Error):
            class Model(model.DomainModel):
                """Test model."""

                __unique_key__ = fields.Field()

    def test_not_valid_unique_key_object(self):
        """Test that error is raised when unique key is not correct."""
        with self.assertRaises(errors.Error):
            class Model(model.DomainModel):
                """Test model."""

                __unique_key__ = object()

    def test_not_valid_unique_key_scalar(self):
        """Test that error is raised when unique key is not correct."""
        with self.assertRaises(errors.Error):
            class Model(model.DomainModel):
                """Test model."""

                __unique_key__ = 1

    def test_not_valid_view_key_field(self):
        """Test that error is raised when view key is not correct."""
        with self.assertRaises(errors.Error):
            class Model(model.DomainModel):
                """Test model."""

                __view_key__ = fields.Field()

    def test_not_valid_view_key_object(self):
        """Test that error is raised when view key is not correct."""
        with self.assertRaises(errors.Error):
            class Model(model.DomainModel):
                """Test model."""

                __view_key__ = object()

    def test_not_valid_view_key_scalar(self):
        """Test that error is raised when view key is not correct."""
        with self.assertRaises(errors.Error):
            class Model(model.DomainModel):
                """Test model."""

                __view_key__ = 1

    def test_field_could_not_be_rebound_in_same_model(self):
        """Test that field could not be rebound."""
        with self.assertRaises(errors.Error):
            class Model(model.DomainModel):
                """Test model."""

                field = fields.Field()
                another_field = field

    def test_field_could_not_be_rebound_in_different_model(self):
        """Test that field could not be rebound."""
        class Model1(model.DomainModel):
            """Test model."""

            field = fields.Field()

        with self.assertRaises(errors.Error):
            class Model2(model.DomainModel):
                """Test model."""

                field = Model1.field


class ModelReprTests(unittest.TestCase):
    """Tests for model Pythonic representation."""

    def test_repr(self):
        """Test model __repr__()."""
        class User(model.DomainModel):
            """Test user domain model."""

            id = fields.Int()
            email = fields.String()
            first_name = fields.Unicode()
            last_name = fields.Unicode()
            gender = fields.String()
            birth_date = fields.String()

        user = User()
        user.id = 1
        user.email = 'example1@example.com'
        user.first_name = 'John'
        user.last_name = 'Smith'
        user.gender = 'male'
        user.birth_date = '05/04/1988'

        user_repr = repr(user)

        self.assertIn('test_model.User', user_repr)
        self.assertIn('id=1', user_repr)
        self.assertIn('email=\'example1@example.com\'', user_repr)
        self.assertIn('first_name={0}'.format(repr(six.u('John'))), user_repr)
        self.assertIn('last_name={0}'.format(repr(six.u('Smith'))), user_repr)
        self.assertIn('gender=\'male\'', user_repr)
        self.assertIn('birth_date=\'05/04/1988\'', user_repr)


class ModelStrTests(unittest.TestCase):
    """Tests for model string representation."""

    def test_str_with_single_view_key(self):
        """Test model __str__()."""
        class User(model.DomainModel):
            """Test user domain model."""

            id = fields.Int()
            email = fields.String()
            first_name = fields.Unicode()
            last_name = fields.Unicode()
            gender = fields.String()
            birth_date = fields.String()

            __view_key__ = [id]

        user = User()
        user.id = 1
        user.email = 'example1@example.com'
        user.first_name = 'John'
        user.last_name = 'Smith'
        user.gender = 'male'
        user.birth_date = '05/04/1988'

        user_str = str(user)

        self.assertIn('test_model.User', user_str)
        self.assertIn('id=1', user_str)

        self.assertNotIn('example1@example.com', user_str)
        self.assertNotIn(six.u('John'), user_str)
        self.assertNotIn(six.u('Smith'), user_str)
        self.assertNotIn('male', user_str)
        self.assertNotIn('05/04/1988', user_str)

    def test_str_with_multiple_view_keys(self):
        """Test model __str__()."""
        class User(model.DomainModel):
            """Test user domain model."""

            id = fields.Int()
            email = fields.String()
            first_name = fields.Unicode()
            last_name = fields.Unicode()
            gender = fields.String()
            birth_date = fields.String()

            __view_key__ = (id, email)

        user = User()
        user.id = 1
        user.email = 'example1@example.com'
        user.first_name = 'John'
        user.last_name = 'Smith'
        user.gender = 'male'
        user.birth_date = '05/04/1988'

        user_str = str(user)

        self.assertIn('test_model.User', user_str)
        self.assertIn('id=1', user_str)
        self.assertIn('email=example1@example.com', user_str)

        self.assertNotIn(six.u('John'), user_str)
        self.assertNotIn(six.u('Smith'), user_str)
        self.assertNotIn('male', user_str)
        self.assertNotIn('05/04/1988', user_str)

    def test_str_without_view_key(self):
        """Test model __str__()."""
        class User(model.DomainModel):
            """Test user domain model."""

            id = fields.Int()
            email = fields.String()
            first_name = fields.Unicode()
            last_name = fields.Unicode()
            gender = fields.String()
            birth_date = fields.String()

        user = User()
        user.id = 1
        user.email = 'example1@example.com'
        user.first_name = 'John'
        user.last_name = 'Smith'
        user.gender = 'male'
        user.birth_date = '05/04/1988'

        self.assertEquals(str(user), repr(user))


class ModelSlotsOptimizationTests(unittest.TestCase):
    """Tests for model slots optimizations."""

    def test_model_slots(self):
        """Test model slots optimization."""
        class Model(model.DomainModel):
            """Test model."""

            field = fields.Field()

        test_model = Model()
        test_model.field = 'test'

        self.assertEquals(test_model.field, 'test')
        with self.assertRaises(AttributeError):
            test_model.undefined_field = 'NaN'

    def test_model_slots_disabling(self):
        """Test disabling of model slots optimization."""
        class Model(model.DomainModel):
            """Test model."""

            field = fields.Field()
            __slots_optimization__ = False

        test_model = Model()
        test_model.field = 'test'
        test_model.undefined_field = 'NaN'

        self.assertEquals(test_model.field, 'test')
        self.assertEquals(test_model.undefined_field, 'NaN')


class ModelsEqualityComparationsTests(unittest.TestCase):
    """Tests for models equality comparations."""

    def test_models_equal_single_key(self):
        """Test models equality comparator based on unique key."""
        class Model(model.DomainModel):
            """Test domain model with single unique key."""

            id = fields.Int()
            __unique_key__ = [id]

        user11 = Model()
        user11.id = 1

        user12 = Model()
        user12.id = 1

        self.assertTrue(user11 == user12)
        self.assertFalse(user11 != user12)

    def test_models_not_equal_single_key(self):
        """Test that models are not equal."""
        class Model(model.DomainModel):
            """Test domain model with single unique key."""

            id = fields.Int()
            __unique_key__ = [id]

        user1 = Model()
        user1.id = 1

        user2 = Model()
        user2.id = 2

        self.assertFalse(user1 == user2)
        self.assertTrue(user1 != user2)

    def test_models_equal_multiple_keys(self):
        """Test models equality comparator based on unique key."""
        class Model(model.DomainModel):
            """Test domain model with multiple unique key."""

            id = fields.Int()
            email = fields.String()
            __unique_key__ = (id, email)

        user11 = Model()
        user11.id = 1
        user11.email = 'john@example.com'

        user12 = Model()
        user12.id = 1
        user12.email = 'john@example.com'

        self.assertTrue(user11 == user12)
        self.assertFalse(user11 != user12)

    def test_models_not_equal_multiple_keys(self):
        """Test that models are not equal."""
        class Model(model.DomainModel):
            """Test domain model with multiple unique key."""

            id = fields.Int()
            email = fields.String()
            __unique_key__ = (id, email)

        user1 = Model()
        user1.id = 1
        user1.email = 'john@example.com'

        user2 = Model()
        user2.id = 2
        user2.email = 'jane@example.com'

        self.assertFalse(user1 == user2)
        self.assertTrue(user1 != user2)

    def test_models_not_equal_multiple_keys_first_equal(self):
        """Test that models are not equal."""
        class Model(model.DomainModel):
            """Test domain model with multiple unique key."""

            id = fields.Int()
            email = fields.String()
            __unique_key__ = (id, email)

        user11 = Model()
        user11.id = 1
        user11.email = 'john@example.com'

        user12 = Model()
        user12.id = 1
        user12.email = 'jane@example.com'

        self.assertFalse(user11 == user12)
        self.assertTrue(user11 != user12)

    def test_models_not_equal_different_classes(self):
        """Test that models are not equal."""
        class Model1(model.DomainModel):
            """Test domain model with single unique key."""

            id = fields.Int()
            __unique_key__ = [id]

        class Model2(model.DomainModel):
            """Test domain model with single unique key."""

            id = fields.Int()
            __unique_key__ = [id]

        user1 = Model1()
        user1.id = 1

        user2 = Model2()
        user2.id = 1

        self.assertFalse(user1 == user2)
        self.assertTrue(user1 != user2)

    def test_models_not_equal_scalar_value(self):
        """Test that model and scalar value are not equal."""
        class Model(model.DomainModel):
            """Test domain model with single unique key."""

            id = fields.Int()
            __unique_key__ = [id]

        user1 = Model()
        user1.id = 1

        self.assertFalse(user1 == 1)
        self.assertTrue(user1 != 1)

    def test_models_not_equal_unknown_unique_key(self):
        """Test that models are not equal."""
        class Model(model.DomainModel):
            """Test domain model without unique key."""

            id = fields.Int()

        user1 = Model()
        user1.id = 1

        user2 = Model()
        user2.id = 1

        self.assertFalse(user1 == user2)
        self.assertTrue(user1 != user2)

    def test_same_models_equal_unknown_unique_key(self):
        """Test that models are not equal."""
        class Model(model.DomainModel):
            """Test domain model without unique key."""

            id = fields.Int()

        user1 = Model()
        user1.id = 1

        self.assertTrue(user1 == user1)
        self.assertFalse(user1 != user1)

    def test_non_equal_models_in_set_single_key(self):
        """Test that non-equal models work properly with sets."""
        class Model(model.DomainModel):
            """Test domain model with single unique key."""

            id = fields.Int()
            __unique_key__ = [id]

        user1 = Model()
        user1.id = 1
        user2 = Model()
        user2.id = 2
        user3 = Model()
        user3.id = 3

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 3)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)

    def test_equal_models_in_set_single_key(self):
        """Test that equal models work properly with sets."""
        class Model(model.DomainModel):
            """Test domain model with single unique key."""

            id = fields.Int()
            __unique_key__ = [id]

        user1 = Model()
        user1.id = 1
        user2 = Model()
        user2.id = 1
        user3 = Model()
        user3.id = 1

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 1)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)

    def test_non_equal_models_in_set_multiple_keys(self):
        """Test that non-equal models work properly with sets."""
        class Model(model.DomainModel):
            """Test domain model with multiple unique key."""

            id = fields.Int()
            email = fields.String()
            __unique_key__ = (id, email)

        user1 = Model()
        user1.id = 1
        user1.email = 'email1@example.com'
        user2 = Model()
        user2.id = 2
        user2.email = 'email2@example.com'
        user3 = Model()
        user3.id = 3
        user3.email = 'email3@example.com'

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 3)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)

    def test_equal_models_in_set_multiple_keys(self):
        """Test that equal models work properly with sets."""
        class Model(model.DomainModel):
            """Test domain model with multiple unique key."""

            id = fields.Int()
            email = fields.String()
            __unique_key__ = (id, email)

        user1 = Model()
        user1.id = 1
        user1.email = 'email1@example.com'
        user2 = Model()
        user2.id = 1
        user2.email = 'email1@example.com'
        user3 = Model()
        user3.id = 1
        user3.email = 'email1@example.com'

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 1)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)

    def test_non_equal_models_in_set_without_unique_key(self):
        """Test that non-equal models work properly with sets."""
        class Model(model.DomainModel):
            """Test domain model without unique key."""

            id = fields.Int()

        user1 = Model()
        user1.id = 1
        user2 = Model()
        user2.id = 2
        user3 = Model()
        user3.id = 3

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 3)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)

    def test_equal_models_in_set_without_unique_key(self):
        """Test that equal models work properly with sets."""
        class Model(model.DomainModel):
            """Test domain model without unique key."""

            id = fields.Int()

        user1 = Model()
        user1.id = 1
        user2 = user1
        user3 = user1

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 1)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)
