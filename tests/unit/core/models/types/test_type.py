import pytest
import unittest
import uuid

from spb.core.models.attrs import AttributeModel
from spb.core.models.types import Type, ID, JsonObject, String, Int, Float, Boolean, List, PlainObject, PlainObjectList
from spb.exceptions import ImmutableValueChangeException, AttributeTypeException, TypeInitiationFailedException


'''
''  Test Type class
'''
class TypeTest(unittest.TestCase):
    def test_must_have_predefined_params(self):
        class OptionalClass():
            pass
        test_type = Type(property_name='a', default='default_value', express=OptionalClass)

    def test_doesnt_receive_property_name_param(self):
        class optionalClass():
            pass

        with pytest.raises(TypeInitiationFailedException):
            test_type = Type(default='default_value', express=optionalClass)


'''
''  Test ID type
'''
class IDTypeTest(unittest.TestCase):
    def setUp(self):
        self.id = uuid.uuid4()
        self.test_id = ID(property_name='id', default=id)

    def test_validation_returns_uuid_for_uuid_string_or_uuid(self):
        assert self.test_id.validation(self.id) == self.id
        assert str(self.test_id.validation(str(self.id))) == str(self.id)

    def test_validation_raises_AttributeTypeException_if_not_uuid(self):
        with pytest.raises(AttributeTypeException):
            self.test_id.validation('NOT UUID STRING')
        with pytest.raises(AttributeTypeException):
            self.test_id.validation(uuid.uuid5(uuid.NAMESPACE_DNS, 'superb-ai.com'))

    def test_return_graphql_query_with_attribute_name_and_value(self):
        self.assertEqual(self.test_id.to_query(self.id), ('id:$id', {'id': str(self.id)}))


'''
''  Test JSON type
'''
class JSONTypeTest(unittest.TestCase):
    def test_validation_returns_json_object_for_dictionary_or_json_object_input(self):
        #TODO : [MinjuneL] Not yed designed detail of use case!!
        pass

    def test_validation_raises_AttributeTypeException_if_not_json_ojbect_input(self):
        #TODO [MinjuneL]
        pass

    def test_return_graphql_query_with_attribute_name_and_value_dictionary(self):
        #TODO : [MinjuneL] Not yed designed detail of use case!!
        pass


'''
''  Test String type
'''
class StringTypeTest(unittest.TestCase):
    def setUp(self):
        self.test_string = String(property_name='test_string')

    def test_validation_returns_string_for_string_input(self):
        assert self.test_string.validation('test string') == 'test string'
        assert self.test_string.validation(None) == None

    def test_validation_raises_AttributeTypeException_if_not_string(self):
        with pytest.raises(AttributeTypeException):
            self.test_string.validation(123)
        with pytest.raises(AttributeTypeException):
            self.test_string.validation(True)

    def test_return_graphql_query_with_attribute_name_and_value_string(self):
        self.assertEqual(self.test_string.to_query('test data'), ('test_string:$test_string', {'test_string': 'test data'}))
        self.assertEqual(self.test_string.to_query(None), ('test_string:$test_string', {'test_string': None}))


'''
''  Test Number type
'''
class IntTypeTest(unittest.TestCase):
    def setUp(self):
        self.test_number = Int(property_name='test_number', default=123123)

    def test_validation_returns_number_for_number_input(self):
        assert self.test_number.validation(123123) == 123123
        # assert self.test_number.validation(0.33) == 0.33
        assert self.test_number.validation(0) == 0

    def test_validation_thorws_AttributeTypeException_if_not_number(self):
        with pytest.raises(AttributeTypeException):
            self.test_number.validation('WRONG TYPE')
        with pytest.raises(AttributeTypeException):
            self.test_number.validation(True)
        with pytest.raises(AttributeTypeException):
            self.test_number.validation(0.33)

    def test_return_graphql_query_with_attribute_name_and_value_int_(self):
        self.assertEqual(self.test_number.to_query(123123), ('test_number:$test_number', {'test_number': 123123}))
        self.assertEqual(self.test_number.to_query(None), ('test_number:$test_number', {'test_number': None}))
        self.assertEqual(self.test_number.to_query(0), ('test_number:$test_number', {'test_number': 0}))


class FloatTypeTest(unittest.TestCase):
    def setUp(self):
        self.test_float = Float(property_name='test_number', default=0.123123)

    def test_validation_returns_float_for_float_input(self):
        assert self.test_float.validation(0.1233) == 0.1233
        assert self.test_float.validation(0.0) == 0.0

    def test_validation_raises_AttributeTypeException_if_not_float(self):
        with pytest.raises(AttributeTypeException):
            self.test_float.validation('WRONG TYPE')
        with pytest.raises(AttributeTypeException):
            self.test_float.validation(True)

    def test_return_graphql_query_with_attribute_name_and_float(self):
        self.assertEqual(self.test_float.to_query(0.33), ('test_number:$test_number', {'test_number': 0.33}))
        self.assertEqual(self.test_float.to_query(None), ('test_number:$test_number', {'test_number': None}))


'''
''  Test Boolean type
'''
class BooleanTypeTest(unittest.TestCase):
    def setUp(self):
        self.test_bool = Boolean(property_name='test_bool', default=True)

    def test_validation_returns_boolean_or_null_for_boolean_or_none_input(self):
        assert self.test_bool.validation(True) == True
        assert self.test_bool.validation(False) == False
        assert self.test_bool.validation(None) == None

    def test_validation_throws_AttributeTypeException_if_not_boolean(self):
        with pytest.raises(AttributeTypeException):
            self.test_bool.validation('WRONG TYPE')
        with pytest.raises(AttributeTypeException):
            self.test_bool.validation(0)
        with pytest.raises(AttributeTypeException):
            self.test_bool.validation('True')

    def test_return_graphql_query_with_attribute_name_and_boolean_string(self):
        self.assertEqual(self.test_bool.to_query(True), ('test_bool:$test_bool', {'test_bool':True}))
        self.assertEqual(self.test_bool.to_query(False),('test_bool:$test_bool', {'test_bool':False}))
        self.assertEqual(self.test_bool.to_query(None),('test_bool:$test_bool', {'test_bool':None}))


'''
''  Test Object type
'''
class DummyTestAttribute(AttributeModel):
    def __init__(self, *args, **kwargs):
        self.attr_a = None
        self.attr_b = None


class WrongTestAttribute():
    pass


class PlainObjectTypeTest(unittest.TestCase):
    def setUp(self):
        self.test_plain_object = PlainObject(property_name='test_plain_object', express=DummyTestAttribute)

    def test_validation_returns_plain_object_for_plain_object_input(self):
        new_validation_object = DummyTestAttribute()
        assert self.test_plain_object.validation(new_validation_object) == new_validation_object
        assert self.test_plain_object.validation(None) == None

    def test_validation_raises_AttributeTypeException_if_not_plain_object(self):
        with pytest.raises(AttributeTypeException):
            self.test_plain_object.validation(WrongTestAttribute())
        with pytest.raises(AttributeTypeException):
            self.test_plain_object.validation([DummyTestAttribute()])
        with pytest.raises(AttributeTypeException):
            self.test_plain_object.validation(0)
        with pytest.raises(AttributeTypeException):
            self.test_plain_object.validation("WRONG_STRING_TYPE")

    def test_return_graphql_query_with_attribute_name_and_object_dictionary(self):
        obj = DummyTestAttribute()
        self.assertEqual(self.test_plain_object.to_query(obj),('test_plain_object:$test_plain_object', {
            'test_plain_object': obj
        }))
        self.assertEqual(self.test_plain_object.to_query(None),('test_plain_object:$test_plain_object', {
            'test_plain_object': None
        }))


'''
'' Test PlainObjectList type
'''
class PlainObjectListTypeTest(unittest.TestCase):
    def setUp(self):
        self.test_plain_object_list = PlainObjectList(property_name='test_plain_object', express=DummyTestAttribute)

    def test_validation_returns_plain_object_list_for_plain_object_input(self):
        new_validation_object = [DummyTestAttribute()]
        assert self.test_plain_object_list.validation(new_validation_object) == new_validation_object
        assert self.test_plain_object_list.validation(None) == None

    def test_validation_raises_AttributeTypeException_if_not_plain_object_list(self):
        with pytest.raises(AttributeTypeException):
            self.test_plain_object_list.validation([WrongTestAttribute()])
        with pytest.raises(AttributeTypeException):
            self.test_plain_object_list.validation(WrongTestAttribute())
        with pytest.raises(AttributeTypeException):
            self.test_plain_object_list.validation(DummyTestAttribute())
        with pytest.raises(AttributeTypeException):
            self.test_plain_object_list.validation(0)
        with pytest.raises(AttributeTypeException):
            self.test_plain_object_list.validation("WRONG_STRING_TYPE")

    def test_return_graphql_query_with_attribute_name_and_dictionary_list(self):
        object_list = [DummyTestAttribute()]
        self.assertEqual(self.test_plain_object_list.to_query(object_list),('test_plain_object:$test_plain_object', {
            'test_plain_object': object_list
        }))
        self.assertEqual(self.test_plain_object_list.to_query(None),('test_plain_object:$test_plain_object', {
            'test_plain_object': None
        }))


'''
''  Test list object type
'''
class ListTypeTest(unittest.TestCase):
    def test_validation_returns_list_object_for_list_input(self):
        #TODO : [MinjuneL] Not yed designed detail of use case!!
        pass

    def test_validation_raises_AttributeTypeException_if_not_list_object(self):
        #TODO [MinjuneL]
        pass

    def test_return_graphql_query_with_attribute_name_and_object_dictionary_list(self):
        #TODO : [MinjuneL] Not yed designed detail of use case!!
        pass
