import os

from spb.assets.asset import Asset
from spb.core.session import BaseSession
from spb.exceptions import APIFormatException


class Session(BaseSession):
    endpoint = (
        os.getenv("SPB_APP_API_ENDPOINT", "https://api.superb-ai.com") + "/v2/graphql"
    )

    def get_cursor_based_data_from_response(self, response):
        response_json = response.json()
        self._check_errors(response_json)
        prev = None
        nxt = None
        count = response_json["data"]["assetsV2"]["count"]
        if "previous" in response_json["data"]["assetsV2"]:
            prev = response_json["data"]["assetsV2"]["previous"]
        if "next" in response_json["data"]["assetsV2"]:
            nxt = response_json["data"]["assetsV2"]["next"]
        prev = prev.encode("utf-8") if prev else None
        nxt = nxt.encode("utf-8") if nxt else None

        data = response_json["data"]["assetsV2"]["edges"]
        histories = [Asset(**item) for item in data]
        return (count, prev, nxt, histories)

    def get_data_from_response(self, response):
        response_json = response.json()
        self._check_errors(response_json)
        data = response_json["data"]["assetV2"]
        return Asset(**data)

    def get_url_from_response(self, response):
        response_json = response.json()
        self._check_errors(response_json)
        url = response_json["data"]["getAssetUrl"]["presignedURL"]
        return url

    def get_assign_result_from_response(self, response):
        response_json = response.json()
        self._check_errors(response_json)
        result = response_json["data"]["assignAsset"]
        return result

    def _check_errors(self, response_json):
        if "errors" in response_json:
            errors = response_json["errors"]
            raise APIFormatException(message=errors[0]["message"])
