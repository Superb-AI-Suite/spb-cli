import unittest
from unittest.mock import patch, Mock

import spb.sdk
from spb.labels.session import Session
from .mocks import MOCK_PROJECT


class TestSDK(unittest.TestCase):
    def setUp(self):
        with patch.object(spb.sdk.Client, 'get_project') as mock_method:
            mock_method.return_value = MOCK_PROJECT
            self.client = spb.sdk.Client(project_name='PROJECT_NAME_TO_TEST')

    def test_init_sdk(self):
        self.assertTrue(self.client, spb.sdk.Client)
        self.assertEqual(self.client.get_project_name(), 'PROJECT_NAME_TO_TEST')

    def test_project_data(self):
        with patch.object(Session, 'execute') as mock_method:
            mock_method.json.return_value = {'data': {'labels': {'count': 10}}}
            self.assertTrue(self.client.get_num_data(), int)

    # def test_get_data_page_about_image_default(self):
    #     client = self.client

    #     # Iterate all data in dataset
    #     def get_data(dataset, page_size=10):
    #         num_data = client.get_num_data(dataset=dataset)
    #         self.assertTrue(isinstance(num_data, int))
    #         num_page = (num_data + page_size - 1) // page_size
    #         for page_idx in range(num_page):
    #             for data_handler in client.get_data_page(page_idx=page_idx, page_size=page_size, dataset=dataset):
    #                 yield data_handler

    #     uploaded_data = {}
    #     for data_handler in get_data('20'):
    #         dataset = data_handler.get_dataset_name()
    #         data_key = data_handler.get_key()
    #         uploaded_data[(dataset, data_key)] = data_handler
    #     print(list(uploaded_data.keys()))
