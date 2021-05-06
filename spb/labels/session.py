import os
import json

from spb.core.session import BaseSession
from spb.exceptions import APIFormatException


class Session(BaseSession):
    endpoint = os.getenv("SPB_APP_API_ENDPOINT", "https://api.superb-ai.com/v2/graphql")

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

    def _check_errors(self, response_json):
        if 'errors' in response_json:
            errors = response_json['errors']
            raise APIFormatException(message=errors[0]['message'])
