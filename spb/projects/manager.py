import uuid
from typing import List, Optional

from spb.core.manager import BaseManager
from spb.exceptions import PreConditionException
from spb.libs.phy_credit.phy_credit.imageV2.project_info import ProjectInfo

from .project import Project
from .query import Query
from .session import Session


class ProjectManager(BaseManager):
    PROJECT_LIST_QUERY_ID = "projects"
    PROJECT_QUERY_ID = "project"

    def __init__(self, team_name=None, access_key=None):
        self.session = Session(team_name=team_name, access_key=access_key)
        self.query = Query()

    def create_project(
        self,
        name: str,
        label_interface: dict,
        description: str = "",
        is_public: bool = False,
        allow_advanced_qa: bool = False,
    ) -> Optional[Project]:
        query_id = "createProject"
        self.query.query_id = query_id
        project_info = {
            "name": name,
            "description": description,
            "label_interface": label_interface,
            "is_public": is_public,
            "settings": {
                "allow_advanced_qa": allow_advanced_qa,
            },
        }
        if "workapp" not in project_info:
            project_info["workapp"] = label_interface["type"]

        project = Project()
        response_attrs = "\n".join(project.get_property_names())
        query = f"mutation ($projectInfo:JSONObject!) {{{query_id}(projectInfo: $projectInfo) {{{response_attrs}}}}}"
        values = {"projectInfo": project_info}
        response = self.session.execute(query, values)
        return self.session.get_result_from_response_project(
            response, query_id
        )

    def update_project(
        self,
        id: uuid.UUID,
        new_name: str = None,
        label_interface: dict = None,
        description: str = None,
        is_public: bool = None,
        allow_advanced_qa: bool = None,
    ):
        existing_project = self.get_project_by_id(id=id)

        query_id = "updateProject"
        self.query.query_id = query_id
        project_info = dict()
        if new_name is not None:
            project_info.update({"name": new_name})
        if description is not None:
            project_info.update({"description": description})
        if label_interface is not None:
            project_info.update({"label_interface": label_interface})
            if (
                existing_project.label_interface["type"]
                != label_interface["type"]
            ):
                raise PreConditionException(
                    "[ERROR] Workapp type cannot be changed"
                )
        if is_public is not None:
            project_info.update({"is_public": is_public})
        if allow_advanced_qa is not None:
            project_info.update(
                {
                    "settings": {
                        "allow_advanced_qa": allow_advanced_qa,
                    }
                }
            )

        project = Project(id=id)
        id = project.to_json()["id"]
        response_attr = "\n".join(project.get_property_names())
        query = f"mutation ($id: String!, $projectInfo: JSONObject!) {{{query_id}(id: $id, projectInfo: $projectInfo) {{{response_attr}}}}}"
        values = {"id": id, "projectInfo": project_info}
        response = self.session.execute(query, values)
        return self.session.get_result_from_response_project(
            response, query_id
        )

    def get_project_list(
        self,
        page: int = 1,
        page_size: int = 10,
        name_icontains: str = None,
        data_type: str = None,
        annotation_type: List[str] = None,
    ):
        self.query.query_id = self.PROJECT_LIST_QUERY_ID

        project = Project()

        self.query.name_icontains = name_icontains
        self.query.data_type = data_type
        self.query.annotation_type = annotation_type
        self.query.page = page
        self.query.page_size = page_size

        self.query.response_attrs.extend(project.get_property_names())

        query, _ = self.query.build_query()

        response = self.session.execute(query, None)
        return self.session.extract_project_list(
            response, self.PROJECT_LIST_QUERY_ID
        )

    def get_project_by_name(self, name: str) -> Optional[Project]:
        self.query.query_id = self.PROJECT_QUERY_ID

        project = Project(name=name)

        query_attrs = project.get_attributes_map(include=["name"])
        self.query.attrs.update(query_attrs)

        self.query.response_attrs.extend(project.get_property_names())

        query, value = self.query.build_query()

        response = self.session.execute(query, value)
        project = self.session.extract_project(response, self.PROJECT_QUERY_ID)

        return project

    def get_project_by_id(self, id: uuid.UUID):
        self.query.query_id = self.PROJECT_QUERY_ID

        project = Project(id=id)

        query_attrs = project.get_attributes_map(include=["id"])
        self.query.attrs.update(query_attrs)

        self.query.response_attrs.extend(project.get_property_names())

        query, value = self.query.build_query()

        response = self.session.execute(query, value)
        project = self.session.extract_project(response, self.PROJECT_QUERY_ID)

        return project

    def delete_project(self, id: uuid.UUID):
        query_id = "deleteProject"
        self.query.query_id = query_id
        project = Project(id=id)
        query_attrs = project.get_attributes_map(include=["id"])
        self.query.attrs.update(query_attrs)
        self.query.required_attrs.extend(
            project.get_property_names(include=["id"])
        )

        query, values = self.query.build_mutation_query()

        response = self.session.execute(query, values)

        return self.session.get_result_from_response(response, query_id)
