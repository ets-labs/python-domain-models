"""Collections tests."""

import unittest2

from domain_models import collections
from domain_models import errors


class CollectionTests(unittest2.TestCase):
    """Collection tests."""

    def test_init_empty(self):
        """Test creation of collection."""
        collection = collections.Collection(int)

        self.assertIsInstance(collection, collections.Collection)
        self.assertIsInstance(collection, list)

    def test_init_with_correct_values(self):
        """Test creation of collection."""
        collection = collections.Collection(int, (1, 2, 3))

        self.assertEqual(collection, [1, 2, 3])

    def test_init_with_incorrect_values(self):
        """Test creation of collection."""
        with self.assertRaises(TypeError):
            collections.Collection(int, ('1', '2', '3'))

    def test_init_without_value_type(self):
        """Test creation of collection."""
        with self.assertRaises(errors.Error):
            collections.Collection(None)

        with self.assertRaises(errors.Error):
            collections.Collection(1)

        with self.assertRaises(errors.Error):
            collections.Collection(object())

    def test_append_valid_type(self):
        """Test append."""
        collection = collections.Collection(int)

        collection.append(1)

        self.assertEqual(collection, [1])

    def test_append_invalid_type(self):
        """Test append."""
        collection = collections.Collection(int)

        with self.assertRaises(TypeError):
            collection.append('1')

    def test_extend_valid_type(self):
        """Test extend."""
        collection = collections.Collection(int)

        collection.extend([1])

        self.assertEqual(collection, [1])

    def test_extend_invalid_type(self):
        """Test extend."""
        collection = collections.Collection(int)

        with self.assertRaises(TypeError):
            collection.extend(['1'])

    def test_insert_valid_type(self):
        """Test insert."""
        collection = collections.Collection(int)

        collection.insert(0, 1)

        self.assertEqual(collection, [1])

    def test_insert_invalid_type(self):
        """Test insert."""
        collection = collections.Collection(int)

        with self.assertRaises(TypeError):
            collection.insert(0, '1')

    def test_set_valid_type(self):
        """Test set."""
        collection = collections.Collection(int, [0])

        collection[0] = 1

        self.assertEqual(collection, [1])

    def test_set_invalid_type(self):
        """Test set."""
        collection = collections.Collection(int, [0])

        with self.assertRaises(TypeError):
            collection[0] = '1'

    def test_set_valid_slice(self):
        """Test set slice."""
        collection = collections.Collection(int, [1, 2, 3])

        collection[0:3] = [7, 7, 7]

        self.assertEqual(collection, [7, 7, 7])

    def test_set_invalid_slice(self):
        """Test set slice."""
        collection = collections.Collection(int, [1, 2, 3])

        with self.assertRaises(TypeError):
            collection[0:3] = [7, '7', 7]

        self.assertEqual(collection, [1, 2, 3])

    def test_set_valid_slice_setitem(self):
        """Test set slice."""
        collection = collections.Collection(int, [1, 2, 3])

        collection.__setitem__(slice(0, 3), [7, 7, 7])

        self.assertEqual(collection, [7, 7, 7])

    def test_set_invalid_slice_setitem(self):
        """Test set slice."""
        collection = collections.Collection(int, [1, 2, 3])

        with self.assertRaises(TypeError):
            collection.__setitem__(slice(0, 3), [7, '7', 7])

        self.assertEqual(collection, [1, 2, 3])

    def test_get_item(self):
        """Test getting of item."""
        collection = collections.Collection(int, [1, 2, 3])

        self.assertEqual(collection[0], 1)
        self.assertEqual(collection[1], 2)
        self.assertEqual(collection[2], 3)

    def test_get_slice(self):
        """Test getting of slice."""
        collection = collections.Collection(int, [1, 2, 3])

        collection_slice = collection[0:2]

        self.assertEqual(collection_slice, [1, 2])
        self.assertIsInstance(collection_slice, collections.Collection)
        self.assertIs(collection.value_type, collection_slice.value_type)

    def test_getitem_slice(self):
        """Test getting of slice."""
        collection = collections.Collection(int, [1, 2, 3])

        collection_slice = collection.__getitem__(slice(0, 2))

        self.assertEqual(collection_slice, [1, 2])
        self.assertIsInstance(collection_slice, collections.Collection)
        self.assertIs(collection.value_type, collection_slice.value_type)
