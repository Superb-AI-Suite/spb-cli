import pytest
import unittest
import uuid

from spb.core import Model
from spb.core.models.types import ID, JsonObject, String, Int, Float, Boolean, List, PlainObject, PlainObjectList
from spb.core.query import BaseQuery as Query
from spb.exceptions import AttributeTypeException, QueryTypeException

class QueryTest(unittest.TestCase):
    def setUp(self):
        self.id = uuid.uuid4()
        self.dummy_attrs = {
            ID(property_name='id'): self.id,
            JsonObject(property_name='info'): {
                'result': {
                    'classes': [{'dummy_class':'unknown_field'}]
                }
            },
            String(property_name='key'): 'key',
            Int(property_name='number'): 1,
            Float(property_name='number2'): 1.0,
            Boolean(property_name='boolean'): True
        }
        self.dummy_response_attrs = ['id']

    def test_init_query(self):
        query = Query()
        assert isinstance(query, Query)

    def test_build_query_string(self):
        query = Query()
        query_string, values = query.build_query(query_id = 'describe_xxxx', attrs = self.dummy_attrs, response_attrs = self.dummy_response_attrs)

        self.assertEqual(
            query_string,
            'query ($id:String,$info:JSONObject,$key:String,$number:Int,$number2:Float,$boolean:Boolean) {describe_xxxx(id:$id,info:$info,key:$key,number:$number,number2:$number2,boolean:$boolean){id}}'
        )
        self.assertEqual(
            values,
            {
                'id': str(self.id),
                'info': {'result': {'classes': [{'dummy_class': 'unknown_field'}]}},
                'key': 'key', 'number': 1, 'number2': 1.0, 'boolean': True
            }
        )
        query_string, values = query.build_query(query_id = 'describe_yyyy', response_attrs = self.dummy_response_attrs)
        self.assertEqual(
            query_string,
            'query  {describe_yyyy{id}}'
        )
        self.assertEqual(
            values,
            {}
        )

    def test_build_cursor_query_string(self):
        query = Query()
        query_string, values = query.build_cursor_query(query_id = "describe_xxxx", attrs = self.dummy_attrs, response_attrs = self.dummy_response_attrs)
        self.assertEqual(
            query_string,
            'query ($id:String,$info:JSONObject,$key:String,$number:Int,$number2:Float,$boolean:Boolean) {describe_xxxx(id:$id,info:$info,key:$key,number:$number,number2:$number2,boolean:$boolean){id}}'
        )

        self.assertEqual(
            values,
            {
                'id': str(self.id),
                'info': {'result': {'classes': [{'dummy_class': 'unknown_field'}]}},
                'key': 'key',
                'number': 1,
                'number2': 1.0,
                'boolean': True
            }
        )

    def test_build_cursor_query_string_with_page_size(self):
        query = Query()
        query_string, values = query.build_cursor_query(query_id = "describe_xxxx", attrs = self.dummy_attrs, response_attrs = self.dummy_response_attrs, page_size = 10)
        self.assertEqual(
            query_string,
            'query ($id:String,$info:JSONObject,$key:String,$number:Int,$number2:Float,$boolean:Boolean) {describe_xxxx(id:$id,info:$info,key:$key,number:$number,number2:$number2,boolean:$boolean,pageSize:$pageSize){count, next, previous, edges{id}}}'
        )

        self.assertEqual(
            values,
            {
                'id': str(self.id),
                'info': {'result': {'classes': [{'dummy_class': 'unknown_field'}]}},
                'key': 'key',
                'number': 1,
                'number2': 1.0,
                'boolean': True,
                'pageSize': 10
            }
        )

    def test_build_cursor_query_string_with_cursor(self):
        query = Query()
        query_string, values = query.build_cursor_query(query_id = "describe_xxxx", attrs = self.dummy_attrs, response_attrs = self.dummy_response_attrs, cursor = bytes("DUMMY_CURSOR", "utf-8"))
        self.assertEqual(
            query_string,
            'query ($id:String,$info:JSONObject,$key:String,$number:Int,$number2:Float,$boolean:Boolean) {describe_xxxx(id:$id,info:$info,key:$key,number:$number,number2:$number2,boolean:$boolean,cursor:$cursor,pageSize:$pageSize){id}}'
        )

        self.assertEqual(
            values,
            {
                'id': str(self.id),
                'info': {'result': {'classes': [{'dummy_class': 'unknown_field'}]}},
                'key': 'key',
                'number': 1,
                'number2': 1.0,
                'boolean': True,
                'cursor': b'DUMMY_CURSOR',
                'pageSize': 10
            }
        )

    def test_build_cursor_query_string_with_cursor_and_page_size(self):
        query = Query()
        query_string, values = query.build_cursor_query(query_id = "describe_xxxx", attrs = self.dummy_attrs, response_attrs = self.dummy_response_attrs, page_size = 1, cursor = bytes("DUMMY_CURSOR", "utf-8"))
        self.assertEqual(
            query_string,
            'query ($id:String,$info:JSONObject,$key:String,$number:Int,$number2:Float,$boolean:Boolean) {describe_xxxx(id:$id,info:$info,key:$key,number:$number,number2:$number2,boolean:$boolean,cursor:$cursor,pageSize:$pageSize,pageSize:$pageSize){count, next, previous, edges{id}}}'
        )

        self.assertEqual(
            values,
            {
                'id': str(self.id),
                'info': {'result': {'classes': [{'dummy_class': 'unknown_field'}]}},
                'key': 'key',
                'number': 1,
                'number2': 1.0,
                'boolean': True,
                'cursor': b'DUMMY_CURSOR',
                'pageSize': 1
            }
        )


    def test_build_query_string_with_setter(self):
        query = Query()
        query.query_id = 'describe_xxxx'
        query.attrs.update(self.dummy_attrs)
        query.response_attrs.extend(self.dummy_response_attrs)
        query.page = 10
        query.page_size = 100

        query_string, values = query.build_query()
        self.assertEqual(
            query_string,
            'query ($id:String,$info:JSONObject,$key:String,$number:Int,$number2:Float,$boolean:Boolean) {describe_xxxx(id:$id,info:$info,key:$key,number:$number,number2:$number2,boolean:$boolean,page:10,pageSize:100){count, edges{id}}}'
        )
        self.assertEqual(
            values,
            {
                'id': str(self.id),
                'info': {'result': {'classes': [{'dummy_class': 'unknown_field'}]}},
                'key': 'key', 'number': 1, 'number2': 1.0, 'boolean': True
            }
        )

    def test_build_query_raises_Exceptions_with_wrong_attr_keys(self):
        query = Query()
        with pytest.raises(QueryTypeException):
            wrong_attr_key = { 'wrong_key': 'value with wrong_key' }
            query.build_query(query_id = 'describe_wrong_xxxx', attrs = wrong_attr_key, response_attrs = self.dummy_response_attrs)

        with pytest.raises(AttributeTypeException):
            wrong_attr_values = {ID(property_name='id'): 'wrong_id_value'}
            query.build_query(query_id = 'describe_wrong_xxxx', attrs = wrong_attr_values, response_attrs = self.dummy_response_attrs)

        with pytest.raises(QueryTypeException):
            query.build_query(query_id = 'describe_wrong_xxxx', attrs = self.dummy_response_attrs, response_attrs = self.dummy_response_attrs)

    def test_build_query_raises_Exceptions_with_wrong_response_attrs(self):
        query = Query()
        with pytest.raises(QueryTypeException):
            wrong_response_attrs = [1, 2, 3]
            query.build_query(query_id = 'describe_wrong_xxxx', attrs = self.dummy_attrs, response_attrs = wrong_response_attrs)

        with pytest.raises(QueryTypeException):
            wrong_response_attrs = [ID(property_name='id')]
            query.build_query(query_id = 'describe_wrong_xxxx', attrs = self.dummy_attrs, response_attrs = wrong_response_attrs)

        with pytest.raises(QueryTypeException):
            query.build_query(query_id = 'describe_wrong_xxxx', attrs = self.dummy_attrs, response_attrs = self.dummy_attrs)


    def test_build_mutation_query_string(self):
        query = Query()
        mutation_query, variables = query.build_mutation_query(query_id = 'update_xxxx', attrs = self.dummy_attrs, response_attrs = self.dummy_response_attrs)

        self.assertEqual(
            mutation_query,
            'mutation ($id:String,$info:JSONObject,$key:String,$number:Int,$number2:Float,$boolean:Boolean) {update_xxxx(id:$id,info:$info,key:$key,number:$number,number2:$number2,boolean:$boolean){id}}'
        )
        self.assertEqual(
            variables,
            {
                'id': str(self.id),
                'info': {'result': {'classes': [{'dummy_class': 'unknown_field'}]}},
                'key': 'key', 'number': 1, 'number2': 1.0, 'boolean': True
            }
        )
        mutation_query, variables = query.build_mutation_query(query_id = 'update_yyyy', response_attrs = self.dummy_response_attrs)
        self.assertEqual(
            mutation_query,
            'mutation  {update_yyyy{id}}'
        )
        self.assertEqual(
            variables,
            {}
        )

    def test_build_mutation_query_string_with_setter(self):
        query = Query()
        query.query_id = 'update_xxxx'
        query.attrs.update(self.dummy_attrs)
        query.response_attrs.extend(self.dummy_response_attrs)

        mutation_query, variables = query.build_mutation_query()
        self.assertEqual(
            mutation_query,
            'mutation ($id:String,$info:JSONObject,$key:String,$number:Int,$number2:Float,$boolean:Boolean) {update_xxxx(id:$id,info:$info,key:$key,number:$number,number2:$number2,boolean:$boolean){id}}'
        )
        self.assertEqual(
            variables,
            {
                'id': str(self.id),
                'info': {'result': {'classes': [{'dummy_class': 'unknown_field'}]}},
                'key': 'key', 'number': 1, 'number2': 1.0, 'boolean': True
            }
        )

    def test_build_mutation_query_raises_Exceptions_with_wrong_attr_keys(self):
        query = Query()
        with pytest.raises(QueryTypeException):
            wrong_attr_key = { 'wrong_key': 'value with wrong_key' }
            query.build_mutation_query(query_id = 'update_wrong_xxxx', attrs = wrong_attr_key, response_attrs = self.dummy_response_attrs)

        with pytest.raises(AttributeTypeException):
            wrong_attr_values = {ID(property_name='id'): 'wrong_id_value'}
            query.build_mutation_query(query_id = 'update_wrong_xxxx', attrs = wrong_attr_values, response_attrs = self.dummy_response_attrs)

        with pytest.raises(QueryTypeException):
            query.build_mutation_query(query_id = 'update_wrong_xxxx', attrs = self.dummy_response_attrs, response_attrs = self.dummy_response_attrs)

    def test_build_mutation_query_raises_Exceptions_with_wrong_response_attrs(self):
        query = Query()
        with pytest.raises(QueryTypeException):
            wrong_response_attrs = [1, 2, 3]
            query.build_mutation_query(query_id = 'update_wrong_xxxx', attrs = self.dummy_attrs, response_attrs = wrong_response_attrs)

        with pytest.raises(QueryTypeException):
            wrong_response_attrs = [ID(property_name='id')]
            query.build_mutation_query(query_id = 'update_wrong_xxxx', attrs = self.dummy_attrs, response_attrs = wrong_response_attrs)

        with pytest.raises(QueryTypeException):
            query.build_mutation_query(query_id = 'update_wrong_xxxx', attrs = self.dummy_attrs, response_attrs = self.dummy_attrs)
