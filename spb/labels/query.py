from spb.core.query import BaseQuery
from spb.exceptions import QueryTypeException

class Query(BaseQuery):
    def build_label_count_query(self, query_id: str = None, attrs: dict = None, response_attrs: list = None, page: int = None, page_size: int = None) -> str:
        self._set_variables(query_id, attrs, response_attrs, page, page_size)

        where_message, values = self._make_where_message()
        type_expressions = self._make_attribute_type_expressions()
        response_body = self._make_count_body_message()

        self.query_string = 'query %s {%s%s%s}' % (type_expressions, self.query_id, where_message, response_body)
        self._reset_variables()
        return self.query_string, values

    def _make_count_body_message(self):
        try:
            return '{count}'
        except TypeError as e:
            raise QueryTypeException('Invalid attribute exceptions: response must be set of string')