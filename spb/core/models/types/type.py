import abc
import json
from typing import Dict
from uuid import UUID, UUID

from spb.exceptions import ImmutableValueChangeException, AttributeTypeException
from spb.core.models.attrs import AttributeModel

from .type_base import Type


class JsonObject(Type):
    GRAPHQL_TYPE = 'JSONObject'
    """
    This defines Json Object to Suite SDK
    You can use dictionary(without instacne key & value) to Model
    """
    def _validation(self, value):
        """Validation json object to use SDK
        1. instance check : Value dictionary cannot consist of instances. value only

        :param dict value: Dictionary value to use SDK
        :returns: Value when validation check success
        """
        try:
            if isinstance(value, str):
                value = json.loads(value)
            elif isinstance(value, dict):
                json.dumps(value)
        except Exception as e:
            raise AttributeTypeException(f'Invalid JsonObject type for {self.attr_name}: value is of {str(type(value))} type')
        return value


class JsonList(Type):
    GRAPHQL_TYPE='JSON'

    def _validation(self, value):
        try:
            if isinstance(value, str):
                value = json.loads(value)
            if isinstance(value, list):
                value = [json.loads(item) if isinstance(item, str) else item for item in value]
        except Exception as e:
            raise AttributeTypeException(f'Invalid Json type for {self.attr_name}: value is of {str(type(value))} type')
        return value


@abc.abstractmethod
class Number(Type):
    """
    Top level class to define all number types in SDK
    """
    def _validation(self, value):
        return value


class Int(Number):
    GRAPHQL_TYPE = 'Int'

    def _validation(self, value):
        """Define Integer attribute

        :param int value:
        :returns: "attribute_name:value"
        """
        if value is None or (isinstance(value, int) and type(value) is not bool):
            return value
        else:
            raise AttributeTypeException(f"Invalid Integer type for {self.attr_name}: {str(value)} is of {str(type(value))} type")


class Float(Number):
    GRAPHQL_TYPE = 'Float'

    def _validation(self, value):
        """Define Float attribute

        :param float value:
        :returns: "attribute_name:value"
        """
        if value is None or ((isinstance(value, float) or isinstance(value, int)) and type(value) is not bool):
            return value
        else:
            raise AttributeTypeException(f"Invalid Float type for {self.attr_name}: {str(value)} is of {str(type(value))} type")



class ID(Type):
    GRAPHQL_TYPE = 'String'

    def _validation(self, value):
        """Define ID attribute to use in SDK
        * You can use only uuid version 4

        :param uuid/string value: UUID instance or uuid string to use in SDK
        :returns: UUID instance
        """
        if isinstance(value, str):
            try:
                value = UUID(value, version=4)
            except ValueError:
                raise AttributeTypeException(f"Invalid ID type for {self.attr_name}: {str(value)} is of {str(type(value))} type. UUID4 is needed")
        elif not isinstance(value, UUID):
            raise AttributeTypeException(f"Invalid ID type for {self.attr_name}: {str(value)} is of {str(type(value))} type. UUID4 is needed")
        elif isinstance(value, UUID) and value.version != 4:
            raise AttributeTypeException(f"Invalid ID type for {self.attr_name}: {str(value)} is of {str(type(value))} type. UUID4 is needed")

        return value

    def to_query(self, value):
        """Define graphql query and return it

        :param uuid/string value: UUID instance or uuid string to use in SDK
        :returns: 'attribute_name:"uuid_string"'
        """
        self._validation(value)
        return f'{self.attr}:${self.attr}', {f'{self.attr}': str(value)}


class String(Type):
    GRAPHQL_TYPE = 'String'

    """This class defines String attribute type to SDK
    """
    def _validation(self, value):
        """Validation string value whether can use or not
        value must be string or None

        :param string value: The value to use in model
        :returns: value when validation check success
        """
        if not value or (isinstance(value, str) and type(value) is not bool):
            return value
        else:
            raise AttributeTypeException(f"Invalid String type for {self.attr_name}: {str(value)} is of {str(type(value))} type")


class Boolean(Type):
    GRAPHQL_TYPE = 'Boolean'

    """This class defines Boolean attribute type to SDK
    """
    def _validation(self, value):
        """Validation boolean value whether can use or not
        value must be boolean or None

        :param boolean value: The value to use in model
        :returns: value when validation check success
        """
        if value is None:
            return None
        elif not type(value) == bool:
            raise AttributeTypeException(f"Invalid Boolean type for {self.attr_name}: {str(value)} is of {str(type(value))} type")

        return value

    def to_query(self, value):
        """Translate boolean to graphql query with attribute name

        :param boolean value: The value to translate
        :returns: 'attribute_name:|true or false|'
        """
        self._validation(value)
        if value is None:
            #TODO [MinjuneL] boolean의 None 상태에 대해서 return false를 할지, null을 할지 고민이 필요함.
            return f'{self.attr}:${self.attr}', {f'{self.attr}': None}
        else:
            return f'{self.attr}:${self.attr}', {f'{self.attr}': value}


class List(Type):
    GRAPHQL_TYPE = 'List'

    def _validation(self, value):
        """Translate list to graphql query with attribute name
        element in list can consist of serializable values

        :param list value: The value to translate
        :returns: 'attribute_name:["value1"]'
        """
        if value is not None and not type(value) == list:
            raise AttributeTypeException(f"Invalid List type for {self.attr_name}: {str(value)} is of {str(type(value))} type")
        return value


class PlainObject(Type):
    GRAPHQL_TYPE = 'JSONObject'

    """JSON serializable plain object type
    PlainObject must set express param
    &
    Object has to be implemented AttributeModel class
    """
    def _validation(self, value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
                # TODO: refactoring serialize
                if isinstance(value, dict):
                    value = self.express(**value)
            except Exception as e:
                raise AttributeTypeException('')
        elif isinstance(value, dict):
            value = self.express(**value)
        if value is None:
            return value
        elif not isinstance(value, AttributeModel):
            raise AttributeTypeException(f'Invalid PlainObject type for {self.attr_name}: {str(type(value))} is unimplemented AttributeModel')
        elif not isinstance(value, self._express):
            raise AttributeTypeException(f'Invalid PlainObject type for {self.attr_name}: {str(type(value))} is not unmatched with {str(type(self._express))}')
        return value


class PlainObjectList(Type):
    GRAPHQL_TYPE = 'JSON'
    """JSON Serializable plain object list type
    PlainObjectList have to be list of instances of AttributeModel
    """
    def _validation(self, value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except Exception as e:
                raise AttributeTypeException('')
        if value is None:
            return None
        elif not isinstance(value, list):
            raise AttributeTypeException(f'Invalid PlainObjectList type for {self.attr_name}: {str(type(value))} is not a list')
        result = []
        for idx, item in enumerate(value):
            # TODO: refactoring serialize
            if isinstance(item, AttributeModel):
                result.append(item)
            elif isinstance(item, dict):
                item = self.express(**item)
                result.append(item)
            if not isinstance(item, AttributeModel):
                raise AttributeTypeException(f'Invalid PlainObjectList type for {self.attr_name}: {str(type(value))}-{idx} is unimplemented AttributeModel')
            elif not isinstance(item, self._express):
                raise AttributeTypeException(f'Invalid PlainObjectList type for {self.attr_name}: {str(type(value))}-{idx} is not unmatched with {str(type(self._express))}')
        return result
