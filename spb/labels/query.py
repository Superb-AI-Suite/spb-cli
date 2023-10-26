from typing import Optional, List

from spb.core.query import BaseQuery
from spb.exceptions import QueryTypeException
from spb.utils.search_filter import SearchFilter

from .label import Tags

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
    
    def build_search_labels_query(
        self,
        query_id: str,
        project_id: str,
        response_attrs: list,
        filter: Optional[SearchFilter] = None,
        cursor: Optional[str] = None,
        page_size: int = 10
    ):
        self.response_attrs = response_attrs
        self.query_id = query_id
        self.page_size = page_size
        self.query_string = (
            "query ($projectId: String!, $pageSize: Int!, $filter: String, $cursor: String) {"
            f"  {self.query_id}("
            "       projectId: $projectId, pageSize: $pageSize, filter:$filter, cursor:$cursor"
            "   ) {"
            "       count "
            "       edges {"
            f"          {' '.join(self.response_attrs)}"
            "       } "
            "       cursor"
            "   }"
            "}"
        )
        values = {
            "projectId": str(project_id),
            "filter": filter.to_filter_string() if filter is not None else None,
            "pageSize": page_size,
            "cursor": cursor
        }
        self._reset_variables()
        return self.query_string, values
    
    def build_update_tags_query(
        self,
        project_id: str,
        id: str,
        tags: List[Tags]
    ):
        self.query_string = (
            "mutation ($projectId: String!, $id: String!, $tags: [JSONObject!]) {"
            f"  {self.query_id}("
            "       projectId: $projectId, id: $id, tags: $tags"
            "   ) {"
            f"      {self._make_response_attrs_message()}"
            "     } }"
        )
        values = {
            "projectId": project_id,
            "id": id,
            "tags": [{"name": tag.name} for tag in tags]
        }
        self._reset_variables()
        return self.query_string, values
    
    def build_update_info_query(
            self,
            project_id: str,
            id: str,
            result: Optional[dict]
    ):
        self.query_string = (
            "mutation ($projectId: String!, $id: String!, $result: JSONObject) {"
            f"  {self.query_id}("
            "       projectId: $projectId, id: $id, result: $result"
            "   ) {"
            f"      {self._make_response_attrs_message()}"
            "     } }"
        )
        values = {
            "projectId": project_id,
            "id": id,
            "result": result
        }
        self._reset_variables()
        return self.query_string, values

    def build_update_status_query(
        self,
        project_id: str,
        id: str,
        status: str,
    ):
        self.query_string = (
            "mutation ($projectId: String!, $id: String!, $status: String!) {"
            f"  {self.query_id}("
            "       projectId: $projectId, id: $id, status: $status"
            "   ) {"
            f"      {self._make_response_attrs_message()}"
            "     } }"
        )
        values = {
            "projectId": project_id,
            "id": id,
            "status": status
        }
        self._reset_variables()
        return self.query_string, values

    def build_update_assignee_query(
        self,
        project_id: str,
        id: str,
        assignee: Optional[str] = None,
    ):
        self.query_string = (
            "mutation ($projectId: String!, $id: String!, $assignee: String) {"
            f"  {self.query_id}("
            "       projectId: $projectId, id: $id, assignee: $assignee"
            "   ) {"
            f"      {self._make_response_attrs_message()}"
            "     } }"
        )
        values = {
            "projectId": project_id,
            "id": id,
            "assignee": assignee
        }
        self._reset_variables()
        return self.query_string, values

    def build_update_reviewer_query(
        self,
        project_id: str,
        id: str,
        reviewer: Optional[str] = None,
    ):
        self.query_string = (
            "mutation ($projectId: String!, $id: String!, $reviewer: String) {"
            f"  {self.query_id}("
            "       projectId: $projectId, id: $id, reviewer: $reviewer"
            "   ) {"
            f"      {self._make_response_attrs_message()}"
            "     } }"
        )
        values = {
            "projectId": project_id,
            "id": id,
            "reviewer": reviewer
        }
        self._reset_variables()
        return self.query_string, values
