"""Domain models model."""

import six

from . import fields


class DomainModelMetaClass(type):
    """Domain model meta class."""

    def __new__(mcs, class_name, bases, attributes):
        """Domain model class factory."""
        cls = type.__new__(mcs, class_name, bases, attributes)

        for field_name, field in six.iteritems(attributes):
            if not isinstance(field, fields.Field):
                continue
            field.name = field_name
            field.model = cls

        return cls


@six.add_metaclass(DomainModelMetaClass)
class DomainModel(object):
    """Base domain model."""

    __view_key__ = tuple()
    __unique_key__ = tuple()

    def __eq__(self, compared):
        """Make equality comparation based on unique key.

        If unique key is not defined, standard object's equality comparation
        will be used.
        """
