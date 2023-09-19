import json
from uuid import UUID
from typing import Dict, List, Tuple

from spb.core.query import BaseQuery


class Query(BaseQuery):
    def __init__(self):
        super().__init__()
        self._name_icontains: str = None
        self._data_type: str = None
        self._annotation_type: List[str] = None

    @property
    def name_icontains(self):
        return self._name_icontains

    @name_icontains.setter
    def name_icontains(self, name_icontains):
        self._name_icontains = name_icontains

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, data_type):
        self._data_type = data_type

    @property
    def annotation_type(self):
        return self._annotation_type

    @annotation_type.setter
    def annotation_type(self, annotation_type):
        self._annotation_type = annotation_type

    def build_query(
        self,
        query_id: str = None,
        attrs: dict = None,
        response_attrs: list = None,
        page: int = None,
        page_size: int = None,
        name_icontains: str = None,
        data_type: str = None,
        annotation_type: List[str] = None,
    ):
        self._set_variables(
            query_id=query_id,
            attrs=attrs,
            response_attrs=response_attrs,
            page=page,
            page_size=page_size,
            name_icontains=name_icontains,
            data_type=data_type,
            annotation_type=annotation_type,
        )

        where_message, values = self._make_where_message()
        type_expressions = self._make_attribute_type_expressions()
        response_body = self._make_body_message()
        self.query_string = "query %s {%s%s%s}" % (
            type_expressions,
            self.query_id,
            where_message,
            response_body,
        )
        self._reset_variables()
        return self.query_string, values

    def _make_where_message(self) -> Tuple[str, dict]:
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
        if self.name_icontains is not None:
            params.append(f'nameIcontains:"{self.name_icontains}"')
        if self.data_type is not None:
            params.append(f'dataType:"{self.data_type}"')
        if self.annotation_type is not None:
            params.append(f"annotationType:{json.dumps(self.annotation_type)}")

        return f'({",".join(params)})' if len(params) > 0 else "", values

    def _set_variables(
        self,
        query_id: str = None,
        attrs: Dict = None,
        response_attrs: List = None,
        page: int = None,
        cursor: bytes = None,
        page_size: int = None,
        name_icontains: str = None,
        data_type: str = None,
        annotation_type: List[str] = None,
    ):
        if query_id is not None:
            self.query_id = query_id
        if attrs is not None:
            self.attrs = attrs
        if response_attrs is not None:
            self.response_attrs = response_attrs
        if page is not None:
            self.page = page
        if cursor is not None:
            self.cursor = cursor
        if page_size is not None:
            self.page_size = page_size
        if name_icontains is not None:
            self.name_icontains = name_icontains
        if data_type is not None:
            self.data_type = data_type
        if annotation_type is not None:
            self.annotation_type = annotation_type

    def build_tags_query(self, project_id: UUID):
        self.query_string = (
            "query("
            "$projectId: String!"
            ") {"
            f"{self.query_id}("
            "projectId: $projectId"
            ") { count edges { "
            f"{self._make_response_attrs_message()} "
            "} }"
            "}"
        )
        values = {
            "projectId": str(project_id)
        }
        self._reset_variables()
        return self.query_string, values
