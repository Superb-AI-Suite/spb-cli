import copy
import json
from spb.orm.manager import Manager
from spb.orm.type_base import Type
from spb.orm.json_type import JsonObject
from spb.orm.utils import *
from spb.exceptions import ModelInitiationFailedException

class ModelMeta(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        super_new = super(ModelMeta, cls).__new__
        parents = [b for b in bases if isinstance(b, ModelMeta)]
        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super_new(cls, name, bases, attrs)

        module = attrs.pop('__module__')

        new_attrs = {'__module__': module}
        new_attrs.update(attrs)

        model_attrs = {}
        for obj_name, obj in attrs.items():
            if isinstance(obj, Type):
                model_attrs[obj_name] = obj

        attr_classes = {}
        for obj_name, obj in attrs.items():
            if isinstance(obj, Type):
                attr_classes[obj_name] = obj.__class__

        graphql_to_python_attr = {}
        for obj_name, obj in attrs.items():
            if isinstance(obj, Type):
                graphql_to_python_attr[obj.attr_name] = obj_name

        immutable_attr = []
        for obj_name, obj in attrs.items():
            if isinstance(obj, Type) and obj.immutable:
                immutable_attr.append(obj.attr_name)

        filterable_attr = []
        for obj_name, obj in attrs.items():
            if isinstance(obj, Type) and obj.filterable:
                filterable_attr.append(obj.attr_name)

        instance_attr = {}
        for obj_name, obj in attrs.items():
            if isinstance(obj, Type) and obj.express:
                instance_attr[obj_name] = obj.express
            elif isinstance(obj, Type) and isinstance(obj, JsonObject):
                instance_attr[obj_name] = dict

        new_attrs['_immutables'] = immutable_attr
        new_attrs['_filterables'] = filterable_attr
        new_attrs['_instances'] = instance_attr
        new_attrs['_attrs_classes'] = attr_classes

        # make class with attributes
        new_class = super_new(cls, name, bases, new_attrs, **kwargs)
        # insert _attrs to class for type validation
        new_class.add_to_class('_attrs', model_attrs)
        new_class.add_to_class('_graphql_attrs', graphql_to_python_attr)

        return new_class

    def add_to_class(cls, name, value):
        setattr(cls, name, value)


class AttributeContainer:
    def __init__(self, attrs, kwargs=None):
        if len(kwargs) > len(attrs):
            # check argumets numbers over
            raise ModelInitiationFailedException("Number of args exceeds number of parameters")

        self.attribute_values = {}
        for key in attrs:
            # TODO: set default values
            self.attribute_values[key] = None
        for key in kwargs.keys():
            if key in self._instances:
                if is_json(kwargs[key]):
                    kwargs[key] = json.loads(kwargs[key])
                if isinstance(kwargs[key], dict) and not issubclass(self._instances[key], ListAttribute):
                    kwargs[key] = self._instances[key](**kwargs[key])
                elif isinstance(kwargs[key], dict):
                    kwargs[key] = [self._instances[key](**kwargs[key])]
                elif isinstance(kwargs[key], list) and not issubclass(self._instances[key], ListAttribute):
                    kwargs[key] = self._instances[key](**kwargs[key])
                elif isinstance(kwargs[key], list):
                    kwargs[key] = [self._instances[key](**item) for item in kwargs[key]]
            self.attribute_values[key] = kwargs[key]

    def _set_default(self, attr):
        pass

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


class Model(AttributeContainer, metaclass=ModelMeta):  # pylint: disable=R0205
    ''' Abstract entity model with an active record interface '''
    RESOURCE_NAME = 'None'

    def __init__(self, *args, **kwargs):
        cls = self.__class__
        attrs = cls._attrs
        if len(args) == 1 and isinstance(args[0], dict):
            # if args has dict in first row of args -> kwargs
            kwargs = args[0]
        elif len(args) != 0:
            raise ModelInitiationFailedException("Args can only be a dictionary")

        super().__init__(attrs=attrs, kwargs=kwargs)

    @property
    def public(self):
        ''' Return the public model attributes '''
        return attrs(self)

    def __repr__(self):
        return str(self.public)

    def get_resource_name(self):
        return self.RESOURCE_NAME

    def manager(self, type_check=True):
        ''' Create a database managet '''
        return Manager(self, type_check)

    @classmethod
    def get_attr_names(cls):
        return cls._graphql_attrs

class AttributeModel:
    def get_datas(self, item):
        attrs = self.__dict__
        attrs_dict = {}
        for attr in attrs.keys():
            value = getattr(self, attr, None)
            value_string = None
            if not isinstance(value, AttributeModel) and not isinstance(value, list):
                value_string = value
            else:
                if isinstance(value, list):
                    result_items = []
                    for item in value:
                        if isinstance(item, AttributeModel):
                            result_items.append(item.get_datas(item))
                        else:
                            result_items.append(item)
                    value_string = result_items
                else:
                    value_string = value.get_datas(value)
            attrs_dict[attr] = value_string
        return attrs_dict

class ListAttribute(AttributeModel):
    pass
