import os

from spb.core.session import BaseSession
from spb.exceptions import APIFormatException
from spb.exports.export import Export


class Session(BaseSession):
    endpoint = os.getenv('SPB_APP_API_ENDPOINT', "https://api.superb-ai.com") + '/v2/graphql'

    def get_count_and_data_from_response(self, response):
        response_json = response.json()
        self._check_errors(response_json)
        count = response_json['data']['exports']['count']
        data = response_json['data']['exports']['edges']
        histories = [Export(**item) for item in data]
        return (count, histories)

    def get_data_from_response(self, response):
        response_json = response.json()
        self._check_errors(response_json)
        data = response_json['data']['export']
        return Export(**data)

    def _check_errors(self, response_json):
        if 'errors' in response_json:
            errors = response_json['errors']
            raise APIFormatException(message=errors[0]['message'])