import unittest
import uuid
from unittest.mock import Mock, patch

from spb.projects import Project
from spb.projects.manager import ProjectManager
from spb.projects.query import Query

from .mocks import (
    MOCK_PROJECT,
    MOCK_PROJECT_RESPONSE_JSON,
    MOCK_PROJECTS_RESPONSE_JSON,
)


class ProjectManagerTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_project_query_with_right_name(self):
        query = Query()
        query.query_id = ProjectManager.PROJECT_LIST_QUERY_ID
        project = Project(name="MOCK_NAME")
        query_attrs = project.get_attributes_map(include=["name"])
        query.attrs.update(query_attrs)
        query.page = 1
        query.page_size = 1
        query.response_attrs.extend(project.get_property_names())
        query, value = query.build_query()

        print(query)

        self.assertEqual(
            query,
            "query ($name:String) {projects(name:$name,page:1,pageSize:1){count, edges{id name labelInterface workapp settings labelCount isPublic createdAt createdBy lastUpdatedAt lastUpdatedBy progress submittedLabelCount inProgressLabelCount skippedLabelCount stats}}}",
        )
        self.assertEqual(value, {"name": "MOCK_NAME"})

    def test_get_project_list_query(self):
        query = Query()
        query.query_id = ProjectManager.PROJECT_LIST_QUERY_ID
        project = Project()
        query.page = 1
        query.page_size = 10
        query.response_attrs.extend(project.get_property_names())
        query, value = query.build_query()

        self.assertEqual(
            query,
            "query  {projects(page:1,pageSize:10){count, edges{id name labelInterface workapp settings labelCount isPublic createdAt createdBy lastUpdatedAt lastUpdatedBy progress submittedLabelCount inProgressLabelCount skippedLabelCount stats}}}",
        )
        self.assertEqual(value, {})

    @patch("requests.sessions.Session.post")
    def test_get_project(self, mock_response):
        response = mock_response.return_value
        response.status_code = 200
        response.json.return_value = MOCK_PROJECT_RESPONSE_JSON

        manager = ProjectManager()
        project = manager.get_project_by_name(name="MOCK_PROJECT")

        self.assertEqual(
            project.id, uuid.UUID("a9c1f5fa-e698-446b-ab96-fdf9f68a9625")
        )
        self.assertEqual(project.name, "MOCK_PROJECT")

    @patch("requests.sessions.Session.post")
    def test_get_project_list(self, mock_response):
        response = mock_response.return_value
        response.status_code = 200
        response.json.return_value = MOCK_PROJECTS_RESPONSE_JSON

        manager = ProjectManager()
        count, projects = manager.get_project_list()

        self.assertEqual(count, 1)
        self.assertEqual(len(projects), 1)
        project = projects[0]
        self.assertEqual(
            project.id, uuid.UUID("a9c1f5fa-e698-446b-ab96-fdf9f68a9625")
        )
        self.assertEqual(project.name, "MOCK_PROJECT")

        self.assertEqual(len(project.stats), 3)
        for stat in project.stats:
            self.assertIn(
                stat.get("type"),
                ["IN_PROGRESS_COUNT", "SUBMITTED_COUNT", "SKIPPED_COUNT"],
            )
