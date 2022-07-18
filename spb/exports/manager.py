import logging
import requests
import uuid
from typing import Optional

from spb.core.manager import BaseManager
from .session import Session
from .query import Query
from .export import Export
from spb.utils.utils import requests_retry_session
from spb.exceptions import APIFormatException, APIUnknownException

logger = logging.getLogger()


class ExportManager(BaseManager):
    def __init__(self, team_name=None, access_key=None):
        self.session = Session(
            team_name = team_name,
            access_key = access_key
        )
        self.query = Query()
    
    def get_exports(self, project_id:uuid.UUID, page:int=1, page_size:int=10):
        self.query.query_id = 'exports'
        export = Export(
            project_id = project_id
        )
        query_attrs = export.get_attributes_map(include=['project_id'])
        self.query.attrs.update(query_attrs)
        self.query.page = page
        self.query.page_size = page_size
        self.query.response_attrs.extend(export.get_property_names(exclude=['project_id']))
        self.query.required_attrs.extend(export.get_property_names(include=['project_id']))
        try:
            query, values = self.query.build_query()
            response = self.session.execute(query, values)
            _, histories = self.session.get_count_and_data_from_response(response)
            return histories
        except APIFormatException as e:
            raise e
        except Exception as e:
            raise APIUnknownException(str(e))

    def get_export(self, project_id:uuid.UUID, id: Optional[uuid.UUID] = None, name: Optional[str] = None):
        self.query.query_id = 'export'
        if id:
            export = Export(
                project_id = project_id,
                id = id
            )
            query_attrs = export.get_attributes_map(include=['project_id', 'id'])
            self.query.required_attrs.extend(export.get_property_names(include=['project_id', 'id']))
        elif name:
            export = Export(
                project_id = project_id,
                name = name
            )
            query_attrs = export.get_attributes_map(include=['project_id', 'name'])
            self.query.required_attrs.extend(export.get_property_names(include=['project_id', 'name']))
        self.query.attrs.update(query_attrs)
        self.query.response_attrs.extend(export.get_property_names(exclude=['project_id']))
        try:
            query, values = self.query.build_query()
            response = self.session.execute(query, values)
            return self.session.get_data_from_response(response)
        except Exception as e:
            raise APIUnknownException()
