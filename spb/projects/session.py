import os

from spb.core.session import BaseSession
from spb.exceptions import APIFormatException

from .project import Project, Tag


class Session(BaseSession):
    endpoint = (
        os.getenv("SPB_APP_API_ENDPOINT", "https://api.superb-ai.com")
        + "/v3/graphql"
    )

    def extract_project_list(self, response, query_id):
        response_json = response.json()
        self._check_errors(response_json)

        count = response_json["data"][query_id]["count"]
        data = response_json["data"][query_id]["edges"]

        result = [Project(**item) for item in data]

        return (count, result)

    def extract_project(self, response, query_id):
        response_json = response.json()
        self._check_errors(response_json)

        data = response_json["data"][query_id]
        return Project(**data)

    def get_result_from_response_project(self, response, query_id):
        response_json = response.json()
        self._check_errors(response_json)
        data = response_json["data"][query_id]
        return Project(**data)  # TODO check response

    def get_result_from_response(self, response, query_id):
        response_json = response.json()
        self._check_errors(response_json)
        data = response_json["data"][query_id]
        return data

    def extract_tags(self, response, query_id):
        response_json = response.json()
        self._check_errors(response_json)

        count = response_json['data'][query_id]['count']
        data = response_json['data'][query_id]['edges']

        return (count, [Tag(**item) for item in data])

    def _check_errors(self, response_json):
        if "errors" in response_json:
            errors = response_json["errors"]
            raise APIFormatException(message=errors[0]["message"])
