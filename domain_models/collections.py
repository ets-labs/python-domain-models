"""Collections module."""

import six


class Collection(list):
    """Collection."""

    value_type = object
    """Type of values that collection could contain."""

    def __init__(self, iterable=None, type_check=True):
        """Initializer."""
        if not iterable:
            iterable = tuple()

        if type_check:
            iterable = self._ensure_iterable_is_valid(iterable)

        super(Collection, self).__init__(iterable)

    def append(self, value):
        """Add an item to the end of the list."""
        return super(Collection, self).append(
            self._ensure_value_is_valid(value))

    def extend(self, iterable):
        """Extend the list by appending all the items in the given list."""
        return super(Collection, self).extend(
            self._ensure_iterable_is_valid(iterable))

    def insert(self, index, value):
        """Insert an item at a given position."""
        return super(Collection, self).insert(
            index, self._ensure_value_is_valid(value))

    def __setitem__(self, index, value):
        """Set an item at a given position."""
        if isinstance(index, slice):
            return super(Collection, self).__setitem__(index,
                                                       self.__class__(value))
        else:
            return super(Collection, self).__setitem__(
                index, self._ensure_value_is_valid(value))

    def __getitem__(self, index):
        """Return value by index or slice of values if index is slice."""
        value = super(Collection, self).__getitem__(index)
        if isinstance(index, slice):
            return self.__class__(value, type_check=False)
        return value

    if six.PY2:  # pragma: nocover
        def __getslice__(self, start, stop):
            """Return slice of values."""
            return self.__class__(super(Collection, self).__getslice__(start,
                                                                       stop),
                                  type_check=False)

        def __setslice__(self, start, stop, iterable):
            """Set slice of values."""
            super(Collection, self).__setslice__(start, stop,
                                                 self.__class__(iterable))

    def _ensure_iterable_is_valid(self, iterable):
        """Ensure that iterable values are a valid collection's values."""
        for value in iterable:
            self._ensure_value_is_valid(value)
        return iterable

    def _ensure_value_is_valid(self, value):
        """Ensure that value is a valid collection's value."""
        if not isinstance(value, self.__class__.value_type):
            raise TypeError('{0} is not valid collection value, instance '
                            'of {1} required'.format(
                                value, self.__class__.value_type))
        return value
