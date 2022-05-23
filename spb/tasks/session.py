import os

from spb.core.session import BaseSession
from spb.exceptions import APIFormatException

from .task import Task

class Session(BaseSession):
    endpoint = os.getenv("SPB_APP_API_ENDPOINT", "https://api.superb-ai.com") + '/v2/graphql'

    def extract_task_list(self, response, query_id):
        response_json = response.json()
        self._check_errors(response_json)

        count = response_json['data'][query_id]['count']
        data = response_json['data'][query_id]['results']
        
        result = [Task(**item) for item in data]
        return (count, result)

    def extract_task(self, response, query_id):
        response_json = response.json()
        self._check_errors(response_json)
        data = response_json['data'][query_id]
        return Task(**data)


    def extract_task_progress(self, response, query_id):
        response_json = response.json()
        self._check_errors(response_json)
        data = response_json['data'][query_id]
        return Task(**data)


    def extract_autolabel_task(self, response, query_id):
        response_json = response.json()
        self._check_errors(response_json)
        data = response_json['data'][query_id]
        return Task(**data)


    def _check_errors(self, response_json):
        if 'errors' in response_json:
            errors = response_json['errors']
            raise APIFormatException(message=errors[0]['message'])