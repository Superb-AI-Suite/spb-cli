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
            'status': 'SUBMITTED',
            'stats': [Stats(name='STATS1', count=10)],
            'data_id': uuid.uuid4(),
            'dataset': 'TEST_DATASET_NAME',
            # [dataUrl] Init with property name -> To use response to model instance
            'dataUrl': 'https://superb-ai.com',
            'data': 'NOT YET IMPLEMENTED',
            'result': {'result': []},

            'work_assignee': 'labeler@superb-ai.com',
            'reviewer': 'reviewer@superb-ai.com',
            'review_round': 1,
            'last_review_action': 'APPROVE',
            'label_type': '',
            'related_label_method': '',
            'consensus_status': '',
            'consistency_score': 0.0,
            'created_by': 'owner@superb-ai.com',
            'created_at': '2020-04-23T03:14:08.222649Z',
            'last_updated_by': 'admin@superb-ai.com',
            'last_updated_at': '2021-04-14T06:19:38.486464Z',
            'info_last_updated_by': 'admin@superb-ai.com',
            'last_reviewed_at':'2021-04-14T06:19:38.486464Z',
            'info_read_presigned_url': None,
            'info_write_presigned_url': None
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
        self.assertEqual(label.work_assignee, self.attrs['work_assignee'])
        self.assertEqual(label.reviewer, self.attrs['reviewer'])
        self.assertEqual(label.review_round, self.attrs['review_round'])
        self.assertEqual(label.label_type, self.attrs['label_type'])
        self.assertEqual(label.related_label_method, self.attrs['related_label_method'])
        self.assertEqual(label.consensus_status, self.attrs['consensus_status'])
        self.assertEqual(label.consistency_score, self.attrs['consistency_score'])
        self.assertEqual(label.created_by, self.attrs['created_by'])
        self.assertEqual(label.created_at, self.attrs['created_at'])
        self.assertEqual(label.last_updated_by, self.attrs['last_updated_by'])
        self.assertEqual(label.last_updated_at, self.attrs['last_updated_at'])
        self.assertEqual(label.info_last_updated_by, self.attrs['info_last_updated_by'])
        self.assertEqual(label.last_reviewed_at, self.attrs['last_reviewed_at'])
        self.assertEqual(label.info_read_presigned_url, self.attrs['info_read_presigned_url'])
        self.assertEqual(label.info_write_presigned_url, self.attrs['info_write_presigned_url'])

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