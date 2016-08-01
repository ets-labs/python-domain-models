"""Contextual view module."""
from domain_models import models
import six


class ContextViewMetaClass(type):
    """Context view meta class."""

    def __new__(mcs, class_name, bases, attributes):
        """Context view class factory."""
        if bases[0] is not object:
            __model_cls__ = attributes.get('__model_cls__')
            if __model_cls__ is None:
                raise AttributeError("Attribute __model_cls__ is required.")
            if not issubclass(__model_cls__, models.DomainModel):
                raise TypeError("Attribute __model_cls__ must be subclass of "
                                "DomainModel.")

        return type.__new__(mcs, class_name, bases, attributes)


@six.add_metaclass(ContextViewMetaClass)
class ContextView(object):
    """Contextual view class."""

    __model_cls__ = None

    def __init__(self, model):
        """Model validation.

        :param model: DomainModel
        """
        if not isinstance(model, self.__model_cls__):
            raise TypeError("\"{0}\" is not an instance of {1}".format(
                model, self.__model_cls__))

        self.__model__ = model

    def get_data(self):
        """Read only dictionary fields/values of model within current context.

        :rtype: dict
        """
        raise NotImplementedError("Method get_data is required.")
