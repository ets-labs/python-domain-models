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


class SampleTests(unittest.TestCase):
    """Sample tests tests."""

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
