import json
import requests
from spb.orm.type_base import Type
from spb.orm.json_type import JsonObject
from spb.orm import Model
from spb.orm import AttributeModel
from spb.orm import ListAttribute
from spb.orm.type import String, ID, Number, Object, List


class Stats(ListAttribute):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.count = kwargs['count'] if 'count' in kwargs else None

class Tags(ListAttribute):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name'] if 'name' in kwargs else None

class VideoLabel(Model):
    MODEL_UUID = '18545938-eae3-4627-a049-fe1464f9d85f'
    RESOURCE_NAME = 'video_labels'

    # id
    id = ID(property_name='id', immutable=True, filterable=True)
    project_id = ID(property_name='projectId', filterable=True)
    tags = Object(property_name='tags', express=Tags, filterable=True)

    # basic info
    status = String(property_name='status', immutable=True, filterable=True)
    stats = Object(property_name='stats', immutable=True, express=Stats)

    # For assets
    data_id = ID(property_name='dataId', immutable=True)
    dataset = String(property_name='dataset', immutable=True, filterable=True)
    data_key = String(property_name='dataKey', immutable=True, filterable=True)
    data_url = String(property_name='dataUrl', immutable=True)

    # info
    info_read_presigned_url = String(property_name='infoReadPresignedUrl', immutable=True)
    info_write_presigned_url = String(property_name='infoWritePresignedUrl', immutable=True)

    def toJson(self):
        try:
            response = requests.get(self.info_read_presigned_url)
            info_json = response.json()
            result = info_json['result']
        except:
            result = None
        return json.dumps({
            'id': self.id,
            'project_id': self.project_id,
            'status': self.status,
            'stats': [stat.get_datas(stat) for stat in self.stats] if self.stats is not None else None,
            'tags': [tag.get_datas(tag) for tag in self.tags] if self.tags is not None else None,
            'data_id': self.data_id,
            'dataset': self.dataset,
            'data_key': self.data_key,
            'result': result
        }, indent=4)

