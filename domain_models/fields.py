"""Domain models fields."""

import six

from . import errors


class Field(property):
    """Base field."""

    def __init__(self, default=None):
        """Initializer."""
        super(Field, self).__init__(self.get_value, self.set_value)
        self.name = None
        self.storage_name = None

        self.model_cls = None

        self.default = default

    def bind_name(self, name):
        """Bind field to its name in model class."""
        if self.name:
            raise errors.Error('Already bound "{0}" with name "{1}" could not '
                               'be rebound'.format(self, self.name))
        self.name = name
        self.storage_name = ''.join(('_', self.name))
        return self

    def bind_model_cls(self, model_cls):
        """Bind field to model class."""
        if self.model_cls:
            raise errors.Error('"{0}" has been already bound to "{1}" and '
                               'could not be rebound to "{2}"'.format(
                                   self, self.model_cls, model_cls))
        self.model_cls = model_cls
        return self

    def init_model(self, model, value):
        """Init model with field."""
        if not value:
            value = self.default() if callable(self.default) else self.default
        setattr(model, self.storage_name, value)

    def get_value(self, model):
        """Return field's value."""
        return getattr(model, self.storage_name)

    def set_value(self, model, value):
        """Set field's value."""
        setattr(model, self.storage_name, value)


class Int(Field):
    """Int field."""

    def set_value(self, model, value):
        """Set field's value."""
        setattr(model, self.storage_name, int(value))


class String(Field):
    """String field."""

    def set_value(self, model, value):
        """Set field's value."""
        setattr(model, self.storage_name, str(value))


class Unicode(Field):
    """Unicode string field."""

    def set_value(self, model, value):
        """Set field's value."""
        setattr(model, self.storage_name, six.u(value))
