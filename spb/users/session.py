import os

from spb.core.session import BaseSession
from spb.exceptions import APIFormatException

from .user import User


class Session(BaseSession):
    endpoint = os.getenv("SPB_APP_API_ENDPOINT", "https://api.superb-ai.com") + '/v3/graphql'

    def extract_project_users(self, response, query_id):
        response_json = response.json()
        self._check_errors(response_json)

        count = response_json['data'][query_id]['count']
        data = response_json['data'][query_id]['edges']
        result = [User(**item) for item in data]
        return (count, result)

    def _check_errors(self, response_json):
        if 'errors' in response_json:
            errors = response_json['errors']
            raise APIFormatException(message=errors[0]['message'])
