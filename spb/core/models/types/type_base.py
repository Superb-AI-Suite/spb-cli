import abc

from spb.core.models.attrs import AttributeModel
from spb.exceptions import ImmutableValueChangeException, TypeInitiationFailedException, NotImplementedException


class Type(object):
    type_name = None

    def __init__(self, *args, **kwargs):
        self._express = kwargs['express'] if 'express' in kwargs else None
        self._default = kwargs['default'] if 'default' in kwargs else None
        if not 'property_name' in kwargs:
            raise TypeInitiationFailedException('Type must have "property_name" param')
        else:
            self.attr = kwargs['property_name']

    @property
    def default_value(self):
        return self._default

    @property
    def attr_name(self):
        return self.attr

    @attr_name.setter
    def attr_name(self, value):
        self.attr = value

    @property
    def express(self):
        return self._express

    @express.setter
    def express(self, value):
        self._express = value

    @abc.abstractmethod
    def _validation(self, value):
        ''' Verify value attribute according to user defined code '''
        raise NotImplementedException('_validation method must be implemented')

    def validation(self, value):
        return self._validation(value)

    @classmethod
    def get_attr_name(cls):
        return cls.attr_name

    def to_query(self, value):
        self._validation(value)
        return f'{self.attr}:${self.attr}', {f'{self.attr}': value}