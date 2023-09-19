import os
import requests

from spb.core.session import BaseSession
from spb.exceptions import APIFormatException, APIException
from spb.utils.utils import requests_retry_session

from .label import Label


class Session(BaseSession):
    endpoint = os.getenv("SPB_APP_API_ENDPOINT", "https://api.superb-ai.com") + '/v2/graphql'
    def get_count_and_data_from_response(self, response, query_id):
        response_json = response.json()
        self._check_errors(response_json)

        count = response_json['data'][query_id]['count']
        data = response_json['data'][query_id]['edges']
        return (count, data)

    def get_data_from_mutation(self, response, query_id):
        response_json = response.json()
        self._check_errors(response_json)

        data = response_json['data'][query_id]
        return data

    def get_count_cursor_data_from_response(self, query_id: str, response):
        response_json = response.json()
        self._check_errors(response_json)

        count = response_json['data'][query_id]['count']
        data = response_json['data'][query_id]['edges']
        cursor = response_json['data'][query_id]['cursor']

        return (count, data, cursor)
    
    def build_label_from_response(self, query_id, response):
        response_json = response.json()
        self._check_errors(response_json)
        data = response_json['data'][query_id]
        label = Label(**data)
        label = self.get_label_info_from_url(label)
        return label

    def get_label_update_result(self, query_id: str, response):
        response_json = response.json()
        self._check_errors(response_json)
        return response_json['data'][query_id]['success']

    def _check_errors(self, response_json):
        if 'errors' in response_json:
            errors = response_json['errors']
            raise APIFormatException(message=errors[0]['message'])
        
    def get_label_info_from_url(self, label: Label = None):
        if label.info_read_presigned_url is None:
            return label

        try:
            with requests_retry_session() as session:
                read_response = session.get(label.info_read_presigned_url)
            if read_response.status_code == requests.codes.not_found:
                label.result = None
                return label
            read_response.raise_for_status()
            label.result = read_response.json().get("result", {})
            return label
        except:
            raise APIException(
                f"[Label Manager] Label result cannot be described from url : {label.info_read_presigned_url}"
            )
