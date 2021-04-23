import uuid
import json
import logging

from spb.core.manager import BaseManager
from .session import Session
from .query import Query
from .label import Label
from spb.exceptions import ParameterException

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

        self.query.response_attrs.extend(label.get_property_names())
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
        try:
            query, values = self.query.build_query()
            response = self.session.execute(query, values)
        except Exception as e:
            raise e

        count, data = self._get_count_and_data_from_response(response, 'labels')
        labels = []
        for item in data:
            labels.append(Label(**item))
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
        self.query.required_attrs.extend(label.get_property_names(include=['projectId']))
        self.query.response_attrs.extend(label.get_property_names())
        try:
            query, values = self.query.build_query()
            response = self.session.execute(query, values)
        except Exception as e:
            raise e

        count, data = self._get_count_and_data_from_response(response, 'labels')
        label = None
        if count > 0:
            item = data[0]
            label = Label(**item)

        return label

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
        count, data = self._get_count_and_data_from_response(response, 'relatedLabels')
        labels = []
        for item in data:
            labels.append(Label(**item))

        return count, labels

    def create_label(self):
        #Request export to civet
        # boto3
        pass

    def update_label(self, project_id:uuid.UUID, id:uuid.UUID, result:dict, tags:list=None, **kwargs):
        self.query.query_id = 'updateLabels'
        label = Label(
            project_id = project_id,
            id = id,
            result = result,
            tags = tags,
            **kwargs
        )
        self.query.attrs.update(label.get_attributes_map(include=['id', 'project_id', 'result', 'tags']))
        self.query.required_attrs.extend(label.get_property_names(include=['id', 'project_id']))
        self.query.response_attrs.extend(label.get_property_names())
        try:
            query, values = self.query.build_mutation_query()
            response = self.session.execute(query, values)
        except Exception as e:
            raise e

        
        response_json = response.json()
        data = response_json['data']['updateLabels']
        label = Label(**data)

        return label

    def update_label_tags(self, project_id:uuid.UUID, id:uuid.UUID, tags:list, **kwargs):
        return self.update_label(project_id=project_id, id=id, result=None, tags=tags, **kwargs)

    def delete_label(self):
        pass

    def _get_count_and_data_from_response(self, response, query_id):
        response_json = response.json()
        count = response_json['data'][query_id]['count']
        data = response_json['data'][query_id]['edges']
        return (count, data)
