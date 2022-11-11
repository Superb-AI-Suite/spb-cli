import math
from typing import Optional

import rich
import rich.console
import rich.table
from spb.core.manager import BaseManager

from .project import Project
from .query import Query
from .session import Session


class ProjectManager(BaseManager):
    PROJECT_LIST_QUERY_ID = "projects"

    def __init__(self, team_name=None, access_key=None):
        self.session = Session(team_name=team_name, access_key=access_key)
        self.query = Query()

    def create_project(self, project_info) -> Optional[Project]:
        query_id = "createProject"
        query = f"mutation ($projectInfo:JSONObject!) {{{query_id}(projectInfo: $projectInfo)}}"
        values = {"projectInfo": project_info}
        response = self.session.execute(query, values)

        return self.session.get_result_from_create_project(response, query_id)

    def describe_project(
        self, page: int = 1, page_size: int = 10, show_options: str = "default"
    ):

        supported_options = ["default", "reviews"]
        assert show_options in supported_options

        _, projects = self.get_project_list(page=page, page_size=page_size)
        console = rich.console.Console()
        table = rich.table.Table(show_header=True, header_style="bold magenta")
        table.add_column("NAME", width=50)
        table.add_column("LABELS", justify="right")
        if show_options == 'default':
            self.print_default_option_projects(projects=projects, table=table)
        elif show_options == 'reviews':
            self.print_review_option_projects(projects=projects, table=table)
        console.print(table)

    def print_default_option_projects(self, projects, table):
        table.add_column("IN PROGRESS", justify="right")
        table.add_column("SUBMITTED", justify="right")
        table.add_column("SKIPPED", justify="right")

        for project in projects:
            in_progress_ratio = math.ceil( project.in_progress_label_count / project.label_count * 100 ) if project.label_count > 0 else 0
            skipped_ratio = math.ceil( project.skipped_label_count / project.label_count * 100 ) if project.label_count > 0 else 0
            table.add_row(
                project.name,
                f"{project.label_count}",
                f"{project.in_progress_label_count} ({in_progress_ratio} %)",
                f"{project.submitted_label_count} ({project.progress} %)",
                f"{project.skipped_label_count} ({skipped_ratio} %)"
            )

    def print_review_option_projects(self, projects, table):
        table.add_column("IN PROGRESS\nRejected")
        table.add_column("IN PROGRESS\nNot Submitted")
        table.add_column("SUBMITTED\nApproved")
        table.add_column("SUBMITTED\nPending Review")
        table.add_column("SKIPPED\nApproved")
        table.add_column("SKIPPED\nPending Review")

        for project in projects:
            stats = project.stats if project.stats is not None else []

            in_progress_count = ([item for item in stats if item['type'] == 'IN_PROGRESS_COUNT'][0:1] or [{}])[0].get('info', {})
            submitted_count = ([item for item in stats if item['type'] == 'SUBMITTED_COUNT'][0:1] or [{}])[0].get('info', {})
            skipped_count = ([item for item in stats if item['type'] == 'SKIPPED_COUNT'][0:1] or [{}])[0].get('info', {})

            table.add_row(
                project.name,
                f'{project.label_count}',
                f'{in_progress_count.get("rejected", 0)}',
                f'{in_progress_count.get("not_submitted", 0)}',
                f'{submitted_count.get("approved", 0)}',
                f'{submitted_count.get("pending_review", 0)}',
                f'{skipped_count.get("approved", 0)}',
                f'{skipped_count.get("pending_review", 0)}'
            )

    def get_project_list(self, page: int = 1, page_size: int = 10):
        query, _ = self._get_project_list_query(
            name=None, page=page, page_size=page_size
        )

        response = self.session.execute(query, None)
        return self.session.extract_project_list(response, self.PROJECT_LIST_QUERY_ID)

    def get_project_by_name(self, name: str) -> Optional[Project]:
        query, value = self._get_project_list_query(name=name, page=1, page_size=1)

        response = self.session.execute(query, value)
        try:
            project = self.session.extract_project(response, self.PROJECT_LIST_QUERY_ID)
        except:
            project = None
        return project

    def get_project_by_id(self, id: str):
        query, value = self._get_project_list_query()

    def _get_project_list_query(
        self, name: str = None, page: int = 1, page_size: int = 10
    ):
        self.query.query_id = self.PROJECT_LIST_QUERY_ID

        project = Project(name=name)

        if project.name is not None:
            query_attrs = project.get_attributes_map(include=["name"])
            self.query.attrs.update(query_attrs)

        self.query.page = page
        self.query.page_size = page_size

        self.query.response_attrs.extend(project.get_property_names())

        query, value = self.query.build_query()
        return query, value
