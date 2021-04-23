import copy
import json
import operator
from spb.orm.utils import attrs
from spb.exceptions import ModelInitiationFailedException, AttributeNameException, DoesNotExistsAttribute
from spb.core.models.types import Type
from spb.core.models.attrs import AttributeContainer


class ModelMeta(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        """ This make up some attributes
        1. class attribute to types variable
        2. class attribute to values variable

        model instance can use this as graphql attrs and model itself
        """
        super_new = super(ModelMeta, cls).__new__
        parents = [b for b in bases if isinstance(b, ModelMeta)]
        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super_new(cls, name, bases, attrs)

        new_attrs = {}
        new_attrs.update(attrs)

        # To save attribute [property name]s
        model_attr_property_names = {}
        for obj_name, obj in attrs.items():
            if isinstance(obj, Type):
                model_attr_property_names[obj.attr_name] = obj_name

        # To save attribute values
        model_attrs = {}
        for obj_name, obj in attrs.items():
            if isinstance(obj, Type):
                model_attrs[obj_name] = obj.validation(obj.default_value) if obj.default_value is not None else None

        # To save attribute types
        model_types = {}
        for obj_name, obj in attrs.items():
            if isinstance(obj, Type):
                model_types[obj_name] = obj

        new_class = super_new(cls, name, bases, new_attrs, **kwargs)
        new_class.add_to_class('_attrs', model_attrs)
        new_class.add_to_class('_attr_types', model_types)
        new_class.add_to_class('_attr_property_names', model_attr_property_names)

        return new_class

    def add_to_class(cls, name, value):
        setattr(cls, name, value)


class Model(AttributeContainer, metaclass=ModelMeta):
    ''' Abstract entity model with an active record interface '''
    RESOURCE_NAME = 'None'

    def __init__(self, *args, **kwargs):
        cls = self.__class__
        super().__init__(attrs=cls._attrs, attr_types=cls._attr_types, kwargs=kwargs)

    def __getattribute__(self, name):
        """Return attribute values and model instance attributes
        This model already has attributes as class variables
        but this variable is shared all of instances. so, this is make access to instance variable(attribute_values)
        attribute_values has been made by Model Metaclass and AttributeContainer class

        :param string name: attribute name to access
        :returns: instance values
        """
        cls = super().__getattribute__('__class__')
        if name in cls._attrs:
            return self.__getattribute__('attribute_values')[name]
        else:
            return super().__getattribute__(name)

    def __setattr__(self, name, value):
        """To use set attribute values and instance variables

        :param string name: Attribute name
        :returns: None
        """
        cls = self.__class__
        if name in cls._attrs:
            self.attribute_values[name] = self._attr_types[name].validation(value)
        else:
            super().__setattr__(name, value)

    def get_attribute_type(self, name: str):
        """Return attribute type instance according to name

        :param string name: model attribute name to return
        :returns: Type instance
        """
        self._check_is_name_in_attribute(name)
        return self._attr_types[name]

    def __call__(self, name:str):
        return self.get_attribute_tuple(name)

    def get_attribute_tuple(self, name: str):
        """ This returns Attribute Type and Value pair according to name
        This tuples are used to make query

        :param string name: Attribute name to find
        :returns: (Type, Any)
        """
        self._check_is_name_in_attribute(name)
        return (self._attr_types[name], self.attribute_values[name])

    def get_attributes_map(self, include: list = None, exclude: list = None):
        name_list = self._get_user_selected_property_names(include, exclude)

        result = {}
        for name in name_list:
            if name in self._attr_types:
                result[self._attr_types[name]] = self.attribute_values[name]
        return result

    def _check_is_name_in_attribute(self, name):
        if name in self._attr_types:
            return True
        else:
            raise DoesNotExistsAttribute('Does not exists attribute')

    def get_property_names(self, include: list = None, exclude: list = None):
        """ This returns attribute names list -> translated attribute name to graphql query attribute name
        if attribute name is defined as num_count and Type attribute_name property is numCount
        it returns ['numCount'] when user have passed ['num_count']

        :param list name_list: It consist of attribute names
        :returns: graphql attribute name list
        """
        name_list = self._get_user_selected_property_names(include, exclude)

        result = []
        for name in name_list:
            if name in self._attr_types:
                result.append(self._attr_types[name].attr_name)
        return result

    def _get_user_selected_property_names(self, include: list = None, exclude: list = None):
        name_list = self._attr_types.keys()

        if include is not None:
            name_list = include
        if exclude is not None:
            name_list = list(map(operator.sub, name_list, exclude))

        return name_list