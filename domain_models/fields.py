"""Domain models fields."""

import six


class Field(property):
    """Base field."""

    def __init__(self):
        """Initializer."""
        self.name = None
        self.value = None
        self.model = None
        super(Field, self).__init__(self._get, self._set)

    def _get(self, _):
        """Return field's value."""
        return self.value

    def _set(self, _, value):
        """Set field's value."""
        self.value = value


class Int(Field):
    """Int field."""

    def _set(self, _, value):
        """Set field's value."""
        self.value = int(value)


class String(Field):
    """String field."""

    def _set(self, _, value):
        """Set field's value."""
        self.value = str(value)


class Unicode(Field):
    """Unicode string field."""

    def _set(self, _, value):
        """Set field's value."""
        self.value = six.u(value)
