import uuid
import json
import logging
import requests

from spb.libs.phy_credit.phy_credit.imageV2 import LabelInfo
from spb.labels.serializer import LabelInfoBuildParams
from spb.core.manager import BaseManager
from .session import Session
from .query import Query
from .label import Label, WorkappType
from spb.exceptions import ParameterException, APIException

logger = logging.getLogger()


class LabelManager(BaseManager):

    def __init__(self):
        self.session = Session()
        self.query = Query()

    def get_labels_count(self, project_id:uuid.UUID, dataset=None, data_key=None, tags:list=[], label_type=None):
        self.query.query_id = 'labels'
        label = Label(
            project_id = project_id,
            dataset = dataset,
            data_key = data_key,
            tags = tags,
            label_type = label_type
        )
        query_attrs = label.get_attributes_map(include=['project_id'])
        if dataset is not None:
            query_attrs[Label.dataset] = label.dataset
        if data_key is not None:
            query_attrs[Label.data_key] = label.data_key
        if len(tags) != 0:
            query_attrs[Label.tags] = label.tags
        if label_type is not None:
            query_attrs[Label.label_type] = label_type


        self.query.attrs.update(query_attrs)
        self.query.page = 1
        self.query.page_size = 1

        self.query.response_attrs.extend(label.get_property_names(include=['id', 'project_id']))
        self.query.required_attrs.extend(label.get_property_names(include=['project_id']))
        try:
            query, values = self.query.build_label_count_query()
            response = self.session.execute(query, values)
        except Exception as e:
            raise e

        return response.json()['data'].get('labels', {'count': None})['count']

    def get_labels(self, project_id:uuid.UUID, page:int=1, page_size:int=10, dataset=None, data_key=None, tags:list=[], label_type=None):
        self.query.query_id = 'labels'
        label = Label(
            project_id = project_id,
            dataset = dataset,
            data_key = data_key,
            tags = tags,
            label_type = label_type
        )
        query_attrs = label.get_attributes_map(include=['project_id'])

        if dataset is not None:
            query_attrs[Label.dataset] = dataset
        if data_key is not None:
            query_attrs[Label.data_key] = data_key
        if len(tags) != 0:
            query_attrs[Label.tags] = tags
        if label_type is not None:
            query_attrs[Label.label_type] = label_type

        self.query.attrs.update(query_attrs)
        self.query.page = page
        self.query.page_size = page_size

        self.query.response_attrs.extend(label.get_property_names())
        self.query.required_attrs.extend(label.get_property_names(include=['project_id']))
        query, values = self.query.build_query()
        response = self.session.execute(query, values)

        count, data = self.session.get_count_and_data_from_response(response, 'labels')
        labels = []
        for item in data:
            label = Label(**item)
            label = self.get_label_info_from_url(label)
            labels.append(label)
        return count, labels

    def get_label(self, project_id:uuid.UUID, id:uuid.UUID):
        self.query.query_id = 'labels'
        label = Label(
            project_id = project_id,
            id = id
        )
        self.query.attrs.update(label.get_attributes_map(include=['id', 'project_id']))
        self.query.page = 1
        self.query.page_size = 1
        self.query.required_attrs.extend(label.get_property_names(include=['project_id']))
        self.query.response_attrs.extend(label.get_property_names())
        try:
            query, values = self.query.build_query()
            response = self.session.execute(query, values)
        except Exception as e:
            raise e

        count, data = self.session.get_count_and_data_from_response(response, 'labels')
        label = None
        if count > 0:
            item = data[0]
            label = Label(**item)
            label = self.get_label_info_from_url(label)

        return label

    def get_label_info_from_url(self, label: Label = None):
        if label.workapp != WorkappType.IMAGE_SIESTA.value:
            return label
        elif label.info_read_presigned_url is None:
            return label

        try:
            read_response = requests.get(label.info_read_presigned_url)
            if read_response.status_code == requests.codes.not_found:
                label.result = None
                return label
            read_response.raise_for_status()
            label.result = read_response.json().get('result', {})
            return label
        except:
            raise APIException(f'[Label Manager] Label result cannot be described from url : {label.info_read_presigned_url}')

    def set_info_with_url(self, label_info: dict, label: Label = None):
        if label.info_write_presigned_url is None:
            return label
        request_result = requests.put(label.info_write_presigned_url, data=json.dumps(label_info))
        request_result.raise_for_status()

    def get_related_labels_by_label(self, project_id:uuid.UUID, label_id:uuid.UUID, page:int=1, page_size:int=10):
        self.query.query_id = 'relatedLabels'
        label = Label(
            project_id = project_id,
            id = label_id
        )

        self.query.attrs.update(label.get_attributes_map(include=['id', 'project_id']))
        self.query.page = page
        self.query.page_size = page_size

        self.query.response_attrs.extend(label.get_property_names())
        self.query.required_attrs.extend(label.get_property_names(include=['project_id']))
        try:
            query, values = self.query.build_query()
            response = self.session.execute(query, values)
        except Exception as e:
            raise e
        count, data = self.session.get_count_and_data_from_response(response, 'relatedLabels')
        labels = []
        for item in data:
            label = Label(**item)
            label = self.get_label_info_from_url(label)
            labels.append(label)
        return count, labels

    def create_label(self):
        #Request export to civet
        # boto3
        pass

    def update_label(self, label: Label, info_build_params: LabelInfoBuildParams = None):
        query_id = 'updateLabels'
        self.query.query_id = query_id

        attribute_maps = label.get_attributes_map(include=['id', 'project_id', 'tags', 'workapp'])
        if label.workapp == WorkappType.IMAGE_SIESTA.value:
            if info_build_params is not None:
                label_info = info_build_params.build_info()
            else:
                label_info = label.result
            result = {'tags': label_info.get('tags', None)}
        else:
            result = label.result
        attribute_maps.update({
            label.get_attribute_type('result'): result
        })
        self.query.attrs.update(attribute_maps)
        self.query.required_attrs.extend(label.get_property_names(include=['id', 'project_id', 'workapp']))
        self.query.response_attrs.extend(label.get_property_names())
        try:
            query, values = self.query.build_mutation_query()
            response = self.session.execute(query, values)
        except Exception as e:
            raise e

        data = self.session.get_data_from_mutation(response, query_id)
        updated_label = Label(**data)

        if label.workapp == WorkappType.IMAGE_SIESTA.value:
            label.info_write_presigned_url = updated_label.info_write_presigned_url
            self.set_info_with_url(label_info = label_info, label = label)
            updated_label.result = label_info.get('result', None)

        return updated_label

    def delete_label(self):
        pass

