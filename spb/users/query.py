from uuid import UUID

from spb.core.query import BaseQuery


class Query(BaseQuery):
    def build_project_users_query(self, project_id: UUID):
        self.query_string = (
            "query("
            "$projectId: String!"
            ") {"
            f"{self.query_id}("
            "projectId: $projectId"
            ") { count edges { "
            f"{self._make_response_attrs_message()}"
            "} }"
            "}"
        )
        values = {
            "projectId": str(project_id)
        }
        self._reset_variables()
        return self.query_string, values
