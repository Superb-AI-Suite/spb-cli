import abc
import json
from uuid import UUID

from copy import deepcopy

from spb.exceptions import ImmutableValueChangeException, AttributeTypeException, ModelInitiationFailedException
from spb.orm.utils import is_json


class AttributeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, AttributeModel):
            return o.__dict__
        else:
            return o

class AttributeModel():
    @classmethod
    def get_data(self, item):
        """Change PlainObject(&List) to dictionary
        """
        if isinstance(item, dict):
            result = {}
            for key, value in item.items():
                result[key] = self.get_data(value)
            return result
        elif isinstance(item, list):
            return [self.get_data(value) for value in item]
        elif isinstance(item, AttributeModel):
            return self.get_data(vars(item))
        else:
            return item


class AttributeContainer:
    def __init__(self, attrs: dict, attr_types:dict, kwargs:dict = None):
        if len(kwargs) > len(attrs):
            # check argumets numbers over
            raise ModelInitiationFailedException("Number of args exceeds number of parameters")

        self.attribute_values = deepcopy(self._attrs)
        for key, value in kwargs.items():
            if key in self._attr_property_names:
                key = self._attr_property_names[key]
            if key not in attr_types:
                continue
            self.attribute_values[key] = attr_types[key]._validation(value)

    @classmethod
    def res_to_model(cls, inputs):
        gql_attrs = cls.get_attr_names()
        transformed_attrs = {}
        for key, attr_name in gql_attrs.items():
            if key not in inputs:
                raise ModelInitiationFailedException('Response data is not matched requested resource')
            value = inputs[key]
            transformed_attrs[attr_name] = value
        result = cls(**transformed_attrs)
        return result
