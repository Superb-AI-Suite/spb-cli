import abc
import json
from uuid import UUID
from spb.exceptions import ImmutableValueChangeException, AttributeTypeException
from .model import ListAttribute, AttributeModel
from .type_base import Type

class Number(Type):
    def _validation(self, value):
        if self._immutable:
            raise ImmutableValueChangeException(f"'{self.attr_name}' cannot be changed")

        if value is not None and not str(value).isdigit():
            raise AttributeTypeException(f"'{self.attr_name}' need number type value")

        return str(value)

    @classmethod
    def _type_to_query(cls, name, value):
        query = {}
        query[name] = value
        return query


class ID(Type):
    type_name = 'ID'

    def _validation(self, value):
        if self._immutable:
            raise ImmutableValueChangeException(f"'{self.attr_name}' cannot be changed")
        try:
            if value is not None:
                uuid_result = UUID(value, version=4)
                if value != uuid_result:
                    raise ValueError
        except ValueError:
            raise AttributeTypeException(f"'ID' can be UUID4 string")

        return str(value)

    @classmethod
    def _type_to_query(cls, name, value):
        query = {}
        query[name] = f'"{value}"'
        return query


class String(Type):
    type_name = 'String'
    def _validation(self, value):
        if self._immutable:
            raise ImmutableValueChangeException(f"'{self.attr_name}' cannot be changed")
        if value is not None and not isinstance(value, str):
            raise AttributeTypeException(f"'{self.attr_name}' need string type value")

        return str(value)

    @classmethod
    def _type_to_query(cls, name, value):
        query = {}
        query[name] = f'"{value}"'
        return query


class Boolean(Type):
    type_name ='Boolean'

    def _validation(self, value):
        if self._immutable:
            raise ImmutableValueChangeException(f"'{self.attr_name}' cannot be changed")

        if value is not None and not type(value) == bool:
            raise AttributeTypeException(f"'{self.attr_name}' need boolean type value")

        return str(value)

    @classmethod
    def _type_to_query(cls, name, value):
        query = {}
        query[name] = value
        return query

class List(Type):
    type_name = 'List'
    def _validation(self, value):
        if self._immutable:
            raise ImmutableValueChangeException(f"'{self.attr_name}' cannot be changed")
        if value is not None and not type(value) == list:
            raise AttributeTypeException(f"'{self.attr_name}' need list type value")
        return value
    @classmethod
    def _type_to_query(cls, name, value):
        query= {}
        query[name] = value.replace("'", '"')
        return query

class Object(Type):
    type_name = 'Object'
    def _validation(self, value):
        if self._immutable:
            raise ImmutableValueChangeException(f"'{self.attr_name}' cannot be changed")

        if value is None:
            return None
        else:
            if issubclass(self._express, ListAttribute):
                if not isinstance(value, list):
                    raise AttributeTypeException(f"'{self.attr_name}' need list type value")
                for item in value:
                    if not isinstance(item, self._express):
                        raise AttributeTypeException(f"'{self.attr_name}' need empty list or adjust type value")
                return value
            elif issubclass(self._express, AttributeModel):
                if not isinstance(value, self._express):
                    raise AttributeTypeException(f"'{self.attr_name}' need None or adjust type value")
                return value

    @classmethod
    def _type_to_query(cls, name, value):
        query = {}
        if isinstance(value, list):
            result = [item.get_datas(item) if "get_datas" in dir(item) else None for item in value]
        else:
            result = value.get_datas(value) if "get_datas" in dir(value) else None
        json_result = json.dumps(result)
        json_result = json_result.replace("\"","\\\"")
        query[name] = f'"{json_result}"'
        return query

