"""Contextual view module."""

from . import models
import six


class ContextViewMetaClass(type):
    """Context view meta class."""

    def __new__(mcs, class_name, bases, attributes):
        """Context view class factory."""
        mcs.validate(bases, attributes)
        cls = type.__new__(mcs, class_name, bases, attributes)
        cls.__fields__ = mcs.get_properties(attributes)
        return cls

    @classmethod
    def validate(mcs, bases, attributes):
        """Check attributes."""
        if bases[0] is object:
            return None

        mcs.check_model_cls(attributes)
        mcs.check_include_exclude(attributes)
        mcs.check_properties(attributes)
        mcs.match_unknown_attrs(attributes)

    @staticmethod
    def check_model_cls(attributes):
        """Check __model_cls__ attribute.

        :type attributes: dict
        """
        model_cls = attributes.get('__model_cls__')
        if model_cls is None:
            raise AttributeError("Attribute __model_cls__ is required.")

        if not issubclass(model_cls, models.DomainModel):
            raise TypeError("Attribute __model_cls__ must be subclass of "
                            "DomainModel.")

    @staticmethod
    def get_prepared_include_exclude(attributes):
        """Return tuple with prepared __include__ and __exclude__ attributes.

        :type attributes: dict
        :rtype: tuple
        """
        attrs = dict()
        for attr in ('__include__', '__exclude__'):
            attrs[attr] = tuple([item.name for item in
                                 attributes.get(attr, tuple())])
        return attrs['__include__'], attrs['__exclude__']

    @staticmethod
    def check_include_exclude(attributes):
        """Check __include__ and __exclude__ attributes.

        :type attributes: dict
        """
        include = attributes.get('__include__', tuple())
        exclude = attributes.get('__exclude__', tuple())

        if not isinstance(include, tuple):
            raise TypeError("Attribute __include__ must be a tuple.")

        if not isinstance(exclude, tuple):
            raise TypeError("Attribute __exclude__ must be a tuple.")

        if all((not include, not exclude)):
            return None

        if all((include, exclude)):
            raise AttributeError("Usage of __include__ and __exclude__ "
                                 "at the same time is prohibited.")

    @staticmethod
    def get_properties(attributes):
        """Return tuple of names of defined properties.

        :type attributes: dict
        :rtype: list
        """
        return [key for key, value in six.iteritems(attributes)
                if isinstance(value, property)]

    @classmethod
    def check_properties(mcs, attributes):
        """Check whether intersections exist.

        :type attributes: dict
        """
        include, exclude = mcs.get_prepared_include_exclude(attributes)

        if include:
            intersections = mcs.get_intersections(attributes, include)
            attr = '__include__'
        elif exclude:
            intersections = mcs.get_intersections(attributes, exclude)
            attr = '__exclude__'
        else:
            return None

        if not intersections:
            return None

        raise AttributeError(
            "It is not allowed to mention already defined properties: "
            "{0} in {1} attributes.".format(", ".join(intersections), attr))

    @classmethod
    def get_intersections(mcs, attributes, attr):
        """Return intersection with defined properties if exists.

        :type attributes: dict
        :type attr: list
        :rtype: list
        """
        if not attr:
            return []
        properties = mcs.get_properties(attributes)
        return list(set(properties).intersection(attr))

    @classmethod
    def match_unknown_attrs(mcs, attributes):
        """Check about using nonexistent attributes.

        :type attributes: dict
        """
        model_cls = attributes.get('__model_cls__')
        include, exclude = mcs.get_prepared_include_exclude(attributes)
        attrs = include if include else exclude
        unknown_attr = list()

        for attr in attrs:
            if not hasattr(model_cls, attr):
                unknown_attr.append(attr)

        if not unknown_attr:
            return None

        raise AttributeError(
            "Nonexistent attributes: {0}.".format(", ".join(unknown_attr)))


@six.add_metaclass(ContextViewMetaClass)
class ContextView(object):
    """Contextual view class."""

    __model_cls__ = None
    __include__ = tuple()
    __exclude__ = tuple()
    __fields__ = list()

    def __init__(self, model):
        """Model validation.

        :type model: DomainModel
        """
        if not isinstance(model, self.__model_cls__):
            raise TypeError("\"{0}\" is not an instance of {1}".format(
                model, self.__model_cls__))

        self._model = model

        if self.__include__:
            self._include()
        elif self.__exclude__:
            self._exclude()
        else:
            self._fields()

    def _include(self):
        """Fill __fields__ out based on __include__."""
        for field in self.__include__:
            value = getattr(self._model, field.name)
            setattr(self, field.name, value)
            self.__fields__.append(field.name)

    def _exclude(self):
        """Fill __fields__ out based on __exclude__."""
        exclude = [field.name for field in self.__exclude__]
        for (field, value) in six.iteritems(self._model.get_data()):
            if field in exclude:
                continue
            setattr(self, field, value)
            self.__fields__.append(field)

    def _fields(self):
        """Fill __fields__ out based on full model data."""
        for (field, value) in six.iteritems(self._model.get_data()):
            if field in self.__fields__:
                continue
            setattr(self, field, value)
            self.__fields__.append(field)

    def get_data(self):
        """Read only dictionary fields/values of model within current context.

        :rtype: dict
        """
        return dict((field, getattr(self, field)) for field in self.__fields__)
