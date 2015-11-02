"""Domain models model."""

import six

from . import fields


class DomainModelMetaClass(type):
    """Domain model meta class."""

    def __new__(mcs, class_name, bases, attributes):
        """Domain model class factory."""
        cls = type.__new__(mcs, class_name, bases, attributes)

        model_fields = list()

        for field_name, field in six.iteritems(attributes):
            if not isinstance(field, fields.Field):
                continue
            field.bind(model_cls=cls, name=field_name)
            model_fields.append(field)

        cls.__fields__ = tuple(model_fields)

        return cls


@six.add_metaclass(DomainModelMetaClass)
class DomainModel(object):
    """Base domain model.

    :type __fields__: tuple[fields.Field]
    :type __unique_key__: tuple[fields.Field]
    :type __unique_key__: tuple[fields.Field]
    """

    __fields__ = tuple()
    __view_key__ = tuple()
    __unique_key__ = tuple()

    def __init__(self, **kwargs):
        """Initializer."""
        for field in self.__fields__:
            field.init_model(self, kwargs.get(field.name))

    def __eq__(self, compared):
        """Make equality comparation based on unique key.

        If unique key is not defined, standard object's equality comparation
        will be used.
        """
