"""Contextual view module."""

from . import models
import six


class ContextViewMetaClass(type):
    """Context view meta class."""

    attributes = dict()

    def __new__(mcs, class_name, bases, attributes):
        """Context view class factory."""
        mcs.attributes = attributes
        mcs.validate(bases)
        cls = type.__new__(mcs, class_name, bases, attributes)
        cls.__fields__ = mcs.get_properties()
        return cls

    @classmethod
    def validate(mcs, bases):
        """Check attributes."""
        if bases[0] is object:
            return None
        mcs.check_model_cls()
        mcs.check_include_exclude()

    @classmethod
    def check_model_cls(mcs):
        """Check __model_cls__ attribute."""
        model_cls = mcs.attributes.get('__model_cls__')
        if model_cls is None:
            raise AttributeError("Attribute __model_cls__ is required.")

        if not issubclass(model_cls, models.DomainModel):
            raise TypeError("Attribute __model_cls__ must be subclass of "
                            "DomainModel.")

    @classmethod
    def check_include_exclude(mcs):
        """Check __include__ and __exclude__ attributes."""
        include = mcs.attributes.get('__include__', tuple())
        exclude = mcs.attributes.get('__exclude__', tuple())

        if not isinstance(include, tuple):
            raise TypeError("Attribute __include__ must be a tuple.")

        if not isinstance(exclude, tuple):
            raise TypeError("Attribute __exclude__ must be a tuple.")

        if all((not include, not exclude)):
            return None

        if all((include, exclude)):
            raise AttributeError("Usage of __include__ and __exclude__ "
                                 "at the same time is prohibited.")

        include_names = [item.name for item in include]
        exclude_names = [item.name for item in exclude]

        mcs.chk_intersections(include_names, exclude_names)
        mcs.match_unknown_attrs(include_names, exclude_names)

    @classmethod
    def chk_intersections(mcs, include, exclude):
        """Check whether intersections exist."""
        intersections = mcs.get_intersections(include)
        attr, intersections = ('__include__', intersections) \
            if intersections \
            else ('__exclude__', mcs.get_intersections(exclude))

        if intersections:
            raise AttributeError(
                "It is not allowed to mention already defined properties: "
                "{0} in {1} attributes.".format(", ".join(intersections),
                                                attr))

    @classmethod
    def get_intersections(mcs, attr):
        """Return intersection with defined properties if exists.

        :type attr: list
        :rtype: list
        """
        if not attr:
            return []
        return list(set(mcs.get_properties()).intersection(attr))

    @classmethod
    def match_unknown_attrs(mcs, include, exclude):
        """Check about using nonexistent attributes."""
        model_cls = mcs.attributes.get('__model_cls__')
        unknown_attr = []
        for item in include:
            if not hasattr(model_cls, item):
                unknown_attr.append(item)

        for item in exclude:
            if not hasattr(model_cls, item):
                unknown_attr.append(item)

        if unknown_attr:
            raise AttributeError(
                "Nonexistent attributes: {0}.".format(
                    ", ".join(unknown_attr)))

    @classmethod
    def get_properties(mcs):
        """Return list of names of defined properties.

        :rtype: list
        """
        return [key for key, value in six.iteritems(mcs.attributes)
                if isinstance(value, property)]


@six.add_metaclass(ContextViewMetaClass)
class ContextView(object):
    """Contextual view class."""

    __model_cls__ = None
    __model__ = None
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

        self.__model__ = model

        if self.__include__:
            self._include()
        elif self.__exclude__:
            self._exclude()
        else:
            self._fields()

    def _include(self):
        for field in self.__include__:
            value = getattr(self.__model__, field.name)
            setattr(self, field.name, value)
            self.__fields__.append(field.name)

    def _exclude(self):
        exclude = [field.name for field in self.__exclude__]
        for (field, value) in six.iteritems(self.__model__.get_data()):
            if field in exclude:
                continue
            setattr(self, field, value)
            self.__fields__.append(field)

    def _fields(self):
        for (field, value) in six.iteritems(self.__model__.get_data()):
            if field in self.__fields__:
                continue
            setattr(self, field, value)
            self.__fields__.append(field)

    def get_data(self):
        """Read only dictionary fields/values of model within current context.

        :rtype: dict
        """
        return dict((field, getattr(self, field)) for field in self.__fields__)
