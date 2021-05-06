import uuid
import json
from enum import Enum

from spb.core import Model
from spb.core.models.attrs import AttributeModel
from spb.core.models.types import JsonObject, String, ID, Int, PlainObject, PlainObjectList, Float


class WorkappType(Enum):
    IMAGE_DEFAULT = 'IMAGE_DEFAULT'
    IMAGE_SIESTA = 'IMAGE_SIESTA'

class Stats(AttributeModel):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.count = kwargs['count'] if 'count' in kwargs else None


class Tags(AttributeModel):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name'] if 'name' in kwargs else None


class Label(Model):
    id = ID(property_name='id', default_value=uuid.uuid4())
    project_id = ID(property_name='projectId')
    tags = PlainObjectList(property_name='tags', express=Tags)

    #basic info
    status = String(property_name='status')
    stats = PlainObjectList(property_name='stats', express=Stats)
    work_assignee = String(property_name='workAssignee')
    label_type = String(property_name='labelType')
    workapp = String(property_name='workapp', default_value='image-siesta')
    related_label_method = String(property_name='relatedLabelMethod')
    consensus_status = String(property_name='consensusStatus')
    consistency_score = Float(property_name='consistencyScore')

    #For assets
    data_id = ID(property_name='dataId')
    dataset = String(property_name='dataset')
    data_key = String(property_name='dataKey')
    data_url = String(property_name='dataUrl')

    result = JsonObject(property_name='result')
    info_read_presigned_url = String(property_name='infoReadPresignedUrl', default_value=None)
    info_write_presigned_url = String(property_name='infoWritePresignedUrl', default_value=None)


    created_by = String(property_name='createdBy')
    created_at = String(property_name='createdAt')
    last_updated_by = String(property_name='lastUpdatedBy')
    last_updated_at = String(property_name='lastUpdatedAt')

    def to_json(self, include_project=True, include_data=True):
        label = {
            'id': str(self.id),
            'status': self.status,
            'work_assignee': self.work_assignee,
            'workapp': self.workapp,
            'consistency_score': self.consistency_score,
            'stats': [Stats.get_data(stat) for stat in self.stats] if self.stats is not None else None,
            'tags': [Tags.get_data(tag) for tag in self.tags] if self.tags is not None else None,
            'result': self.result,
            'created_by': self.created_by,
            'created_at': self.created_at,
            'last_updated_by': self.last_updated_by,
            'last_updated_at': self.last_updated_at
        }
        if include_project:
            label.update({
                'project_id': str(self.project_id),
            })
        if include_data:
            label.update({
                'data_id': str(self.data_id),
                'dataset': self.dataset,
                'data_key': self.data_key,
            })
        return label

