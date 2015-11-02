"""Sample unittests."""

import unittest2 as unittest
import domain_models as dm


class SampleTests(unittest.TestCase):
    """Sample tests tests."""

    def test_version(self):
        """Test package version."""
        self.assertIsNotNone(dm.VERSION)
