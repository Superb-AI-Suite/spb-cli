import unittest
import uuid
from unittest.mock import patch, Mock

from spb.labels import Label
from spb.labels.manager import LabelManager

class LabelManagerTest(unittest.TestCase):
    def setUp(self):
        pass

    @patch('spb.core.session.requests.post')
    def test_get_labels_with_right_params(self, mock_response):
        id = uuid.uuid4()
        project_id = uuid.uuid4()

        response = mock_response.return_value
        response.status_code = 200
        response.json.return_value = {
            'data':{
                'labels': {
                    'count': 100,
                    'edges': [{
                        'id': id,
                        'projectId': project_id
                    }]
                }
            }
        }

        manager = LabelManager()
        count, labels = manager.get_labels(project_id, page = 0, page_size = 10)

        self.assertEqual(count, 100)
        self.assertEqual(len(labels), 1)
        label = labels[0]
        self.assertEqual(label.id, id)
        self.assertEqual(label.project_id, project_id)

    @patch('spb.core.session.requests.post')
    def test_get_0_labels_with_right_params(self, mock_response):
        response = mock_response.return_value
        response.status_code = 200
        response.json.return_value = {
            'data': {
                'labels': {
                    'count': 0,
                    'edges': []
                }
            }
        }

        manager = LabelManager()
        count, labels = manager.get_labels(project_id=uuid.uuid4(), page = 0, page_size = 10)
        self.assertEqual(count, 0)
        self.assertEqual(len(labels), 0)

    @patch('spb.core.session.requests.post')
    def test_get_labels_count(self, mock_response):
        response = mock_response.return_value
        response.status_code = 200
        response.json.return_value = {'data':{'labels': {'count': 3}}}
        manager = LabelManager()
        count = manager.get_labels_count(project_id="29e6f25e-ac75-4882-9025-6ff73fd94cb1")

        self.assertEqual(count, 3)

    @patch('spb.core.session.requests.post')
    def test_get_label_detail_with_right_params(self, mock_response):
        response = mock_response.return_value
        response.status_code = 200
        response.json.return_value = {
            "data": {
                "labels": {
                    "count": 1,
                    "edges": [
                        {
                        "id": "29e6f25e-ac75-4882-9025-6ff73fd94cb1",
                        "dataset": "dfdf",
                        "dataKey": "Untitled.png",
                        "tags": [
                            {
                            "id": "2566992b-78a0-4ea0-9677-6811677d5e45",
                            "name": "A"
                            }
                        ],
                        "result": {
                            "objects": [
                            {
                                "id": 1,
                                "class": "person",
                                "shape": {
                                "box": {
                                    "x": 67.07317073170731,
                                    "y": 52.92682926829268,
                                    "width": 53.04878048780488,
                                    "height": 202.9268292682927
                                }
                                },
                                "properties": [
                                {
                                    "name": "abc",
                                    "value": "a"
                                }
                                ]
                            }
                            ],
                            "categorization": {
                            "value": []
                            }
                        },
                        "info_read_presigned_url": None,
                        "info_write_presigned_url": None
                        }
                    ]
                }
            }
        }

        label = Label(id=uuid.uuid4(), project_id=uuid.uuid4())
        manager = LabelManager()
        manager.get_label(project_id = label.project_id, id = label.id)

    @patch('spb.core.session.requests.post')
    def test_update_label(self, mock_response):
        response = mock_response.return_value
        response.status_code = 200
        response.json.return_value = {
            "data": {
                "updateLabels": {
                    "id": "29e6f25e-ac75-4882-9025-6ff73fd94cb1",
                    "projectId": "b2a7205f-4f2a-4eb2-b845-3ed6af9a9fc5",
                    "tags": [
                        {
                            "id": "2566992b-78a0-4ea0-9677-6811677d5e45",
                            "name": "A"
                        }
                    ],
                    "status": "SUBMITTED",
                    "stats": [
                        {
                            "name": "person",
                            "count": 1
                        }
                    ],
                    "workAssignee": "mscha@superb-ai.com",
                    "labelType": "MAIN_LABEL",
                    "relatedLabelMethod": "",
                    "consensusStatus": "",
                    "consistencyScore": 0,
                    "dataId": "90722177-24f1-469f-9372-bb180f2a8c5e",
                    "dataset": "dfdf",
                    "dataKey": "Untitled.png",
                    "dataUrl": "https://suite-asset.dev.superb-ai.com/apne2/tenants/pingu/assets/90722177-24f1-469f-9372-bb180f2a8c5e/image.png?Expires=1618384778&Signature=DEBpBduQI83HdfW6rouMxZiF73QvKp3teIpsvwcPvJGlSomN8GxiyOiTVE5R-5piJVhMCzbrAc~kbPFGgkciBceQEJOGMGxRnxlL4esAyMYzy28jETDwQpeXxHb5FYsYVe3YfRABaz8B2OOV1r2KElxW3NntEEc~6kcmbRPXKswZRFiXvYm1QPgAnUuaDHSzRBS8XKhB-jLhGFHfIzrrn47bazp1~aJIVfMRqgH8-7xhvVeEB65ijLuSmELQqg-S~pEmtfXQKeQ0z62Rlgn9IDkNiTo1gZf~r5kx0Wgf-yNyoyII2kiGvkRB8FqRuevU7hHsjk5B9fGj12sJRbm2lw__&Key-Pair-Id=APKAIBKPXKPWUNCICOBA",
                    "result": {
                        "objects": [
                            {
                                "id": 1,
                                "class": "person",
                                "shape": {
                                    "box": {
                                        "x": 67.07317073170731,
                                        "y": 52.92682926829268,
                                        "width": 53.04878048780488,
                                        "height": 202.9268292682927
                                    }
                                },
                                "properties": [
                                    {
                                        "name": "abc",
                                        "value": "a"
                                    }
                                ]
                            }
                        ],
                        "categorization": {
                            "value": []
                        }
                    },
                    "createdBy": "mscha@superb-ai.com",
                    "createdAt": "2020-04-23T03:14:08.222649Z",
                    "lastUpdatedBy": "system@superb-ai.com",
                    "lastUpdatedAt": "2021-04-14T06:19:38.486464Z",
                    "info_read_presigned_url": None,
                    "info_write_presigned_url": None
                }
            }
        }

        manager = LabelManager()
        # update_label(self, project_id:uuid.UUID, id:uuid.UUID, result:dict, tags:list=[], **kwargs)
        label = Label(
            project_id = "b2a7205f-4f2a-4eb2-b845-3ed6af9a9fc5",
            id = "29e6f25e-ac75-4882-9025-6ff73fd94cb1",
            result = {
                "objects": [
                    {
                    "id": 1,
                    "class": "person",
                    "shape": {
                            "box": {
                            "x": 67.07317073170731,
                            "y": 52.92682926829268,
                            "width": 53.04878048780488,
                            "height": 202.9268292682927
                        }
                    },
                    "properties": [
                        {
                            "name": "abc",
                            "value": "a"
                        }
                    ]
                    }
                ],
                "categorization": {"value": []}
            },
            tags = [{"name": "A"}]
        )
        manager.update_label(label=label)

