import unittest
import json
from uuid import UUID
from unittest.mock import patch, Mock

import spb.sdk
from .mocks import MOCK_PROJECT, MOCK_LABEL, MOCK_DATA_HANDLE
from spb.labels.session import Session
from spb.labels.serializer import LabelInfoBuildParams
from spb.labels.label import WorkappType


class TestImageDataHandler(unittest.TestCase):

    @patch('spb.sdk.Client.get_project')
    def setUp(self, mock):
        # Settings about mock data
        mock.return_value = MOCK_PROJECT

        self.client = spb.sdk.Client(project_name='PROJECT_NAME_TO_TEST')

        with patch.object(spb.sdk.Client, 'get_data_page') as mock_method:
            mock_method.return_value = iter([MOCK_DATA_HANDLE])
            self.data = next(self.client.get_data_page(page_idx=0, page_size=1, dataset='DATASET_NAME_TO_TEST'))

    def test_data_handler(self):
        data = self.data._data
        try:
            UUID(str(data.id), version=4)
            UUID(str(data.project_id), version=4)
        except ValueError:
            self.fail('Label id type attributes have to be UUIDv4 string')

        # Image dataset and data key
        self.assertEqual(type(self.data.get_dataset_name()), str)
        self.assertEqual(type(self.data.get_key()), str)

        # Workapp Type Test
        self.assertTrue(data.workapp in [WorkappType.IMAGE_DEFAULT.value, WorkappType.IMAGE_SIESTA.value])

        # Image URL of data
        self.assertEqual(type(self.data.get_image_url()), str)
        self.assertTrue('https://suite-asset.dev.superb-ai.com' in self.data.get_image_url() )

        self.assertTrue(self.data.get_status() in ['SUBMITTED', 'WORKING', 'SKIPPED'])
        self.assertTrue(data.label_type in ['MAIN_LABEL', 'RELATED_LABEL'])

        if data.workapp == WorkappType.IMAGE_SIESTA.value:
            # If user use new image work app
            self.assertEqual(type(data.info_write_presigned_url), str)
            self.assertEqual(type(data.info_read_presigned_url), str)
            self.assertTrue('https://suite-civet-asset-dev-s3' in data.info_write_presigned_url)
            self.assertTrue('https://suite-civet-asset-dev-s3' in data.info_read_presigned_url)
        else:
            self.assertTrue(data.info_write_presigned_url is None)
            self.assertTrue(data.info_read_presigned_url is None)

    def test_get_result_with_data_handler(self):
        result = self.data._data.result
        if result is not None:
            self.assertTrue('objects' in result)
            self.assertTrue('categories' in result)

    def test_get_objects_with_data_handler(self):
        handler = self.data
        objects = handler.get_object_labels()
        if len(objects) > 0:
            for object in objects:
                self.assertTrue('id' in object.keys())
                self.assertTrue('class_name' in object.keys())
                self.assertTrue('properties' in object.keys())
                self.assertTrue('annotation' in object.keys())

    def test_add_object_label(self):
        handler = self.data
        prev_objects = handler.get_object_labels()
        o = prev_objects[0]
        handler.add_object_label(class_name=o['class_name'], annotation=o['annotation'])
        self.assertTrue(handler.get_object_labels(), [o, o])

    def test_get_categories(self):
        handler = self.data
        prev_categories = handler.get_category_labels()
        properties = [
            {'name':'Box', 'value':'AA'}
        ]
        handler.set_category_labels(properties=properties)
        self.assertEqual(
            {'properties': properties},
            handler.get_category_labels()
        )

    # def test_update_label_with_data_handler(self):
    #     label = MOCK_LABEL
    #     data = self.data._data
    #     prev_result = data.result
    #     self.data.set_object_labels(data.result['objects'])
    #     current_result = self.data._data.result
    #     self.assertEqual(prev_result, current_result)

