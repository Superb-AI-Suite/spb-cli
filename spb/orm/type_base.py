import abc
import json
from spb.exceptions import ImmutableValueChangeException, AttributeTypeException

class Type(object):
    type_name = None

    def __init__(self, *args, **kwargs):
        self._filterable = False
        self._immutable = False
        self._express = None

        # self.attr = kwargs['property_name'] if 'property_name' in kwargs else None
        self.attr = kwargs['property_name']

        if kwargs is not None and 'immutable' in kwargs:
            self._immutable = kwargs['immutable']
        if kwargs is not None and 'filterable' in kwargs:
            self._filterable = kwargs['filterable']

        if kwargs is not None and 'express' in kwargs:
            self._express = kwargs['express']

    @property
    def attr_name(self):
        return self.attr

    @attr_name.setter
    def attr_name(self, value):
        self.attr = value

    @property
    def filterable(self):
        return self._filterable

    @filterable.setter
    def filterable(self, value):
        self._filterable = value

    @property
    def immutable(self):
        return self._immutable

    @immutable.setter
    def immutable(self, value):
        self._immutable = value

    @property
    def express(self):
        return self._express

    @express.setter
    def express(self, value):
        self._express = value

    @abc.abstractmethod
    def _validation(self, value):
        ''' Verify value attribute according to user defined code '''
        if self._immutable:
            raise ImmutableValueChangeException(
                'This is immutable value. Check the model attribute type')
        return value

    @abc.abstractmethod
    def _serialize(self, value):
        return value

    def __set__(self, instance, value):
        attribute_name = instance._graphql_attrs[self.attr]
        if self._express is not None and isinstance(value, dict):
            value = self._express(value)

        value = self._validation(value)
        instance.attribute_values[attribute_name] = value


    def __get__(self, instance, objtype):
        attribute_name = instance._graphql_attrs[self.attr]
        value = instance.attribute_values[attribute_name]
        value = self._serialize(value)
        return value

    def __repr__(self):
        return str(self.type_name)

    @classmethod
    def get_attr_name(cls):
        return cls.attr_name

    def __eq__(self, you):
        if isinstance(you, Type):
            return str(self.value) == str(you.value)
        else:
            return str(self.value) == str(you)