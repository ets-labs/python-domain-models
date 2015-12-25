"""Collections tests."""

import unittest2

from domain_models import collections


class TestCollection(collections.Collection):
    """Test collection of ints."""

    value_type = int


class CollectionTests(unittest2.TestCase):
    """Collection tests."""

    def test_init_empty(self):
        """Test creation of collection."""
        collection = TestCollection()

        self.assertIsInstance(collection, collections.Collection)
        self.assertIsInstance(collection, list)

    def test_init_with_correct_values(self):
        """Test creation of collection."""
        collection = TestCollection((1, 2, 3))

        self.assertEqual(collection, [1, 2, 3])

    def test_init_with_incorrect_values(self):
        """Test creation of collection."""
        with self.assertRaises(TypeError):
            TestCollection(('1', '2', '3'))

    def test_append_valid_type(self):
        """Test append."""
        collection = TestCollection()

        collection.append(1)

        self.assertEqual(collection, [1])

    def test_append_invalid_type(self):
        """Test append."""
        collection = TestCollection()

        with self.assertRaises(TypeError):
            collection.append('1')

    def test_extend_valid_type(self):
        """Test extend."""
        collection = TestCollection()

        collection.extend([1])

        self.assertEqual(collection, [1])

    def test_extend_invalid_type(self):
        """Test extend."""
        collection = TestCollection()

        with self.assertRaises(TypeError):
            collection.extend(['1'])

    def test_insert_valid_type(self):
        """Test insert."""
        collection = TestCollection()

        collection.insert(0, 1)

        self.assertEqual(collection, [1])

    def test_insert_invalid_type(self):
        """Test insert."""
        collection = TestCollection()

        with self.assertRaises(TypeError):
            collection.insert(0, '1')

    def test_set_valid_type(self):
        """Test set."""
        collection = TestCollection([0])

        collection[0] = 1

        self.assertEqual(collection, [1])

    def test_set_invalid_type(self):
        """Test set."""
        collection = TestCollection([0])

        with self.assertRaises(TypeError):
            collection[0] = '1'

    def test_set_valid_slice(self):
        """Test set slice."""
        collection = TestCollection([1, 2, 3])

        collection[0:3] = [7, 7, 7]

        self.assertEqual(collection, [7, 7, 7])

    def test_set_invalid_slice(self):
        """Test set slice."""
        collection = TestCollection([1, 2, 3])

        with self.assertRaises(TypeError):
            collection[0:3] = [7, '7', 7]

        self.assertEqual(collection, [1, 2, 3])

    def test_set_valid_slice_setitem(self):
        """Test set slice."""
        collection = TestCollection([1, 2, 3])

        collection.__setitem__(slice(0, 3), [7, 7, 7])

        self.assertEqual(collection, [7, 7, 7])

    def test_set_invalid_slice_setitem(self):
        """Test set slice."""
        collection = TestCollection([1, 2, 3])

        with self.assertRaises(TypeError):
            collection.__setitem__(slice(0, 3), [7, '7', 7])

        self.assertEqual(collection, [1, 2, 3])

    def test_get_item(self):
        """Test getting of item."""
        collection = TestCollection([1, 2, 3])

        self.assertEqual(collection[0], 1)
        self.assertEqual(collection[1], 2)
        self.assertEqual(collection[2], 3)

    def test_get_slice(self):
        """Test getting of slice."""
        collection = TestCollection([1, 2, 3])

        collection_slice = collection[0:2]

        self.assertEqual(collection_slice, [1, 2])
        self.assertIsInstance(collection_slice, TestCollection)

    def test_getitem_slice(self):
        """Test getting of slice."""
        collection = TestCollection([1, 2, 3])

        collection_slice = collection.__getitem__(slice(0, 2))

        self.assertEqual(collection_slice, [1, 2])
        self.assertIsInstance(collection_slice, TestCollection)
