"""Domain models model."""

import collections
import six

from . import fields


class DomainModelMetaClass(type):
    """Domain model meta class."""

    def __new__(mcs, class_name, bases, attributes):
        """Domain model class factory."""
        attributes['__fields__'] = tuple(field.bind_name(name)
                                         for name, field in six.iteritems(
                                             attributes)
                                         if isinstance(field, fields.Field))

        if attributes.get('__slots_optimization__', True):
            attributes['__slots__'] = tuple(
                field.storage_name for field in attributes['__fields__'])

        unique_key = attributes.get('__unique_key__')
        if not unique_key:
            unique_key = tuple()
        elif isinstance(unique_key, collections.Iterable):
            unique_key = tuple(unique_key)
        elif isinstance(unique_key, fields.Field):
            unique_key = tuple([unique_key])
        attributes['__unique_key__'] = unique_key

        cls = type.__new__(mcs, class_name, bases, attributes)

        for field in cls.__fields__:
            field.bind_model_cls(cls)

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
    __slots_optimization__ = True

    def __init__(self, **kwargs):
        """Initializer."""
        for field in self.__class__.__fields__:
            field.init_model(self, kwargs.get(field.name))
        super(DomainModel, self).__init__()

    def __eq__(self, other):
        """Make equality comparation based on unique key.

        If unique key is not defined, standard object's equality comparation
        will be used.
        """
        if self is other:
            return True
        if not isinstance(other, self.__class__):
            return False
        if not self.__class__.__unique_key__:
            return NotImplemented
        for field in self.__class__.__unique_key__:
            if field.get_value(self) != field.get_value(other):
                return False
        return True

    def __ne__(self, other):
        """Make non-equality comparation based on unique key.

        If unique key is not defined, standard object's not equality
        comparation will be used.
        """
        if isinstance(other, self.__class__):
            return not self == other
        return NotImplemented

    def __hash__(self):
        """Calculate and return model hash based on unique key.

        If unique key is not defined, standard object's hash calculation will
        be used.
        """
        if self.__class__.__unique_key__:
            return hash(tuple(field.get_value(self)
                              for field in self.__class__.__unique_key__))
        return super(DomainModel, self).__hash__()

    @property
    def __data__(self):
        """Read only dictionary of model fields/values."""
        return dict((field.name, field.get_value(self))
                    for field in self.__class__.__fields__)
