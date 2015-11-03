"""Model unittests."""

import six
import unittest2 as unittest

from domain_models import model
from domain_models import fields


class User(model.DomainModel):
    """Example user domain model."""

    id = fields.Int()
    email = fields.String()
    first_name = fields.Unicode()
    last_name = fields.Unicode()
    gender = fields.String()
    birth_date = fields.String()

    __view_key__ = [id, email]
    __unique_key__ = id


class ExampleModel1(model.DomainModel):
    """Example domain model."""

    id = fields.Int()
    __unique_key__ = id

class ExampleModel2(model.DomainModel):
    """Example domain model."""

    id = fields.Int()
    email = fields.String()
    __unique_key__ = (id, email)

class ExampleModel3(model.DomainModel):
    """Example domain model."""

    id = fields.Int()


class BaseModelsTests(unittest.TestCase):
    """Basic model tests."""

    def test_set_and_get_attrs(self):
        """Test setting and getting of domain model attributes."""
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


class ModelsEqualityComparationsTests(unittest.TestCase):
    """Tests for models equality comparations."""

    def test_models_equal_single_key(self):
        """Test models equality comparator based on unique key."""
        user11 = ExampleModel1()
        user11.id = 1

        user12 = ExampleModel1()
        user12.id = 1

        self.assertTrue(user11 == user12)
        self.assertFalse(user11 != user12)

    def test_models_not_equal_single_key(self):
        """Test that models are not equal."""
        user1 = ExampleModel1()
        user1.id = 1

        user2 = ExampleModel1()
        user2.id = 2

        self.assertFalse(user1 == user2)
        self.assertTrue(user1 != user2)

    def test_models_equal_multiple_keys(self):
        """Test models equality comparator based on unique key."""
        user11 = ExampleModel2()
        user11.id = 1
        user11.email = 'john@example.com'

        user12 = ExampleModel2()
        user12.id = 1
        user12.email = 'john@example.com'

        self.assertTrue(user11 == user12)
        self.assertFalse(user11 != user12)

    def test_models_not_equal_multiple_keys(self):
        """Test that models are not equal."""
        user1 = ExampleModel2()
        user1.id = 1
        user1.email = 'john@example.com'

        user2 = ExampleModel2()
        user2.id = 2
        user2.email = 'jane@example.com'

        self.assertFalse(user1 == user2)
        self.assertTrue(user1 != user2)

    def test_models_not_equal_multiple_keys_first_equal(self):
        """Test that models are not equal."""
        user11 = ExampleModel2()
        user11.id = 1
        user11.email = 'john@example.com'

        user12 = ExampleModel2()
        user12.id = 1
        user12.email = 'jane@example.com'

        self.assertFalse(user11 == user12)
        self.assertTrue(user11 != user12)

    def test_models_not_equal_different_classes(self):
        """Test that models are not equal."""
        user1 = ExampleModel1()
        user1.id = 1

        user2 = ExampleModel2()
        user2.id = 1

        self.assertFalse(user1 == user2)
        self.assertTrue(user1 != user2)

    def test_models_not_equal_scalar_value(self):
        """Test that models are not equal."""
        user1 = ExampleModel1()
        user1.id = 1

        self.assertFalse(user1 == 1)
        self.assertTrue(user1 != 1)

    def test_models_not_equal_unknown_unique_key(self):
        """Test that models are not equal."""
        user1 = ExampleModel3()
        user1.id = 1

        user2 = ExampleModel3()
        user2.id = 1

        self.assertFalse(user1 == user2)
        self.assertTrue(user1 != user2)

    def test_same_models_equal_unknown_unique_key(self):
        """Test that models are not equal."""
        user1 = ExampleModel3()
        user1.id = 1

        self.assertTrue(user1 == user1)
        self.assertFalse(user1 != user1)

    def test_non_equal_models_in_set_single_key(self):
        """Test that non-equal models work properly with sets."""
        user1 = ExampleModel1()
        user1.id = 1
        user2 = ExampleModel1()
        user2.id = 2
        user3 = ExampleModel1()
        user3.id = 3

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 3)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)

    def test_equal_models_in_set_single_key(self):
        """Test that equal models work properly with sets."""
        user1 = ExampleModel1()
        user1.id = 1
        user2 = ExampleModel1()
        user2.id = 1
        user3 = ExampleModel1()
        user3.id = 1

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 1)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)

    def test_non_equal_models_in_set_multiple_keys(self):
        """Test that non-equal models work properly with sets."""
        user1 = ExampleModel2()
        user1.id = 1
        user1.email = 'email1@example.com'
        user2 = ExampleModel2()
        user2.id = 2
        user2.email = 'email2@example.com'
        user3 = ExampleModel2()
        user3.id = 3
        user3.email = 'email3@example.com'

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 3)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)

    def test_equal_models_in_set_multiple_keys(self):
        """Test that equal models work properly with sets."""
        user1 = ExampleModel2()
        user1.id = 1
        user1.email = 'email1@example.com'
        user2 = ExampleModel2()
        user2.id = 1
        user2.email = 'email1@example.com'
        user3 = ExampleModel2()
        user3.id = 1
        user3.email = 'email1@example.com'

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 1)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)

    def test_non_equal_models_in_set_without_unique_key(self):
        """Test that non-equal models work properly with sets."""
        user1 = ExampleModel3()
        user1.id = 1
        user2 = ExampleModel3()
        user2.id = 2
        user3 = ExampleModel3()
        user3.id = 3

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 3)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)

    def test_equal_models_in_set_without_unique_key(self):
        """Test that equal models work properly with sets."""
        user1 = ExampleModel3()
        user1.id = 1
        user2 = user1
        user3 = user1

        users_set = set((user1, user2, user3))

        self.assertEquals(len(users_set), 1)
        self.assertIn(user1, users_set)
        self.assertIn(user2, users_set)
        self.assertIn(user3, users_set)
