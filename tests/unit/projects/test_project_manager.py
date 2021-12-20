import unittest
import uuid
from unittest.mock import patch, Mock

from spb.projects import Project
from spb.projects.manager import ProjectManager

from .mocks import MOCK_PROJECT, MOCK_PROJECT_RESPONSE_JSON


class ProjectManagerTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_project_query_with_right_name(self):
        manager = ProjectManager()
        query, value = manager._get_project_list_query(name='MOCK_NAME', page=1, page_size=1)

        self.assertEqual(
            query,
            'query ($name:String) {projects(name:$name,page:1,pageSize:1){count, edges{id name labelInterface workapp labelCount progress submittedLabelCount inProgressLabelCount skippedLabelCount stats}}}'
        )
        self.assertEqual(
            value,
            {'name': 'MOCK_NAME'}
        )

    def test_get_project_list_query(self):
        manager = ProjectManager()
        query, value = manager._get_project_list_query(page=1, page_size=10)

        self.assertEqual(
            query,
            'query  {projects(page:1,pageSize:10){count, edges{id name labelInterface workapp labelCount progress submittedLabelCount inProgressLabelCount skippedLabelCount stats}}}'
        )
        self.assertEqual(
            value,
            {}
        )

    @patch('spb.core.session.requests.post')
    def test_get_project(self, mock_response):
        response = mock_response.return_value
        response.status_code = 200
        response.json.return_value = MOCK_PROJECT_RESPONSE_JSON

        manager = ProjectManager()
        project = manager.get_project(name = 'MOCK_PROJECT')

        self.assertEqual(
            project.id,
            uuid.UUID('a9c1f5fa-e698-446b-ab96-fdf9f68a9625')
        )
        self.assertEqual(
            project.name,
            'MOCK_PROJECT'
        )

    @patch('spb.core.session.requests.post')
    def test_get_project_list(self, mock_response):
        response = mock_response.return_value
        response.status_code = 200
        response.json.return_value = MOCK_PROJECT_RESPONSE_JSON

        manager = ProjectManager()
        count, projects = manager.get_project_list()

        self.assertEqual(
            count,
            1
        )
        self.assertEqual(
            len(projects),
            1
        )
        project = projects[0]
        self.assertEqual(
            project.id,
            uuid.UUID('a9c1f5fa-e698-446b-ab96-fdf9f68a9625')
        )
        self.assertEqual(
            project.name,
            'MOCK_PROJECT'
        )

        self.assertEqual(
            len(project.stats),
            3
        )
        for stat in project.stats:
            self.assertIn(
                stat.get('type'),
                ['IN_PROGRESS_COUNT', 'SUBMITTED_COUNT', 'SKIPPED_COUNT']
            )
