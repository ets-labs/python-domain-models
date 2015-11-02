"""Sample unittests."""

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
        user = User()
        user.id = 1
        user.email = 'example@example.com'
        user.first_name = 'John'
        user.last_name = 'Smith'
        user.gender = 'male'
        user.birth_date = '05/04/1988'

        self.assertEqual(user.id, 1)
        self.assertEqual(user.email, 'example@example.com')
        self.assertEqual(user.first_name, unicode('John'))
        self.assertEqual(user.last_name, unicode('Smith'))
        self.assertEqual(user.gender, 'male')
        self.assertEqual(user.birth_date, '05/04/1988')
