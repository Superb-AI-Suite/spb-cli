import unittest
import uuid

from spb.core.models.types import ID, JsonObject, String, Int, Float, Boolean, List, PlainObject, PlainObjectList
from spb.core import Model
from spb.core.models.attrs import AttributeModel
from spb.exceptions import DoesNotExistsAttribute, AttributeTypeException


class WrongAttribute():
    pass


class TempAttributeInTempAttribute(AttributeModel):
    def __init__(self, *args, **kwargs):
        self.items = ['value_1', 'value_2']


class TempAttribute(AttributeModel):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.count = kwargs['count'] if 'count' in kwargs else None
        self.items = [TempAttributeInTempAttribute()]


class DummyModel(Model):
    id = ID(property_name='id', immutable=True, filterable=True)

    stats = PlainObjectList(property_name='stats', express=TempAttribute)

    dataset = String(property_name='dataset', default='test dataset')
    label_count = Int(property_name='labelCount', default=1)
    submit_rate = Float(property_name='submitRate', default=0.0)
    is_ended = Boolean(property_name='isEnded', default=False)


class ModelTest(unittest.TestCase):
    def test_init_model(self):
        instance_id = uuid.uuid4()
        instance = DummyModel(id=instance_id, stats=[TempAttribute()])
        self.assertTrue(isinstance(instance, Model))
        self.assertEqual(instance.id, instance_id)
        self.assertEqual(instance.dataset, 'test dataset')
        self.assertEqual(instance.label_count, 1)
        self.assertEqual(instance.submit_rate, 0.0)
        self.assertEqual(instance.is_ended, False)

    def test_init_model_with_response_dict(self):
        response_dict = {
            'labelCount': 1,
            'submitRate': 1.0,
            'isEnded': False
        }
        instance = DummyModel(**response_dict)
        self.assertEqual(instance.label_count, 1)
        self.assertEqual(instance.submit_rate, 1.0)
        self.assertEqual(instance.is_ended, False)

    def test_init_model_raises_AttributeTypeExcpeiton_if_unusable_params(self):
        invalid_id = uuid.uuid5(uuid.NAMESPACE_DNS, 'superb-ai.com')
        with self.assertRaises(AttributeTypeException):
            DummyModel(id=invalid_id)

        invalid_stats = [WrongAttribute()]
        with self.assertRaises(AttributeTypeException):
            DummyModel(stats=invalid_stats)

    def test_can_get_attribute_types(self):
        instance = DummyModel()
        self.assertTrue(isinstance(instance.get_attribute_type('id'), ID))
        self.assertTrue(isinstance(instance.get_attribute_type('stats'), PlainObjectList))
        self.assertTrue(isinstance(instance.get_attribute_type('dataset'), String))
        self.assertTrue(isinstance(instance.get_attribute_type('label_count'), Int))
        self.assertTrue(isinstance(instance.get_attribute_type('submit_rate'), Float))
        self.assertTrue(isinstance(instance.get_attribute_type('is_ended'), Boolean))

    def test_get_attribute_types_raises_DoesNotExistsAttribute_if_wrong_attribute_name(self):
        instance = DummyModel()
        with self.assertRaises(DoesNotExistsAttribute):
            instance.get_attribute_type('wrong_attribute')

    def test_change_attribute_values(self):
        instance = DummyModel()
        new_instance_id = uuid.uuid4()
        new_stats = [TempAttribute(), TempAttribute()]
        new_dataset = 'new dataset'
        new_label_count = 1000
        new_submit_rate = 1.0
        new_is_ended = True

        instance.id = new_instance_id
        instance.stats = new_stats
        instance.dataset = new_dataset
        instance.label_count = new_label_count
        instance.submit_rate = new_submit_rate
        instance.is_ended = new_is_ended
        self.assertEqual(instance.id, new_instance_id)
        self.assertEqual(instance.stats, new_stats)
        self.assertEqual(instance.dataset, new_dataset)
        self.assertEqual(instance.label_count, new_label_count)
        self.assertEqual(instance.submit_rate, new_submit_rate)
        self.assertEqual(instance.is_ended, new_is_ended)

    def test_change_attribute_value_raises_AttributeTypeException_if_wrong_attribute_value(self):
        instance = DummyModel()
        with self.assertRaises(AttributeTypeException):
            instance.id = 'WRONG_UUID_STRING'
        with self.assertRaises(AttributeTypeException):
            instance.dataset = True
        with self.assertRaises(AttributeTypeException):
            instance.label_count = '1000'
        with self.assertRaises(AttributeTypeException):
            instance.submit_rate = '100.0'
        with self.assertRaises(AttributeTypeException):
            instance.stats = [DummyModel()]
