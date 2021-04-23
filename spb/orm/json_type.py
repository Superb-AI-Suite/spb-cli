import abc
import json
from spb.exceptions import ImmutableValueChangeException, AttributeTypeException
from .type_base import Type


class JsonObject(Type):
    type_name = 'JsonObject'
    def _validation(self, value):
        if self._immutable:
            raise ImmutableValueChangeException(f"'{self.attr_name}' cannot be changed")
        if value is not None and not type(value) == dict:
            raise AttributeTypeException(f"'{self.attr_name}' need dictionary type value")
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