from urllib.parse import urlencode, unquote
from spb.core import query
from spb.core.query import BaseQuery
from spb.exceptions import QueryTypeException
from spb.models import data, project


class Query(BaseQuery):
    def build_request_autolabel_query(self, project_id: str, tags: list = None) -> str:
        self.query_string = self._make_request_autolabel_query_string()
        values = self._make_request_autolabel_query_value(project_id, tags)
        self._reset_variables()
        return self.query_string, values

    def _make_request_autolabel_query_string(self):
        query_string = f'mutation {self.query_id}($projectId:String!, $filter:String!) {{{self.query_id}(projectId: $projectId, filter: $filter) {{id}}}}'
        return query_string

    def _make_request_autolabel_query_value(self, project_id, tags):
        values = {}
        if project_id is not None:
            values.update({"projectId": str(project_id)})
        if tags is not None:
            values.update({"filter": unquote(urlencode([("tags_name_all[]", tag) for tag in tags]))})
        return values

    def build_task_list_query(self, project_id, status_in, page, page_size) -> str:
        self.query_string = self._make_task_list_query_string()
        values = self._make_task_list_query_value(project_id, status_in, page, page_size)
        self._reset_variables()
        return self.query_string, values

    def _make_task_list_query_string(self):
        query_string = f'query {self.query_id}($projectId:String!, $statusIn:[String!], $page: Int!, $pageSize: Int!) \
            {{{self.query_id}(projectId: $projectId, statusIn: $statusIn, page: $page, pageSize: $pageSize) \
            {{count, results}}}}'
        return query_string

    def _make_task_list_query_value(self, project_id, status_in, page, page_size):
        values = {}
        values.update({"page": page})
        values.update({"pageSize": page_size})

        if project_id is not None:
            values.update({"projectId": str(project_id)})
        if status_in is not None:
            values.update({"statusIn": status_in})
        return values
