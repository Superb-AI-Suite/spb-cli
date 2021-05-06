import uuid
import unittest

from spb.labels.manager import LabelManager
from spb.labels import Label
from spb.labels.label import Tags, Stats
from spb.exceptions import AttributeTypeException


class LabelTest(unittest.TestCase):
    def setUp(self):
        self.attrs = {
            'id': uuid.uuid4(),
            'project_id': uuid.uuid4(),
            'tags': [Tags(name='TAG1'), Tags(name='TAG2')],
            'status': '',
            'stats': [Stats(name='STATS1', count=10)],
            'data_id': uuid.uuid4(),
            'dataset': 'TEST_DATASET_NAME',
            # [dataUrl] Init with property name -> To use response to model instance
            'dataUrl': 'https://superb-ai.com',
            'data': 'NOT YET IMPLEMENTED',
            'result': {'result': []},

            'work_assignee': 'mjlee@superb-ai.com',
            'label_type': '',
            'related_label_method': '',
            'consensus_status': '',
            'consistency_score': 0.0
        }
        self.label_manager = LabelManager()

    def test_init_label_instance(self):
        label = Label()
        self.assertTrue(isinstance(label, Label))

    def test_init_label_with_attrs(self):
        label = Label(**self.attrs)

        self.assertEqual(label.id, self.attrs['id'])
        self.assertEqual(label.project_id, self.attrs['project_id'])
        self.assertEqual(label.tags, self.attrs['tags'])
        self.assertEqual(label.stats, self.attrs['stats'])
        self.assertEqual(label.data_id, self.attrs['data_id'])
        self.assertEqual(label.dataset, self.attrs['dataset'])
        self.assertEqual(label.data_url, self.attrs['dataUrl'])
        self.assertEqual(label.result, self.attrs['result'])

        with self.assertRaises(AttributeError):
            self.assertEqual(label.data, self.attrs['data'])

    def test_init_label_raises_Exception_with_wrong_attribute(self):
        with self.assertRaises(AttributeTypeException):
            label = Label(id='WRONG_LABEL_ID')

        with self.assertRaises(AttributeTypeException):
            label = Label(project_id= 1234)

        with self.assertRaises(AttributeTypeException):
            label = Label(tags=Tags(name='TAG1'))


        class DummyClass():
            pass

        with self.assertRaises(AttributeTypeException):
            label = Label(stats=[DummyClass()])

        with self.assertRaises(AttributeTypeException):
            label = Label(result={
                'RIGHT_KEY': DummyClass()
            })