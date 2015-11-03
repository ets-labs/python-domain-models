"""Domain models fields."""

import six


class Field(property):
    """Base field."""

    def __init__(self, default=None):
        """Initializer."""
        self.model_cls = None
        self.name = None
        self.storage_name = None
        self.default = default
        super(Field, self).__init__(self.get_value, self.set_value)

    def bind(self, model_cls, name):
        """Post initializer."""
        self.model_cls = model_cls
        self.name = name
        self.storage_name = ''.join(('_', self.name))
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
