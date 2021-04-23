import logging
from typing import List, Dict

from spb.core.models.types import Type
from spb.exceptions import AttributeTypeException, QueryTypeException

logger = logging.getLogger()


class BaseQuery(object):

    def __init__(self):
        self._query_id: str = None
        self._attrs: Dict = {}
        self._response_attrs: List = []
        self._required_attrs: List = []
        self._page: int = None
        self._page_size: int = None

        self._query_string: str = None

    def build_query(self, query_id: str = None, attrs: dict = None, response_attrs: list = None, page: int = None, page_size: int = None) -> str:
        self._set_variables(query_id, attrs, response_attrs, page, page_size)

        where_message, values = self._make_where_message()
        type_expressions = self._make_attribute_type_expressions()
        response_body = self._make_body_message()

        self.query_string = 'query %s {%s%s%s}' % (type_expressions, self.query_id, where_message, response_body)
        self._reset_variables()
        return self.query_string, values

    def build_mutation_query(self, query_id: str = None, attrs: dict = None, response_attrs: list = None) -> str:
        self._set_variables(query_id, attrs, response_attrs)

        mutation_message, values = self._make_where_message()
        type_expressions = self._make_attribute_type_expressions()
        response_body = self._make_body_message()

        self.query_string = 'mutation %s {%s%s%s}' % (type_expressions, self.query_id, mutation_message, response_body)
        self._reset_variables()
        return self.query_string, values

    def _make_attribute_type_expressions(self) -> str:
        attrs = self._attrs
        required_attrs = self._required_attrs

        type_expressions = []
        for type_instance, attr in attrs.items():
            value = f'{type_instance.GRAPHQL_TYPE}!' if type_instance.attr in required_attrs else type_instance.GRAPHQL_TYPE
            type_expressions.append(f'${type_instance.attr}:{value}')

        return f'({",".join(type_expressions)})' if len(type_expressions) > 0 else ''

    def _make_where_message(self) -> (str, dict):
        params = []
        values = {}
        for attr_type, value in self.attrs.items():
            query, v = attr_type.to_query(value)
            values.update(v)
            params.append(query)
        if self.page is not None:
            params.append(f"page:{self.page}")
        if self.page_size is not None:
            params.append(f"pageSize:{self.page_size}")

        return f'({",".join(params)})' if len(params) > 0 else '', values

    def _make_body_message(self) -> str:
        try:
            if self.page is not None and self.page_size is not None:
                return '{count, edges{%s}}' % ' '.join(self.response_attrs)
            else:
                return '{%s}' % ' '.join(self.response_attrs)
        except TypeError as e:
            raise QueryTypeException('Invalid attribute exceptions: response must be set of string')

    @property
    def query_id(self):
        return self._query_id

    @query_id.setter
    def query_id(self, query_id: str = ''):
        if not isinstance(query_id, str) and query_id is not None:
            raise QueryTypeException('Query Attribute Type Exception: query_id must be string')
        self._query_id = query_id

    @property
    def attrs(self):
        if not isinstance(self._attrs, Dict):
            return {}
        return self._attrs

    @attrs.setter
    def attrs(self, attrs: Dict = {}):
        if not isinstance(attrs, dict) and attrs is not None:
            raise QueryTypeException('Query Attribute Type Exception: attrs must be dictionary of {Type : value}')
        if attrs is not None:
            for attr_type, value in attrs.items():
                if not isinstance(attr_type, Type):
                    raise QueryTypeException('Invalid key exceptions: key is not Type instance')

        self._attrs = attrs

    @property
    def response_attrs(self):
        if not isinstance(self._response_attrs, List):
            return []
        return self._response_attrs if self._response_attrs is not None else []

    @response_attrs.setter
    def response_attrs(self, response_attrs: List = []):
        if not isinstance(response_attrs, list) and response_attrs is not None:
            raise QueryTypeException('Query Attribute Type Exception: response_attrs must be set of string')
        if response_attrs is not None:
            for item in response_attrs:
                if not isinstance(item, str):
                    raise QueryTypeException('Query Attribute Type Exception: response_attrs must be set of string')
        self._response_attrs = response_attrs

    @property
    def required_attrs(self):
        if not isinstance(self._required_attrs, List):
            return []
        return self._required_attrs if self._required_attrs is not None else []

    @required_attrs.setter
    def required_attrs(self, required_attrs: List = []):
        if not isinstance(required_attrs, list) and required_Attrs is not None:
            raise QueryTypeException('Query Attribute Type Exception: required_attrs must be set of string')
        if required_attrs is not None:
            for item in required_attrs:
                if not isinstance(item, str):
                    raise QueryTypeException('Query Attribute Type Exception: response_attrs must be set of string')
        self._required_attrs = required_attrs

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, page: int = 0):
        if not isinstance(page, int) and page is not None:
            raise QueryTypeException('Query Attribute Type Exception: page must be integer')
        elif page is not None and page < 0:
            raise QueryTypeException('Query Attribute Type Exception: page must be equal or greater than 0')
        self._page = page

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, page_size: int = 10):
        if not isinstance(page_size, int) and page_size is not None:
            raise QueryTypeException('Query Attribute Type Exception: page_size must be integer')
        elif page_size is not None and page_size < 0:
            raise QueryTypeException('Query Attribute Type Exception: page_size must be equal or greater than 0')
        self._page_size = page_size

    def _set_variables(self, query_id: str = None, attrs: Dict = None, response_attrs: List = None, page: int = None, page_size: int = None):
        if query_id is not None:
            self.query_id = query_id
        if attrs is not None:
            self.attrs = attrs
        if response_attrs is not None:
            self.response_attrs = response_attrs
        if page is not None:
            self.page = page
        if page_size is not None:
            self.page_size = page_size

    def _reset_variables(self):
        self.query_id = None
        self.attrs = {}
        self.response_attrs = []
        self.page = None
        self.page_size = None