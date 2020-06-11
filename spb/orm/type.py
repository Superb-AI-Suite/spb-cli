import abc
import json
from uuid import UUID
from spb.exceptions.exceptions import ImmutableValueChangeException, AttribureTypeException


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
        instance.attribute_values[attribute_name] = str(value)

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


class Number(Type):
    def _validation(self, value):
        if self._immutable:
            raise ImmutableValueChangeException(f"'{self.attr_name}' cannot be changed")

        if value is not None and not str(value).isdigit():
            raise AttribureTypeException(f"'{self.attr_name}' need number type value")

        return value

    @classmethod
    def _type_to_query(cls, name, value):
        query = {}
        query[name] = value
        return query


class ID(Type):
    def _validation(self, value):
        if self._immutable:
            raise ImmutableValueChangeException(f"'{self.attr_name}' cannot be changed")
        try:
            if value is not None:
                uuid_result = UUID(value, version=4)
                if value != uuid_result:
                    raise ValueError
        except ValueError:
            raise AttribureTypeException(f"'ID' can be UUID4 string")

        return value

    @classmethod
    def _type_to_query(cls, name, value):
        query = {}
        query[name] = f'"{value}"'
        return query


class String(Type):
    def _validation(self, value):
        if self._immutable:
            raise ImmutableValueChangeException(f"'{self.attr_name}' cannot be changed")
        if value is not None and not isinstance(value, str):
            raise AttribureTypeException(f"'{self.attr_name}' need string type value")

        return value

    @classmethod
    def _type_to_query(cls, name, value):
        query = {}
        query[name] = f'"{value}"'
        return query


class Boolean(Type):
    def _validation(self, value):
        if self._immutable:
            raise ImmutableValueChangeException(f"'{self.attr_name}' cannot be changed")

        if value is not None and not type(value) == bool:
            raise AttribureTypeException(f"'{self.attr_name}' need boolean type value")

        return value

    @classmethod
    def _type_to_query(cls, name, value):
        query = {}
        query[name] = value
        return query


class Object(Type):
    @classmethod
    def _type_to_query(cls, name, value):
        query = {}
        if isinstance(value, list):
            result = [item.get_datas(item) for item in value]
        else:
            result = value.get_datas(value)
        json_result = json.dumps(result)
        json_result = json_result.replace("\"","\\\"")
        query[name] = f'"{json_result}"'
        return query

class JsonObject(Type):
    def _validation(self, value):
        if self._immutable:
            raise ImmutableValueChangeException(f"'{self.attr_name}' cannot be changed")
        if value is not None and not type(value) == dict:
            raise AttribureTypeException(f"'{self.attr_name}' need dictionary type value")
        return value
    def _serialize(self, value):
        if value == 'None' or value is None:
            return None
        elif isinstance(value, dict):
            return value

        value = value.replace("'", '"')
        value = value.replace("None", "null")
        value = json.loads(str(value))
        return value
    @classmethod
    def _type_to_query(cls, name, value):
        query = {}
        if value == 'None' or value == None:
            query[name] = 'null'
            return query

        value = json.dumps(value)
        # value = value.replace("\"","\\\"")
        # value = value.replace("\"\"", "\"")
        value = value.replace('None', 'null')
        if value.find('\'') != -1:
            value = value.replace("\'", "\\\"")
            query[name] = f'{value}'
        else:
            value = value.replace("\"", "\\\"")
            query[name] = f'"{value}"'
        return query