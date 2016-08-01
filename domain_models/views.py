"""Contextual view module."""
from domain_models import models


class ContextView(object):
    """Contextual view class."""

    __model_cls__ = None

    def __init__(self, model):
        """Model validation.

        :param model: DomainModel
        """
        if not issubclass(self.__model_cls__, models.DomainModel):
            raise TypeError("Attribute __model__ must be subclass of "
                            "DomainModel")

        if not isinstance(model, self.__model_cls__):
            raise TypeError("\"{0}\" is not an instance of {1}".format(
                model, self.__model_cls__))

        self.__model__ = model

    def get_data(self):
        """Read only dictionary fields/values of model within current context.

        :rtype: dict
        """
        raise NotImplementedError("Method get_data is required.")
