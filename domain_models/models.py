"""Models module."""

from __future__ import absolute_import

import collections as std_collections
import six

from . import fields
from . import collections
from . import errors


class DomainModelMetaClass(type):
    """Domain model meta class."""

    def __new__(mcs, class_name, bases, attributes):
        """Domain model class factory."""
        model_fields = mcs.parse_fields(attributes)

        if attributes.get('__slots_optimization__', True):
            attributes['__slots__'] = mcs.prepare_model_slots(model_fields)

        cls = type.__new__(mcs, class_name, bases, attributes)

        cls.__fields__ = mcs.bind_fields_to_model_cls(cls, model_fields)
        cls.__unique_key__ = mcs.prepare_fields_attribute(
            attribute_name='__unique_key__', attributes=attributes,
            class_name=class_name)
        cls.__view_key__ = mcs.prepare_fields_attribute(
            attribute_name='__view_key__', attributes=attributes,
            class_name=class_name)

        mcs.bind_collection_to_model_cls(cls)

        return cls

    @staticmethod
    def parse_fields(attributes):
        """Parse model fields."""
        return tuple(field.bind_name(name)
                     for name, field in six.iteritems(attributes)
                     if isinstance(field, fields.Field))

    @staticmethod
    def prepare_model_slots(model_fields):
        """Return tuple of model field slots."""
        return tuple(field.storage_name for field in model_fields)

    @staticmethod
    def prepare_fields_attribute(attribute_name, attributes, class_name):
        """Prepare model fields attribute."""
        attribute = attributes.get(attribute_name)
        if not attribute:
            attribute = tuple()
        elif isinstance(attribute, std_collections.Iterable):
            attribute = tuple(attribute)
        else:
            raise errors.Error('{0}.{1} is supposed to be a list of {2}, '
                               'instead {3} given', class_name, attribute_name,
                               fields.Field, attribute)
        return attribute

    @staticmethod
    def bind_fields_to_model_cls(cls, model_fields):
        """Bind fields to model class."""
        return dict(
            (field.name, field.bind_model_cls(cls)) for field in model_fields)

    @staticmethod
    def bind_collection_to_model_cls(cls):
        """Bind collection to model's class.

        If collection was not specialized in process of model's declaration,
        subclass of collection will be created.
        """
        cls.Collection = type('{0}.Collection'.format(cls.__name__),
                              (cls.Collection,),
                              {'value_type': cls})
        cls.Collection.__module__ = cls.__module__


@six.python_2_unicode_compatible
@six.add_metaclass(DomainModelMetaClass)
class DomainModel(object):
    """Base domain model.

    .. py:attribute:: Collection

        Model's collection class.

        :type: collections.Collection

    .. py:attribute:: __fields__

        Dictionary of all model fields.

        :type: dict[str, fields.Field]

    .. py:attribute:: __unique_key__

        Tuple of model fields that represents unique key.

        :type: tuple[fields.Field]

    .. py:attribute:: __view_key__

        Tuple of model fields that represents view key.

        :type: tuple[fields.Field]
    """

    Collection = collections.Collection

    __fields__ = dict()
    __view_key__ = tuple()
    __unique_key__ = tuple()
    __slots_optimization__ = True

    def __init__(self, **kwargs):
        """Initializer."""
        for name, field in six.iteritems(self.__class__.__fields__):
            field.init_model(self, kwargs.get(name))
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

    def __repr__(self):
        """Return Pythonic representation of domain model."""
        return '{module}.{cls}({fields_values})'.format(
            module=self.__class__.__module__, cls=self.__class__.__name__,
            fields_values=', '.join(
                '='.join((name, repr(field.get_value(self))))
                for name, field in
                six.iteritems(self.__class__.__fields__)))

    def __str__(self):
        """Return string representation of domain model."""
        if not self.__class__.__view_key__:
            return self.__repr__()

        return '{module}.{cls}({fields_values})'.format(
            module=self.__class__.__module__, cls=self.__class__.__name__,
            fields_values=', '.join('='.join((field.name,
                                              str(field.get_value(self))))
                                    for field in self.__class__.__view_key__))

    def get(self, field_name, default=None):
        """Return the value of the field.

        Analogue for `dict.get()` python method.
        `field_name` must be a string. If the string is the name of
        one of the existent fields, the result is the value of that field.
        For example, `model.get('foobar')` is equivalent to `model.foobar`.
        If the filed does not have a value, `default` is returned if provided.
        It will raise `TypeError` or `ValueError` if `default` can not be
        converted to right type value.
        If the field does not exist, `AttributeError` is raised as well.

        :param string field_name:
        :param object default:
        """
        try:
            field = self.__class__.__fields__[field_name]
        except KeyError:
            raise AttributeError(
                "Field {0} does not exist.".format(field_name))
        else:
            return field.get_value(self, default)

    def get_data(self):
        """Read only dictionary of model fields/values.

        :rtype dict:
        """
        return dict((name, field.get_builtin_type(self))
                    for name, field in
                    six.iteritems(self.__class__.__fields__))

    def set_data(self, data):
        """Set dictionary data to model.

        :param dict data:
        """
        for name, field in six.iteritems(self.__class__.__fields__):
            field.init_model(self, data.get(name))
