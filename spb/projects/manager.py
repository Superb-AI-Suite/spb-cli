from spb.core.manager import BaseManager
from .session import Session
from .query import Query
from .project import Project

class ProjectManager(BaseManager):
    PROJECT_LIST_QUERY_ID = 'projects'

    def __init__(self):
        self.session = Session()
        self.query = Query()

    def get_project_list(self, page: int = 1, page_size: int = 10):
        query, _ = self._get_project_list_query(name = None, page=page, page_size=page_size)

        response = self.session.execute(query, None)
        return self.session.extract_project_list(response, self.PROJECT_LIST_QUERY_ID)


    def get_project(self, name:str):
        query, value = self._get_project_list_query(name = name, page=1, page_size=1)

        response = self.session.execute(query, value)
        project = self.session.extract_project(response, self.PROJECT_LIST_QUERY_ID)
        return project

    def _get_project_list_query(self, name:str = None, page: int = 1, page_size: int = 10):
        self.query.query_id = self.PROJECT_LIST_QUERY_ID

        project = Project(
            name = name
        )

        if project.name is not None:
            query_attrs = project.get_attributes_map(include=['name'])
            self.query.attrs.update(query_attrs)

        self.query.page = page
        self.query.page_size = page_size

        self.query.response_attrs.extend(project.get_property_names())

        query, value = self.query.build_query()
        return query, value